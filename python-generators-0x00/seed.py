'''
Objective: create a generator that streams rows from an SQL database one by one.

Instructions:

Write a python script that seed.py:

Set up the MySQL database, ALX_prodev with the table user_data with the following fields:
user_id(Primary Key, UUID, Indexed)
name (VARCHAR, NOT NULL)
email (VARCHAR, NOT NULL)
age (DECIMAL,NOT NULL)

Populate the database with the sample data from this user_data.csv
Prototypes:
    
    def connect_db() :- connects to the mysql database server
    
    def create_database(connection):- creates the database ALX_prodev if it does not exist
    
    def connect_to_prodev() connects the the ALX_prodev database in MYSQL
    
    def create_table(connection):- creates a table user_data if it does not exists with the required fields
    
    def insert_data(connection, data):- inserts data in the database if it does not exist
'''

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import csv

load_dotenv()


class DBConfig:
    def __init__(self, host=None, user=None, password=None, database=None):
        self.connection = self._connect_db(host, user, password, database)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def _connect_db(self, host=None, user=None, password=None, database=None):
        host = host if host else os.getenv('DB_HOST')
        user = user if user else os.getenv('DB_USER')
        password = password if password else os.getenv('DB_PASSWORD')

        try:
            connection = mysql.connector.connect(
                host=host,  
                user=user, 
                password=password
            )

            if connection.is_connected():
                print("Connected to MySQL database")

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

        finally:
            if connection.is_connected():
                return connection

    def create_database(self):
        cursor = self.connection.cursor()

        query = 'CREATE DATABASE IF NOT EXISTS ALX_prodev'

        try:
            cursor.execute(query)
            print('Database created successfully')
            cursor.close()
        except Error as e:
            print('Error creating database')
            print('Reason ' + e)
        finally:
            cursor.close()

    def connect_to_prodev(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),  
                user=os.getenv('DB_USER'), 
                password=os.getenv('DB_PASSWORD'),
                database='ALX_prodev'
            )

            if self.connection.is_connected():
                print("Connected to ALX_prodev")

        except Error as e:
            print(f"Error while connecting to ALX_prodev: {e}")

        finally:
            if self.connection.is_connected():
                return self.connection

class File: 
    def __init__(self, file_name): 
        self.file_obj = open(file_name, mode='r', newline='')

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.close()


# creating mysql connection
def connect_db():
    with DBConfig() as db_connection:
        return db_connection.connection
    

# function to create database
def create_database(connection):
    with DBConfig() as db_connection:
        db_connection.create_database()

# function to connect to DB
def connect_to_prodev():
    db_connection = DBConfig()
    return db_connection.connect_to_prodev()

# function to create table
def create_table(connection):
    try:
        cursor = connection.cursor()
    except mysql.connector.errors.OperationalError:
        with DBConfig() as db_connection:
            connection = db_connection.connect_to_prodev()
            cursor = connection.cursor()

    query = '''
        CREATE TABLE IF NOT EXISTS user_data(
            user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
            name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(3, 0) NOT NULL
        );
    '''

    try:
        cursor.execute(query)
        print('Table created successfully')
    except Error as e:
        print('Error creating database')
        print('Reason ', e)
        cursor.close()
    finally:
        cursor.close()

# function to insert data to db
def insert_data(connection, data):
    try:
        cursor = connection.cursor()
    except mysql.connector.errors.OperationalError:
        with DBConfig() as db_connection:
            connection = db_connection.connect_to_prodev()
            cursor = connection.cursor()

    with File(data) as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                query = 'INSERT INTO user_data(name, email, age) VALUES (%s, %s, %s);'

                cursor.execute(query, (row['name'], row['email'], float(row['age'])))
                connection.commit()
            except Error as e:
                print('Error inserting data', e)
        
    