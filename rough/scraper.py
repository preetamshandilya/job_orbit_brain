from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

# List of URLs to scrape
urls = [
    "https://stackoverflow.com/questions/59347372/how-extract-all-urls-in-a-website-using-beautifulsoup"
]

job_recruitment_links = []  # Store job recruitment links

links = []

for url in urls:
    req = Request(url)
    html_page = urlopen(req)

    # Create BeautifulSoup object
    bs4_obj = BeautifulSoup(html_page, 'html.parser')
    
#     for link in bs4_obj.findAll('a'):
#      links.append(link.get('href'))
# #print(links)

# #     Find job recruitment links
# #     job_recruitment_link = bs4_obj.find('a', string='Job Recruitment')
#     job_link_pattern = re.compile(r"(job|recruit|career|employment|apply|teaching)", re.IGNORECASE)
    
#     job_recruitment_link = bs4_obj.find("a", href=job_link_pattern)

#     if not job_recruitment_link:
#         job_recruitment_link = bs4_obj.find('a', href=re.compile(r'job', re.IGNORECASE))
        
#     if not job_recruitment_link:
#         job_recruitment_link = bs4_obj.find('a', href=re.compile(r'Recruitment', re.IGNORECASE))

#     if not job_recruitment_link:
#         job_recruitment_link = bs4_obj.find('a', href=re.compile(r'jobrecruitment', re.IGNORECASE))

#     # Get the href attribute (the URL) of the link and store in the list
#     if job_recruitment_link:
#         job_recruitment_url = job_recruitment_link.get('href')
#         job_recruitment_links.append(job_recruitment_url)

# # Saving links to a separate file
# with open("job_recruitment_links.txt", "w") as file:
#     file.write("Job Recruitment Links:\n")
#     for link in job_recruitment_links:
#         file.write(link + "\n")


with open('link.txt','w') as file:
        file.write('all links: \n')
        for link in links:
           file.write(link + '\n')


# from bs4 import BeautifulSoup
# from urllib.request import Request, urlopen
# import re

# # List of URLs to scrape
# urls = [
#     "https://www.jnu.ac.in/"
# ]

# job_recruitment_links = []  # Store job recruitment links

# for url in urls:
#     req = Request(url)
#     html_page = urlopen(req)

#     # Create BeautifulSoup object
#     bs4_obj = BeautifulSoup(html_page, 'lxml')

#     # Find all anchor tags on the page
#     for link in bs4_obj.find_all('a'):
#         # Check if the link text contains keywords related to job recruitment
#         link_text = link.get_text()
#         if re.search(r"(job|recruit|career|employment|apply|teaching)", link_text, re.IGNORECASE):
#             job_recruitment_links.append(link.get('href'))
#         else:
#             # Check if the href attribute contains keywords related to job recruitment
#             href = link.get('href')
#             if href and re.search(r"(job|recruit|career|employment|apply|teaching)", href, re.IGNORECASE):
#                 job_recruitment_links.append(href)

# # Saving links to a separate file
# with open("job_recruitment_links.txt", "w") as file:
#     file.write("Job Recruitment Links:\n")
#     for link in job_recruitment_links:
#         file.write(link + "\n")





        


