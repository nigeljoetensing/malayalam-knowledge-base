import pytesseract
from pdf2image import convert_from_path
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_path = list(Path("./pdfs").glob("*.pdf"))[0]
print(f"Testing: {pdf_path.name}")

images = convert_from_path(str(pdf_path), dpi=300)
text = pytesseract.image_to_string(images[0], lang="mal+eng")

print(f"Characters extracted: {len(text)}")
print(f"Preview: {text[:300]}")