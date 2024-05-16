from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

req = Request("https://www.jnu.ac.in/node")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
internal_links = []

for link in soup.findAll('a'):
    href = link.get('href')
    if href:
        if href.startswith('http') or href.startswith('/'):
            links.append(href)
        else:
            internal_links.append(href)

# Specify the file path where you want to save the links
file_path = "links.txt"
internal_file_path = "internal_links.txt"

# Open the file in write mode and write the links to it
with open(file_path, "w") as file:
    for link in links:
        file.write(link + "\n")

with open(internal_file_path, "w") as internal_file:
    for link in internal_links:
        internal_file.write(link + "\n")

print(f"External Links have been saved to {file_path}")
print(f"Internal Links have been saved to {internal_file_path}")




