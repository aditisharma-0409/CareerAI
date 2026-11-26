from resume_parser import extract_resume_text

pdf_path = "sample_resume.pdf"

text = extract_resume_text(pdf_path)

print(text)