from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import urllib.parse
import mysql.connector
import os
import PyPDF2
import io

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
    select_query = "SELECT id FROM institute_detail WHERE name = %s AND institute_url = %s"
    cursorObj.execute(select_query, (name, url))
    result = cursorObj.fetchone()

    if result:
        return result[0]
    else:
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
            try:
                response = requests.head(link)
                status = "success" if response.status_code == 200 else "failure"
            except requests.exceptions.RequestException:
                status = "failure"

            insert_job_link(institute_id, link, status)
            processed_links.add(link)
            
# List of URLs with their corresponding institute names
urls_and_names = [
    ("http://cuj.ac.in/", "Central University of Jharkhand"),
    ("https://www.bbau.ac.in/", "Babasaheb Bhimrao Ambedkar University"),
    ("https://www.amu.ac.in/", "Aligarh Muslim University"),
    ("http://www.aus.ac.in/", "Assam University"),
]

def extract_text_from_pdf(pdf_content):
    try:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))

        # Initialize a variable to store the extracted text
        extracted_text = ""

        # Iterate through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()

        return extracted_text
    except PyPDF2.utils.PdfReadError:
        return ""


# Function to extract and save PDF links matching the regular expression
def extract_and_save_pdf_links(institute_id, link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            if content_type and 'application/pdf' in content_type:
                pdf_content = response.content
                pdf_text = extract_text_from_pdf(pdf_content)
                if re.search(teaching_pattern, pdf_text):
                    pdf_filename = f"{institute_id}_pdf_links.txt"
                    with open(pdf_filename, 'a') as pdf_file:
                        pdf_file.write(urllib.parse.quote(link) + '\n')
            else:
                soup = BeautifulSoup(response.text, 'lxml')
                for a in soup.find_all('a', href=True):
                    href = a.get('href')
                    if re.search(teaching_pattern, href):
                        if href.startswith(('http://', 'https://')):
                            extract_and_save_pdf_links(institute_id, href)
                        elif href.startswith('/'):
                            absolute_url = urljoin(link, href)
                            extract_and_save_pdf_links(institute_id, absolute_url)
                        else:
                            absolute_url = urljoin(link, href)
                            extract_and_save_pdf_links(institute_id, absolute_url)
    except requests.exceptions.RequestException:
        pass

# Regular expression for matching teaching-related links
teaching_pattern = re.compile(r'teaching|assistant professor|carrer', re.IGNORECASE)

# Function to process job links and extract PDF links
def process_job_links():
    select_query = "SELECT institute_id, job_link FROM job_links WHERE status = 'success'"
    cursorObj.execute(select_query)
    job_links = cursorObj.fetchall()

    for institute_id, link in job_links:
        extract_and_save_pdf_links(institute_id, link)

# Add a function call to process job links
process_job_links()

# Close the cursor and database connection
cursorObj.close()
dataBase.close()
