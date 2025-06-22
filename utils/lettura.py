# importing required modules
from PyPDF2 import PdfReader

# creating a pdf reader object
reader = PdfReader('2023_05.pdf')

# printing number of pages in pdf file
num_pages = len(reader.pages)
print(f"Total number of pages in the PDF: {num_pages}\n")

# Loop through all pages and extract text
for page_num in range(0,2):
    page = reader.pages[page_num]
    
    # extracting text from the current page
    text = page.extract_text()
    
    # printing the text from the current page
    print(f"Page {page_num + 1}:\n{text}\n")
