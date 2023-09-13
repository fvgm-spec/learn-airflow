# Learn Airflow by doing

This repository is intended to store information regarding Airflow settings and tutorials.

### Quick start book:

* [Data_Pipelines_with_Apache_Airflow](https://biconsult.ru/files/Data_warehouse/Bas_P_Harenslak%2C_Julian_Rutger_de_Ruiter_Data_Pipelines_with_Apache.pdf)

### First steps

Installing Airflow in WSL2

* Prerequisites: This step-by-step assumes that you're familiar with using the command line and can set up your development environment as directed.
* Set Up the Virtual Environment: If you have Anaconda installed in your system, first go to your home directory `cd ~` then run `conda create -c conda-forge -n airflow python=3.11 pyarrow` in order to create a virtual environment named **airflow** with python 3.11 and pyarrow installed.
* Then activate your environment by running `conda activate airflow`
* Set Up the Airflow Directory: Create the folder called **airflow** in your home directory by running `mkdir airflow`, then set that directory into your env variables by `nano ~/.bashrc`, in the last line of that file include `AIRFLOW_HOME=/home/[YourUsername]/airflow`, then press Ctrl+X and save changes, then source them `source ~/.bashrc` in order to set the changes in the **bashrc** file, after that in order to check that the env variable was set successfully just run `cd $AIRFLOW_HOME` like in the screeshot bellow.
   
  Adding AIRFLOW_HOME to bashrc
  ![bashrc](img/bashrc.png)

  Checking that the env variable was set successfully
  ![airflowhome](img/airflow_home.png)
  
* Install Apache Airflow: In order to install airflow in your virtual environment run `pip install apache-airflow`, but before that check that you are under the conda virtual env, then you will need to initialize the database by running `airflow db init` . After that you will need to create a folder called **dags** in your airflow directory, this folder will store your airflow [dags](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) that just definesthwe Tasks and dictates the order in which they have to run, generally are python scripts.
* Create an Airflow User: In this step you'll need to create a user. This user will be used to login into the Airflow UI and perform some admin functions. Run the following in your command line
  
  ```bash
    airflow users create \
      --username Admin \
      --firstname FIRST_NAME \
      --lastname LAST_NAME \
      --role Admin \
      --email admin@example.org
  ```
  
  Installing Airflow in virtual environment
  ![installairflow](img/installing_airflow.png)


**Note**: For further steps on installing Airflow in WSL2 follow this [link](https://www.freecodecamp.org/news/install-apache-airflow-on-windows-without-docker/)

