# nyc-crashes

## Context

This project is the first project of datapreprocessing of the BeCode training.

## Description

In this project, I try to complete a dataset from the [NYC Open Data site](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95).

My solution uses a connected API, Geopy, to recover geographic data based on the latitude and longitude I got in the dataset.

On another part, I clean the data based on my feelings of what could be useful in a future project.

## Usage

You can run the DataPreprocessing file. It takes about 15 hours to process all 100000 rows.

## Python libraries

The needed libraries are in the requirement.txt. To install it, use the command below:  

`python -m pip install -r requirements.txt`  

We use pandas for cleaning the data, geopy to get some new data.

*Links to the official documentation of libraries :*
- [Pandas](https://pandas.pydata.org/docs/reference/index.html#api)  
- [Geopy](https://geopy.readthedocs.io/en/stable/)

-----
### Author

*Melvin Leroy, junior AI developer at BeCode*
