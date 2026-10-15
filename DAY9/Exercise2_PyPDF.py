# 1. Open the PDF using PdfReader .
from pypdf import PdfReader
reader=PdfReader("EY_Digital_PDF_Practice.pdf")
print("pdf readed")

# 2. Print the number of pages.
print("no of pages:",len(reader.pages))


# 3. Extract text from the first page.
first_page=reader.pages[0].extract_text()
print("first page:",first_page)


# 4. Extract text from the second page.
second_page=reader.pages[1].extract_text()
print("second page:",second_page)

# 5. Combine text from both pages into one string.
all_text=first_page+second_page
print("all pages:",all_text)

# 6. Check whether NorthStar Maintenance exists in the PDF.
if "NorthStar Maintenance" in all_text:
    print("north star maintenance is present")
else:
    print("north star maintenance is not present")

# 7. Find the number of occurrences of the word vendor .
no_of_times=all_text.lower().count("vendor")
print("no_of_times_the_word_vendor:",no_of_times)

# 8. Save the extracted content into pypdf_output.txt .
with open("pypdf_output.txt","w") as f:
    f.write(all_text)
