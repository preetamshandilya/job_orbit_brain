import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Define the regular expression pattern to match job application links
job_link_pattern = re.compile(r'jobs|career|employment|vacancy|recruitment|apply', re.IGNORECASE)

# Define a list of university URLs
university_urls = [
    "https://www.jnu.ac.in/node",
    # Add more university URLs as needed
]

job_links = []

def extract_job_links(url):
    print("Source URL:", url)
    source_url = requests.get(url)
    soup = BeautifulSoup(source_url.content, "html.parser")
    
    for link in soup.find_all('a', href=True):
        try:
            href = link.get('href')
            if href not in job_links and re.search(job_link_pattern, href):
                if not href.startswith("http"):
                    # Check if the URL is relative, and construct an absolute URL
                    if href.startswith("/"):
                        href = url + href
                    else:
                        href = url + "/" + href
                job_links.append(href)

        except Exception as e:
            print("Unhandled exception:", e)

    # Extract job links from <link> elements
    for link in soup.find_all('link', href=True):
        try:
            href = link.get('href')
            if href not in job_links and re.search(job_link_pattern, href):
                if not href.startswith("http"):
                    # Check if the URL is relative, and construct an absolute URL
                    if href.startswith("/"):
                        href = url + href
                    else:
                        href = url + "/" + href
                job_links.append(href)

        except Exception as e:
            print("Unhandled exception:", e)

# Iterate through university URLs and extract job links
for university_url in university_urls:
    extract_job_links(university_url)

df = pd.DataFrame({"job_links": job_links})
df.to_csv("job_links.csv")


































# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# url = "https://www.exampleuniversity.com"
# df = pd.DataFrame()
# links = []
# def extract_links(url):
#     print("source url",url)
#     global links
#     source_url = requests.get(url)
#     soup = BeautifulSoup(source_url.content,"html.parser")
#     for link in soup.find_all('a',href=True):
#         try:
#             if link.get('href').startswith("https://") and link.get("href") not in links:
#                 links.append(link.get('href'))
#                 extract_links(link.get('href'))

#         except Exception as e:
#             print("Unhandled exception",e)

# extract_links(url)
# df = pd.DataFrame({"links":links})
# df.to_csv("links.csv")