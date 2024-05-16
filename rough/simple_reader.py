import PyPDF2

pdf = PyPDF2.PdfReader("Advertisement_RC_68_2023-1.pdf")

text = ""

for i in range(10):  # Pages are indexed from 0 to n-1
    text += pdf.pages[i].extract_text()

with open("t.txt", "w", encoding="utf-8") as f:
    f.write(text)
