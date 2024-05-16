import requests
import pdfplumber

# def download_files(url):
#     local_filename = url.split("/")[-1]
#     with requests.get(url) as r:
#         with open(local_filename, "wb") as f:
#             f.write(r.content)
#     return local_filename

def download_files(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        local_filename = url.split("/")[-1]
        with open(local_filename, "wb") as f:
            f.write(response.content)
        return local_filename
    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)
        return None

url_name = "https://adda247jobs-wp-assets-adda247.s3.ap-south-1.amazonaws.com/jobs/wp-content/uploads/sites/13/2023/05/14153240/Advertisement_RC_68_2023-1.pdf"

data = download_files(url_name)

with pdfplumber.open(data) as pdf:
    text = pdf.pages[0].extract_text()

info_found = False
info = ""

for row in text.split("\n"):
    if info_found:
        info += row + "\n"
    if row.startswith("ASSISTANT PROFESSOR:"):
        info_found = True
        info+=row

if info_found:
    print(info)

with open("text.txt", "w", encoding="utf-8") as f:
    f.write(info)
    

    