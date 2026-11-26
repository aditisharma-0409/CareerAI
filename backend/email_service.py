import html
import os
import smtplib
import socket

from dotenv import load_dotenv
from email.message import EmailMessage
from email.utils import parseaddr

load_dotenv()


class IPv4SMTP_SSL(smtplib.SMTP_SSL):

    def _get_socket(self, host, port, timeout):
        ipv4_address = socket.gethostbyname(host)

        sock = socket.create_connection(
            (ipv4_address, port),
            timeout,
            self.source_address
        )

        return self.context.wrap_socket(
            sock,
            server_hostname=host
        )


def _get_smtp_credentials():
    sender_email = os.getenv("CAREERAI_EMAIL", "").strip()
    sender_password = (
        os.getenv("CAREERAI_EMAIL_PASSWORD", "")
        .replace(" ", "")
        .strip()
    )
    return sender_email, sender_password


def _is_valid_email(email_address):
    recipient = (email_address or "").strip()
    _, parsed_email = parseaddr(recipient)
    return bool(parsed_email and parsed_email == recipient and "@" in parsed_email)


# ==========================================================
# WORKFLOW 1: DIRECT RESUME SHARING WITH COMPANY HR
# ==========================================================

def send_resumes_to_company(hr_email, resume_files):

    sender_email, sender_password = _get_smtp_credentials()

    if not sender_email or not sender_password:
        return False, "Email credentials are not configured."

    recipient = (hr_email or "").strip()
    if not _is_valid_email(recipient):
        return False, "Please enter a valid HR email address."

    if not resume_files:
        return False, "No resumes were selected."

    message = EmailMessage()
    message["Subject"] = "Student Resumes - Placement Drive"
    message["From"] = sender_email
    message["To"] = recipient

    message.set_content(
        "Dear HR Team,\n\n"
        "Please find attached the selected student resumes "
        "for your placement drive.\n\n"
        "Regards,\nTraining and Placement Cell\nDAV University, Jalandhar"
    )

    for resume in resume_files:

        file_path = resume.get("file_path")
        file_name = os.path.basename(resume.get("file_name") or "")

        if not file_path or not os.path.isfile(file_path):
            return False, f"Resume file not found: {file_name or 'Unknown file'}"

        if not file_name.lower().endswith(".pdf"):
            return False, f"Only PDF resumes can be emailed: {file_name}"

        with open(file_path, "rb") as file:
            message.add_attachment(
                file.read(),
                maintype="application",
                subtype="pdf",
                filename=resume["file_name"]
            )

    try:
        with IPv4SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=30
        ) as smtp:

            smtp.login(sender_email, sender_password)
            smtp.send_message(message)

        return True, "Resumes sent successfully."

    except Exception as error:
        return False, f"Email sending failed: {error}"


# ==========================================================
# WORKFLOW 2: PLACEMENT DRIVE NOTIFICATIONS TO STUDENTS
# ==========================================================

