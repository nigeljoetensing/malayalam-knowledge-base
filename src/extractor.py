import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_digital(pdf_path: str) -> list[dict]:
    """Extract text from digital (text-layer) PDFs."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and len(text.strip()) > 30:
                pages.append({
                    "page_num": i + 1,
                    "text":     text.strip(),
                    "source":   Path(pdf_path).name
                })
    return pages


def extract_text_ocr(pdf_path: str, lang: str = "mal+eng") -> list[dict]:
    """OCR extraction for scanned Malayalam PDFs."""
    pages = []
    try:
        images = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=r"C:\poppler-25.12.0\Library\bin"
        )
    except Exception as e:
        print(f"   [pdf2image error] {e}")
        print("   Make sure poppler is installed — see Step 5 below")
        return []

    for i, image in enumerate(images):
        try:
            text = pytesseract.image_to_string(image, lang=lang)
            if text and len(text.strip()) > 10:
                pages.append({
                    "page_num": i + 1,
                    "text":     text.strip(),
                    "source":   Path(pdf_path).name
                })
            else:
                print(f"   [OCR warning] Page {i+1} returned no text")
        except Exception as e:
            print(f"   [OCR error] Page {i+1}: {e}")
    return pages


def extract_pdf(pdf_path: str) -> list[dict]:
    """
    Auto-detect digital vs scanned.
    For single-page PDFs — if page 1 has no text, go straight to OCR.
    """
    digital_pages = extract_text_digital(pdf_path)

    if digital_pages:
        print(f"   [Digital] {len(digital_pages)} pages extracted")
        return digital_pages

    # No text found — use OCR
    print(f"   [OCR] No text layer — running Tesseract (mal+eng)")
    return extract_text_ocr(pdf_path)