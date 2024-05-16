#!/usr/bin/env python
# coding: utf-8

import hashlib
import json
import os

import mysql.connector
import requests
from bs4 import BeautifulSoup
from db_config import (MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD,
                       MYSQL_USERNAME)

hash_directory = "hashes"

def get_page_hash(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        anchor_content = ''.join(str(tag) for tag in soup.find_all('a'))
        page_hash = hashlib.md5(anchor_content.encode()).hexdigest()
        return page_hash
    except Exception as e:
        print(f"Error: {e}")
        return None


# Connect to your MySQL server
dataBase = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    database = MYSQL_DATABASE
)

cursor = dataBase.cursor()

def has_webpage_changed(url, department_vacc_id):
    current_hash = get_page_hash(url)
    if current_hash is None:
        return False

    hash_file = os.path.join(hash_directory, f"{department_vacc_id}.txt")

    if not os.path.exists(hash_file):
        with open(hash_file, 'w') as file:
            file.write(current_hash)
        return False

    with open(hash_file, 'r') as file:
        stored_hash = file.read()

    if current_hash != stored_hash:
        with open(hash_file, 'w') as file:
            file.write(current_hash)

        # Update the status to 'new_vac'
        cursor = dataBase.cursor()
        cursor.execute("UPDATE department_vac_record SET is_new_vac = '1' WHERE id = %s", (department_vacc_id,))
        dataBase.commit()

        print(f"Change detected for department ID {department_vacc_id}")
        return True
    return False

def main():
    cursorObj = dataBase.cursor(dictionary=True)
    cursorObj.execute("SELECT id, career_url FROM department_vac_record")
    department_vacc_data = cursorObj.fetchall()

    for data in department_vacc_data:
        department_vacc_id = data['id']
        career_url = data['career_url']

        if has_webpage_changed(career_url, department_vacc_id):
            print(f"Website has been updated for data ID {department_vacc_id}!")
        else:
            # Website has not changed, update the status to 'no_new_vac'
            cursorObj.execute("UPDATE department_vac_record SET is_new_vac = '0' WHERE id = %s", (department_vacc_id,))
            dataBase.commit()
            print(f"Website has not changed for department ID {department_vacc_id}. Status set to 0.")


if __name__ == "__main__":
    if not os.path.exists(hash_directory):
        os.makedirs(hash_directory)
    main()