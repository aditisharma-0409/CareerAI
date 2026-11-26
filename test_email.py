
from backend.email_service import send_resumes_to_company

# Create a dummy PDF for testing
dummy_pdf = "test_resume.pdf"

pdf_content = b"""%PDF-1.1
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] >>
endobj
trailer
<< /Root 1 0 R >>
%%EOF
"""

with open(dummy_pdf, "wb") as file:
    file.write(pdf_content)

# Enter your own email address for testing
test_email = "aditisharma44405@gmail.com"

resume_files = [
    {
        "file_path": dummy_pdf,
        "file_name": "Test_Resume.pdf"
    }
]

success, message = send_resumes_to_company(
    test_email,
    resume_files
)

print(message)
