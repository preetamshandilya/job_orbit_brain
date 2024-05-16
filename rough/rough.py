import urllib.parse
from bs4 import BeautifulSoup
import requests

url= "http://cuj.ac.in/file/Assistant Professor-Geography- for uploadingJuly2023.pdf"

x=urllib.parse.quote(url)
res= requests.get(x).text
soup = BeautifulSoup(res, 'lxml')

print(soup)

# print(x)



