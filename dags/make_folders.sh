#!/bin/bash

# Get the current date in the format MM-DD
folder_name=$(date +"%m-%d")

# Specify the directory where you want to create the folder
data_folder="/tmp/data"
image_folder="/tmp/img"

# Create the data_folder if it doesn't exist
if [ ! -d "$data_folder/$folder_name" ]; then
    mkdir -p "$data_folder/$folder_name"
    echo "Folder '$folder_name' created in $data_folder"
else
    echo "Folder '$folder_name' already exists in $data_folder"
fi

# Create the data_folder if it doesn't exist
if [ ! -d "$image_folder/$folder_name" ]; then
    mkdir -p "$image_folder/$folder_name"
    echo "Folder '$folder_name' created in $image_folder"
else
    echo "Folder '$folder_name' already exists in $image_folder"
fi