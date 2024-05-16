
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import mysql.connector

#database connectivity
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="user",
  passwd ="password",
  database = "institutes"
)

cursorObj= dataBase.cursor()
# cursorObj.execute("CREATE DATABASE institutes")

# creating table
instituteRecords = """CREATE TABLE institute_detail (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    institute_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)"""

jobLinkRecords = """CREATE TABLE job_links (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    institute_id INT,
    job_link TEXT,
    status ENUM('success', 'failure') DEFAULT 'success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (institute_id) REFERENCES institute_detail(id)
)"""



cursorObj.execute(instituteRecords)
cursorObj.execute(jobLinkRecords)


dataBase.commit()
cursorObj.close()
dataBase.close()


# # Function to extract and save links for a given URL
# def extract_and_save_links(url, file, processed_links):
#     links = []
#     res = requests.get(url).text
#     soup = BeautifulSoup(res, 'lxml')

#     keywords_pattern = re.compile(r'job|jobs|recruitment|vacancy|notification|career|teaching|careerteaching|universityjob', re.IGNORECASE)

#     for link in soup.find_all('a', href=True):
#         href = link.get('href')
#         text = link.get_text()

#         if re.search(keywords_pattern, href) or re.search(keywords_pattern, text):
#             if href.startswith(('http://', 'https://')):
#                 links.append(href)
#             elif href.startswith('/'):
#                 absolute_url = urljoin(url, href)
#                 links.append(absolute_url)
#             else:
#                 links.append(url + href)

#     with open(file, "a") as file:
#         file.write(f"Links for {url}:\n")
#         for link in links:
#             if link not in processed_links:
#                 file.write(link + "\n")
#                 processed_links.add(link)
#         file.write("\n")

# # List of URLs to process
# urls = [
#     "http://cuj.ac.in/","http://www.bbau.ac.in/","http://www.amu.ac.in/","http://www.aus.ac.in/",
#     # Add more URLs here as needed
# ]

# # Output file
# output_file = "links.txt"

# # Set to store processed links
# processed_links = set()

# # Process each URL and save links
# for url in urls:
#     extract_and_save_links(url, output_file, processed_links)

# print(f"Links have been saved to {output_file}")





