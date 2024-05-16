#!/usr/bin/env python
# coding: utf-8

import json
import os

import mysql.connector
import pandas as pd
from db_config import (MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD,
                       MYSQL_USERNAME)

# excel_file = config["excel_file"]
# table_name = config["table_name"]

# Connect to your MySQL server
dataBase = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    database = MYSQL_DATABASE
)

cursor = dataBase.cursor()

# # CREATE DATABASE


# # cursor.execute("CREATE DATABASE taskOrbit")

# # # Close the cursor and the connection
# # cursor.close()
# # conn.close()


# # CREATE TABLES IN DATABASE

# departmentsTable = """CREATE TABLE departments (
#     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL UNIQUE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# )"""

# cursor.execute(departmentsTable)
# dataBase.commit()

# institutesTable = """CREATE TABLE institutes (
#     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL UNIQUE,
#     department_id INT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     FOREIGN KEY (department_id) REFERENCES departments(id)
# )"""

# cursor.execute(institutesTable)
# dataBase.commit()

# departmentRecords = """CREATE TABLE department_vac_record (
#     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#     institute_id INT,
#     department_id INT,
#     career_url TEXT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     is_new_vac ENUM('0', '1') DEFAULT '0',
#     FOREIGN KEY (institute_id) REFERENCES institutes(id),
#     FOREIGN KEY (department_id) REFERENCES departments(id)
# )"""
# cursor.execute(departmentRecords)
# dataBase.commit()
# cursor.close()

print(os.getcwd())

df = pd.read_excel("vaccancy_tracker/Careerlist.xlsx")

for index, row in df.iterrows():
    department_name = row["Department Name"]
    institute_name = row["Institute Name"]
    career_url = row["Career URL"]

    # Check if the department already exists
    cursor.execute("SELECT id FROM departments WHERE name = %s", (department_name,))
    department_exists = cursor.fetchone()

    if not department_exists:
        # Insert the department into the 'departments' table
        cursor.execute("INSERT INTO departments (name) VALUES (%s)", (department_name,))
        department_id = cursor.lastrowid
    else:
        department_id = department_exists[0]

    # Check if the institute already exists
    cursor.execute("SELECT id FROM institutes WHERE name = %s", (institute_name,))
    institute_exists = cursor.fetchone()

    if not institute_exists:
        # Insert the institute into the 'institutes' table
        cursor.execute("INSERT INTO institutes (name, department_id) VALUES (%s, %s)", (institute_name, department_id))
        institute_id = cursor.lastrowid
    else:
        institute_id = institute_exists[0]

    # Check if the career URL already exists
    cursor.execute("SELECT id FROM department_vac_record WHERE career_url = %s", (career_url,))
    url_exists = cursor.fetchone()

    if not url_exists:
        # Insert the record into the 'department_vac_record' table
        cursor.execute("INSERT INTO department_vac_record (institute_id, department_id, career_url) VALUES (%s, %s, %s)",
                       (institute_id, department_id, career_url))
    dataBase.commit()

cursor.close()
dataBase.close()