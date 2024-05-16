# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# import re
# from urllib.request import Request, urlopen
# from urllib.parse import urljoin


# url = "http://cuj.ac.in/"

# links=[]

# base_url = "http://cuj.ac.in/"

# res = requests.get(url).text

# # Parsing the HTML content
# soup = BeautifulSoup(res, 'lxml')

# # Define a regular expression pattern for keywords
# keywords_pattern = re.compile(r'job|jobs|recruitment|vacancy|notification|career|teaching|careerteaching|universityjob', re.IGNORECASE)


# # for link in soup.find_all('a', href=True, string=keywords_pattern):
# #     href = link.get('href')
# #     if href:
    
# #         if href.startswith(('http://', 'https://')):
# #             links.append(href)
# #         elif href.startswith('/'):
# #             absolute_url = urljoin(base_url, href)
# #             links.append(absolute_url)
# #         else:
# #             text = link.get_text()
# #             if re.search(keywords_pattern, text):
# #                 links.append(href)

# # Find all anchor elements that match the condition
# for link in soup.find_all('a', href=True):
#     href = link.get('href')
#     text = link.get_text()

#     if re.search(keywords_pattern, href) or re.search(keywords_pattern, text):
#         if href.startswith(('http://', 'https://')):
#             links.append(href)
#         elif href.startswith('/'):
#             absolute_url = urljoin(base_url, href)
#             links.append(absolute_url)
#         else:
#             links.append(base_url + href)

            

# with open(f"links.txt", "w") as file:
#     for link in links:
#         file.write(link + "\n")
        
# print(f"Links have been saved to links.txt")

from bs4 import BeautifulSoup
import requests
import re
from urllib.request import Request, urlopen
from urllib.parse import urljoin

# List of URLs to scrape
urls = ["http://cuj.ac.in/", "http://example.com/", "http://another-example.com/"]

# Define a regular expression pattern for keywords
keywords_pattern = re.compile(r'job|jobs|recruitment|vacancy|notification|career|teaching|careerteaching|universityjob', re.IGNORECASE)

# Create a dictionary to store links for each URL
url_links = {}

# Loop through the list of URLs
for url in urls:
    links = []
    base_url = url
    
    res = requests.get(url).text
    
    # Parsing the HTML content
    soup = BeautifulSoup(res, 'lxml')
    
    # Find all anchor elements that match the condition
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text()
    
        if re.search(keywords_pattern, href) or re.search(keywords_pattern, text):
            if href.startswith(('http://', 'https://')):
                links.append(href)
            elif href.startswith('/'):
                absolute_url = urljoin(base_url, href)
                links.append(absolute_url)
            else:
                links.append(base_url + href)
    
    # Store the links in the dictionary with the URL as the key
    url_links[url] = links

# Save all links to a single file
with open("all_links.txt", "w") as file:
    for url, links in url_links.items():
        file.write(f"Links for {url}:\n")
        for link in links:
            file.write(link + "\n")

print("All links have been saved to all_links.txt")


        
        
        
        





