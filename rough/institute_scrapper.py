# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# import re
# from urllib.parse import urljoin

# # Define a function to extract links from a given URL and save them to a file
# def extract_links_and_save(url, base_url, keywords_pattern):
#     links = []

#     res = requests.get(url).text
#     soup = BeautifulSoup(res, 'lxml')

#     for link in soup.find_all('a', href=True):
#         href = link.get('href')
#         text = link.get_text()

#         if re.search(keywords_pattern, href) or re.search(keywords_pattern, text):
#             if href.startswith(('http://', 'https://')):
#                 links.append(href)
#             elif href.startswith('/'):
#                 absolute_url = urljoin(base_url, href)
#                 links.append(absolute_url)
#             else:
#                 links.append(base_url + href)

#     return links

# # Initial URL
# initial_url = "https://www.bbau.ac.in/"
# base_url = "https://www.bbau.ac.in/"
# keywords_pattern = re.compile(r'job|jobs|recruitment|vacancy|notification|career|teaching', re.IGNORECASE)

# visited_urls = set()
# to_visit_urls = set([initial_url])

# while to_visit_urls:
#     url_to_visit = to_visit_urls.pop()

#     if url_to_visit not in visited_urls:
#         visited_urls.add(url_to_visit)

#         print(f"Visiting: {url_to_visit}")

#         # Extract links from the current URL and append them to to_visit_urls
#         extracted_links = extract_links_and_save(url_to_visit, base_url, keywords_pattern)
#         to_visit_urls.update(extracted_links)

# # Save visited URLs to a file
# file_path = "visited_links.txt"

# with open(file_path, "w") as file:
#     for link in visited_urls:
#         file.write(link + "\n")

# print(f"Visited links have been saved to {file_path}")


from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from urllib.parse import urljoin

# Define a function to extract links from a given URL and save them to a file
def extract_links_and_save(url, base_url, keywords_pattern, used_keywords):
    links = []

    res = requests.get(url).text
    soup = BeautifulSoup(res, 'lxml')

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text()

        # Check if the href or link text contains any keywords that haven't been used yet
        if re.search(keywords_pattern, href) or re.search(keywords_pattern, text):
            unused_keywords = [kw for kw in keywords_pattern.findall(href + text) if kw.lower() not in used_keywords]
            if unused_keywords:
                used_keywords.update(unused_keywords)
                if href.startswith(('http://', 'https://')):
                    links.append(href)
                elif href.startswith('/'):
                    absolute_url = urljoin(base_url, href)
                    links.append(absolute_url)

    return links

# Initial URL
initial_url = "https://www.bbau.ac.in/"
base_url = "https://www.bbau.ac.in/"
keywords_pattern = re.compile(r'job|jobs|recruitment|vacancy|notification|career|teaching', re.IGNORECASE)
used_keywords = set()  # Store used keywords

visited_urls = set()
to_visit_urls = set([initial_url])
links = []  # Define the 'links' list here

while to_visit_urls:
    url_to_visit = to_visit_urls.pop()

    if url_to_visit not in visited_urls:
        visited_urls.add(url_to_visit)

        print(f"Visiting: {url_to_visit}")

        # Extract links from the current URL
        extracted_links = extract_links_and_save(url_to_visit, base_url, keywords_pattern, used_keywords)

        # Filter extracted links to include only those in the 'links' list
        filtered_links = [link for link in extracted_links if link in links]

        to_visit_urls.update(filtered_links)

# Save visited URLs to a file
file_path = "visited_links.txt"

with open(file_path, "w") as file:
    for link in visited_urls:
        file.write(link + "\n")

print(f"Visited links have been saved to {file_path}")


