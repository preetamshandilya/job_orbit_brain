from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import os
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import urllib
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
# def insert_institute_details(name, url):
#     insert_query = "INSERT INTO institute_detail (name, institute_url) VALUES (%s, %s)"
#     cursorObj.execute(insert_query, (name, url))
#     dataBase.commit()
#     return cursorObj.lastrowid

def insert_institute_details(name, url):
    # Check if the institute already exists
    select_query = "SELECT id FROM institute_detail WHERE name = %s AND institute_url = %s"
    cursorObj.execute(select_query, (name, url))
    result = cursorObj.fetchone()

    if result:
        return result[0]
    else:
        # Insert the institute if it doesn't exist
        insert_query = "INSERT INTO institute_detail (name, institute_url) VALUES (%s, %s)"
        cursorObj.execute(insert_query, (name, url))
        dataBase.commit()
        return cursorObj.lastrowid

# Function to insert job link with the given institute ID and status
def insert_job_link(institute_id, link, status):
    insert_query = "INSERT INTO job_links (institute_id, job_link, status) VALUES (%s, %s, %s)"
    cursorObj.execute(insert_query, (institute_id, link, status))
    dataBase.commit()

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
            # Check if the link is valid
            try:
                response = requests.head(link)
                status = "success" if response.status_code == 200 else "failure"
            except requests.exceptions.RequestException:
                status = "failure"

            # Insert the data into the job_links table with status
            insert_job_link(institute_id, link, status)
            processed_links.add(link)

# List of URLs with their corresponding institute names
urls_and_names = [
    ("http://cuj.ac.in/", "Central University of Jharkhand"),
    ("https://www.bbau.ac.in/", "Babasaheb Bhimrao Ambedkar University"),
    ("https://www.amu.ac.in/", "Aligarh Muslim University"),
    ("http://www.aus.ac.in/", "Assam University"),
]

processed_links = set()


visited_link=set()
def extract_and_save_pdf_links(institute_id,link):
    # if visited_link is None:
    #     visited_link=set()
           
    try:
        response = requests.get(link)
        if response.status_code==200:
            visited_link.add(link)
            soup= BeautifulSoup(response.content, "html.parser")
        for a_tag in soup.find_all('a',href=True):
            href = a_tag['href']
            if href.endswith('.pdf'):
                    pdf_link = urllib.parse.urljoin(link, href)
                    pdf_filename = os.path.basename(pdf_link)
                    
                    # Check if the PDF filename contains the job_link_pattern
                    if re.search(teaching_pattern, pdf_filename):
                        pdf_filename = f"{institute_id}_pdf_links.txt"
                        with open(pdf_filename, 'a') as pdf_file:
                            pdf_file.write(urllib.parse.quote(pdf_link) + '\n')

            else:
                if re.search(teaching_pattern, href):
                        if href.startswith(('http://', 'https://')):
                            extract_and_save_pdf_links(institute_id, href)
                        elif href.startswith('/'):
                            absolute_url = urljoin(link, href)
                            extract_and_save_pdf_links(institute_id, absolute_url)
                        else:
                            absolute_url = urljoin(link, href)
                            extract_and_save_pdf_links(institute_id, absolute_url)
        
        # for a_tag in soup.find_all('a', href=True):
        #         next_link = urllib.parse.urljoin(link, a_tag['href'])
        #         if next_link not in visited_link and re.search(teaching_pattern, next_link):
        #             extract_and_save_pdf_links(institute_id, next_link, teaching_pattern, visited_link)     
    except requests.exceptions.RequestException:
        pass        
        
teaching_pattern = re.compile(r'teaching|assistant professor', re.IGNORECASE)


# Function to process job links and extract PDF links
def process_job_links():
    select_query = "SELECT institute_id, job_link FROM job_links WHERE status = 'success'"
    cursorObj.execute(select_query)
    job_links = cursorObj.fetchall()

    for institute_id, link in job_links:
        extract_and_save_pdf_links(institute_id, link)

process_job_links()

# Saving links to the database
for url, institute_name in urls_and_names:
    extract_and_save_links(url, institute_name, processed_links)

print("Links have been saved to the database.")

cursorObj.close()
dataBase.close()
    
