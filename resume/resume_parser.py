# ==========================================
# Resume Parser
# Reads text from PDF Resume
# ==========================================

import fitz


def extract_resume_text(pdf_path):
    """
    Reads a PDF file and returns all text.
    """

    text = ""

    try:

        pdf = fitz.open(pdf_path)

        for page in pdf:

            text += page.get_text()

        pdf.close()

        return text

    except Exception as e:

        print("Error:", e)

        return None