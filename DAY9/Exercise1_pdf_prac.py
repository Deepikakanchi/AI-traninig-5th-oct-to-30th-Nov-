# 1. Open the PDF.
import fitz
doc = fitz.open("EY_Digital_PDF_Practice.pdf")
print("pdf opened")
import pymupdf
document=pymupdf.open("EY_Digital_PDF_Practice.pdf")
print("pdf opened with pymupdf")


# 2. Print the number of pages.
print("the number of pages:",len(doc))


# 3. Extract and print text from page 1.
page1_text=doc[0].get_text()
print("page1_text:",page1_text)
page2_text=doc[1].get_text()
print("page2_text:",page2_text)


# 4. Extract text from all pages.
all_text=""
for page in doc:
    all_text+=page.get_text()
print("text from all pages:",all_text)

# 5. Search whether the word maintenance appears.
if "maintenance" in all_text:
    print("maintenance is appeared")
else:
    print("maintenance is NOT appeared")


# 6. Count how many times V303 appears.
count=all_text.count("V303")
print("v303 appeared:",count,"times")

# 7. Extract only page 2 text.
page2text=doc[1].get_text()
print("page2text:",page2text)

# 8. Save all extracted text into digital_pdf_text.txt .
with open("digital_pdf_text.txt","w") as f:
    f.write(all_text)