def _build_placement_email_bodies(student_name, drive_details):
    company_name = str(drive_details.get("company_name") or "Recruiting Company")
    job_role = str(drive_details.get("job_role") or "Open Position")
    package = str(drive_details.get("package") or "As per company norms")
    location = str(drive_details.get("location") or "To be announced")
    criteria = str(drive_details.get("eligibility_criteria") or "As per placement drive criteria")
    deadline = str(drive_details.get("application_deadline") or "Apply as soon as possible")
    drive_name = str(drive_details.get("drive_name") or f"{company_name} Placement Drive")
    greeting_name = (student_name or "Student").strip()

    plain_text = (
        f"Dear {greeting_name},\n\n"
        "Greetings from DAV University, Jalandhar!\n\n"
        f"We are pleased to inform you that {company_name} is conducting a placement drive "
        f"({drive_name}) for the position of {job_role}.\n"
        "Based on the eligibility criteria provided by the company, you have been identified "
        "as eligible for this opportunity.\n\n"
        "Placement Details:\n"
        f"- Company Name: {company_name}\n"
        f"- Position: {job_role}\n"
        f"- Package: {package}\n"
        f"- Job Location: {location}\n"
        f"- Eligibility Criteria: {criteria}\n"
        f"- Application Deadline: {deadline}\n\n"
        "Interested students are requested to review the placement details and apply through "
        "the CareerAI Student Portal before the deadline.\n\n"
        "Best wishes for your placement journey!\n\n"
        "Regards,\n"
        "Training and Placement Cell\n"
        "DAV University, Jalandhar"
    )

    e_name = html.escape(greeting_name)
    e_company = html.escape(company_name)
    e_role = html.escape(job_role)
    e_package = html.escape(package)
    e_location = html.escape(location)
    e_criteria = html.escape(criteria)
    e_deadline = html.escape(deadline)
    e_drive = html.escape(drive_name)

    html_body = f"""\
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
</head>
<body style="margin:0; padding:0; background-color:#F4F6FA; font-family:'Segoe UI', Arial, sans-serif; color:#0F172A;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#F4F6FA; padding:24px 0;">
    <tr>
      <td align="center">
        <table width="620" cellpadding="0" cellspacing="0" style="background-color:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; overflow:hidden;">
          <!-- Header -->
          <tr>
            <td style="background-color:#0F2A56; padding:22px 28px; border-bottom:4px solid #C89B3C;">
              <div style="font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase; color:#E5C77B;">
                DAV University, Jalandhar
              </div>
              <div style="font-size:20px; font-weight:700; color:#FFFFFF; margin-top:4px;">
                Training and Placement Cell
              </div>
              <div style="font-size:13px; color:#CBD5E1; margin-top:2px;">
                Official Campus Placement Drive Announcement
              </div>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:26px 28px; font-size:14px; line-height:1.6; color:#334155;">
              <p style="margin-top:0;">Dear <strong>{e_name}</strong>,</p>
              <p>Greetings from <strong>DAV University, Jalandhar</strong>!</p>
              <p>
                We are pleased to inform you that <strong>{e_company}</strong> is conducting a placement drive
                (<strong>{e_drive}</strong>) for the position of <strong>{e_role}</strong>.
                Based on the eligibility criteria provided by the company, you have been identified as
                <strong>eligible</strong> for this opportunity.
              </p>

              <!-- Details Table -->
              <table width="100%" cellpadding="10" cellspacing="0" style="border-collapse:collapse; margin:18px 0; border:1px solid #E2E8F0; border-radius:6px;">
                <tr style="background-color:#F8FAFC;">
                  <td width="38%" style="font-weight:700; color:#0F2A56; border-bottom:1px solid #E2E8F0;">Company Name</td>
                  <td style="border-bottom:1px solid #E2E8F0;">{e_company}</td>
                </tr>
                <tr>
                  <td style="font-weight:700; color:#0F2A56; border-bottom:1px solid #E2E8F0;">Position / Job Role</td>
                  <td style="border-bottom:1px solid #E2E8F0;">{e_role}</td>
                </tr>
                <tr style="background-color:#F8FAFC;">
                  <td style="font-weight:700; color:#0F2A56; border-bottom:1px solid #E2E8F0;">Package</td>
                  <td style="border-bottom:1px solid #E2E8F0;">{e_package}</td>
                </tr>
                <tr>
                  <td style="font-weight:700; color:#0F2A56; border-bottom:1px solid #E2E8F0;">Job Location</td>
                  <td style="border-bottom:1px solid #E2E8F0;">{e_location}</td>
                </tr>
                <tr style="background-color:#F8FAFC;">
                  <td style="font-weight:700; color:#0F2A56; border-bottom:1px solid #E2E8F0;">Eligibility Criteria</td>
                  <td style="border-bottom:1px solid #E2E8F0;">{e_criteria}</td>
                </tr>
                <tr>
                  <td style="font-weight:700; color:#0F2A56;">Application Deadline</td>
                  <td style="font-weight:600; color:#9A6F18;">{e_deadline}</td>
                </tr>
              </table>

              <p>
                Interested students are requested to log in to the <strong>CareerAI Student Portal</strong>,
                review the complete drive details, and submit their application before the deadline.
              </p>

              <p style="margin-bottom:0;">
                Best wishes for your placement journey!<br><br>
                <strong>Regards,</strong><br>
                Training and Placement Cell<br>
                DAV University, Jalandhar
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color:#F8FAFC; padding:14px 28px; border-top:1px solid #E2E8F0; font-size:12px; color:#64748B; text-align:center;">
              This is an official placement notification sent via CareerAI — DAV University Placement Management Portal.
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    return plain_text, html_body


def send_placement_drive_notifications(recipients, drive_details):
    """
    Send official DAV University placement drive announcement emails
    to selected eligible students.

    Parameters:
        recipients: list of dicts with keys 'user_id', 'student_name', 'email'
        drive_details: dict with keys 'company_name', 'drive_name', 'job_role',
                       'package', 'location', 'eligibility_criteria', 'application_deadline'

    Returns:
        dict: {
            "sent": [recipient_dict, ...],
            "failed": [{"recipient": recipient_dict, "reason": str}, ...],
            "error": str or None
        }
    """
    sender_email, sender_password = _get_smtp_credentials()

    if not sender_email or not sender_password:
        return {
            "sent": [],
            "failed": [],
            "error": "Email credentials are not configured in environment variables.",
        }

    if not recipients:
        return {
            "sent": [],
            "failed": [],
            "error": "No eligible students were selected.",
        }

    company_name = str(drive_details.get("company_name") or "Recruiting Company")
    job_role = str(drive_details.get("job_role") or "Open Position")
    subject = f"Placement Opportunity – {company_name} | {job_role} | DAV University"

    sent = []
    failed = []

    try:
        with IPv4SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
            smtp.login(sender_email, sender_password)

            for student in recipients:
                recipient_email = (student.get("email") or "").strip()
                student_name = student.get("student_name") or "Student"

                if not _is_valid_email(recipient_email):
                    failed.append(
                        {"recipient": student, "reason": "Invalid email address"}
                    )
                    continue

                plain_text, html_body = _build_placement_email_bodies(
                    student_name, drive_details
                )

                message = EmailMessage()
                message["Subject"] = subject
                message["From"] = f"DAV University Placement Cell <{sender_email}>"
                message["To"] = recipient_email
                message.set_content(plain_text)
                message.add_alternative(html_body, subtype="html")

                try:
                    smtp.send_message(message)
                    sent.append(student)
                except Exception as send_error:
                    failed.append(
                        {"recipient": student, "reason": str(send_error)}
                    )

        return {"sent": sent, "failed": failed, "error": None}

    except Exception as smtp_error:
        return {
            "sent": sent,
            "failed": failed,
            "error": f"SMTP connection failed: {smtp_error}",
        }