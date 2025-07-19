# utils/document_utils.py

import requests
import fitz  # PyMuPDF

def extract_text_from_pdf_url(pdf_url):
    """
    Downloads a PDF from a URL and extracts its full text using PyMuPDF.
    No local file is saved.

    Args:
        pdf_url (str): URL to the PDF file.

    Returns:
        str: Extracted plain text from the PDF.
    """
    try:
        response = requests.get(pdf_url)
        if response.status_code != 200:
            print(f"Failed to fetch PDF: {pdf_url}")
            return ""

        # Use in-memory byte stream to open PDF directly
        doc = fitz.open(stream=response.content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""
