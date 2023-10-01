# Import necessary modules and libraries
# Documentation of pageview format: https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageviews
from urllib import request
import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Creating an Airflow DAG with specified settings
dag = DAG(
    dag_id="read_wiki_pages",                  # Unique identifier for the DAG
    start_date=airflow.utils.dates.days_ago(1),  # Start date for the DAG (1 day ago)
    schedule_interval="@hourly",                # Schedule the DAG to run hourly
    template_searchpath="/tmp",                # Search path for templates
    max_active_runs=1,                         # Maximum concurrent runs of the DAG
)

# Defining a function to retrieve data from Wikipedia pageviews URL and save it to a file
def _get_data(year, month, day, hour, output_path):
    # Construct the URL based on the provided date and time
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    # Retrieve data from the URL and save it to the specified output path
    request.urlretrieve(url, output_path)

# Defining a function to extract pageview data and prepare it for insertion into a PostgreSQL database
def _fetch_pageviews(pagenames, execution_date):
    result = dict.fromkeys(pagenames, 0)

    # Read pageview data from a file and process it
    with open("/tmp/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(" ")
            if domain_code == "en" and page_title in pagenames:
                result[page_title] = view_counts

    # Generate SQL queries to insert data into a PostgreSQL database
    with open("/tmp/postgres_query.sql", "w") as f:
        for pagename, pageviewcount in result.items():
            f.write(
                "INSERT INTO pageview_counts VALUES ("
                f"'{pagename}', {pageviewcount}, '{execution_date}'"
                ");\n"
            )

# Creating a PythonOperator task to fetch data from a URL
get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={
        "year": "{{ execution_date.year }}",
        "month": "{{ execution_date.month }}",
        "day": "{{ execution_date.day }}",
        "hour": "{{ execution_date.hour }}",
        "output_path": "/tmp/wikipageviews.gz",
    },
    dag=dag,
)

# Create a PythonOperator task to process and prepare pageview data
fetch_pageviews = PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    op_kwargs={"pagenames": {"Google", "Amazon", "Apple", "Microsoft", "Facebook"}},
    dag=dag,
)

# Create a BashOperator task to unzip the downloaded data using the command-line-based Linux utility gunzip 
extract_gz = BashOperator(
    task_id="extract_gz",
    bash_command="gunzip --force /tmp/wikipageviews.gz",
    dag=dag
)

# Create a PostgresOperator task to write data to a PostgreSQL database
write_to_postgres = PostgresOperator(
    task_id="write_to_postgres",
    postgres_conn_id="my_postgres",  # Connection ID for PostgreSQL
    sql="postgres_query.sql",         # SQL file containing insertion queries
    dag=dag,
)

# Define task dependencies (execution order)
get_data >> extract_gz >> fetch_pageviews >> write_to_postgres