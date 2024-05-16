from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import mysql.connector

# Database connectivity
dataBase = mysql.connector.connect(
    host="localhost",
    user="user",
    passwd="password",
    database="institutes"
)

cursorObj = dataBase.cursor()

# Function to insert institute details and return the generated ID
def insert_institute_details(name, url):
    insert_query = "INSERT INTO institute_detail (name, institute_url) VALUES (%s, %s)"
    cursorObj.execute(insert_query, (name, url))
    dataBase.commit()
    return cursorObj.lastrowid

# Function to extract and save job links with the given institute ID
def extract_and_save_links(url, institute_name, processed_links):
    institute_id = insert_institute_details(institute_name, url)

    links = []
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'lxml')

    keywords_pattern = re.compile(r'job|jobs|recruitment|vacancy|notification|career|teaching|careerteaching|universityjob', re.IGNORECASE)

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text()

        if re.search(keywords_pattern, href) or re.search(keywords_pattern, text):
            if href.startswith(('http://', 'https://')):
                links.append(href)
            elif href.startswith('/'):
                absolute_url = urljoin(url, href)
                links.append(absolute_url)
            else:
                links.append(url + href)

    for link in links:
        if link not in processed_links:
            # Insert the data into the job_links table
            insert_query = "INSERT INTO job_links (institute_id, job_link) VALUES (%s, %s)"
            cursorObj.execute(insert_query, (institute_id, link))
            processed_links.add(link)

    dataBase.commit()

# List of URLs with their corresponding institute names
urls_and_names = [
    ("http://cuj.ac.in/", "Central University of Jharkhand"),
    ("http://www.bbau.ac.in/", "Babasaheb Bhimrao Ambedkar University"),
    ("http://www.amu.ac.in/", "Aligarh Muslim University"),
    ("http://www.aus.ac.in/", "Assam University"),
]

processed_links = set()

# Saving links to the database
for url, institute_name in urls_and_names:
    extract_and_save_links(url, institute_name, processed_links)

print("Links have been saved to the database.")

cursorObj.close()
dataBase.close()
