import os
import pdfplumber
from pathlib import Path

PDF_DIR = "./pdfs"

pdf_files = list(Path(PDF_DIR).glob("*.pdf"))
print(f"PDFs found: {len(pdf_files)}")
print()

for pdf_path in pdf_files:
    print(f"── {pdf_path.name} ──")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"   Pages     : {len(pdf.pages)}")
            text = pdf.pages[0].extract_text()
            print(f"   Page 1 text: {repr(text[:120]) if text else 'None / Empty'}")
    except Exception as e:
        print(f"   ERROR: {e}")
    print()