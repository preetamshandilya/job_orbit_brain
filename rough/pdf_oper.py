import pdfplumber
import requests
import pandas as pd
import re

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

with open("t.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Function to extract pay scale from a given text
def extract_pay_scale(text):
    # Define regular expression patterns for different situations
    pattern = r'\b(?:salary|pay scale|compensation|wage|earnings|SCALE OF PAY|ASSISTANT\s*PROFESSOR)\b[\s:]*((?:Rs|[$€£¥₹])?[\d,]+(?:\.\d{2})?)'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return matches

# Read the entire content of the "text.txt" file
with open("t.txt", "r", encoding="utf-8") as file:
    file_content = file.read()

# Flag to indicate whether pay scale is found
pay_scale_found = False
search_string = "assistant professor"

# Split the content into lines
lines = file_content.split("\n")

# Iterate through the patterns and search for each one in the text
for line in lines:
    if search_string in line.lower():
        salary = extract_pay_scale(line)
        if salary:
            print("Pay Scale for Assistant Professor:", salary)
            with open("asst_prof_info.txt", "w") as output_file:
                output_file.write(f"Pay Scale for Assistant Professor: {salary}\n")
            pay_scale_found = True
            break
        else:
            print("Pay scale pattern not found in the line:", line)
    else:
        print("Search string not found in the line:", line)


if not pay_scale_found:
    print("Pay scale for Assistant Professor not found in the text file.")
