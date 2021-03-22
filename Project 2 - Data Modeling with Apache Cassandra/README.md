# Udacity - Data Enginnering Nanodegree Program

## Project 2 - Data Modeling with Apache Cassandra

## Datasets
For this project, you'll be working with one dataset: **event_data**. The directory of CSV files partitioned by date. Here are examples of filepaths to two files in the dataset:

´´´
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
´´´

## Project Steps
Below are steps you can follow to complete each component of this project.

**Modeling your NoSQL database or Apache Cassandra database**
1- Design tables to answer the queries outlined in the project template
2- Write Apache Cassandra CREATE KEYSPACE and SET KEYSPACE statements
3- Develop your CREATE statement for each of the tables to address each question
4- Load the data with INSERT statement for each of the tables
5- Include IF NOT EXISTS clauses in your CREATE statements to create tables only if the tables do 6- not already exist. We recommend you also include DROP TABLE statement for each table, this way 7- you can run drop and create tables whenever you want to reset your database and test your ETL pipeline
8 -Test by running the proper select statements with the correct WHERE clause