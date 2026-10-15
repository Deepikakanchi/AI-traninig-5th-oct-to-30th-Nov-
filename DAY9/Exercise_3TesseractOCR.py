# 1. Open the scanned PDF using PyMuPDF.
import fitz
import pymupdf
doc = pymupdf.open("EY_Scanned_PDF_OCR_Practice.pdf")


# 2. Convert the PDF page into an image.
print(len(doc))
pix=doc[0].get_pixmap()
pix.save("scanned_page.png")
print("pdf page into an image")

# 3. Run Tesseract OCR on the image.
import pytesseract
from PIL import Image
image=Image.open("scanned_page.png")
text=pytesseract.image_to_string(image)
print(text)



# 4. Print the extracted text.
print("the extracted text :",text)


# 5. Check whether Forklift FL-17 was detected.
if "Forklift FL-17" in text:
    print("Forklift FL-17 was detected")
else:
    print("Forklift FL-17 was not detected")


# 6. Search for the word injuries .
if "injuries" in text.lower():
    print("injuries were detected")
else:
    print("injuries were not detected")

# 7. Extract lines mentioning inspection.
for line in text.splitlines():
    if "inspection" in line.lower():
        print(line)

# 8. Save the OCR output into ocr_result.txt .
with open("ocr_result.txt","w") as f:
    f.write(text)


# 9. Count the number of times inspection appears.
count=text.lower().count("inspection")
print(count)

# 10. Print all lines containing Loading Bay .
for line in text.splitlines():
    if "Loading Bay" in line:
        print(line)
