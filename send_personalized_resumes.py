import csv
import smtplib
import time
import random
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Load config from .env
SENDER_NAME = os.getenv("SENDER_NAME")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

RESUME_PATH = os.getenv("RESUME_PATH")
HR_CSV = os.getenv("HR_CSV")
LOG_CSV = os.getenv("LOG_CSV")
SUBJECT = os.getenv("SUBJECT")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Email body with placeholders
MOBILE = os.getenv("MOBILE_NUMBER")
LINKDIN_URL = os.getenv("LINKDIN_URL")

BODY_TEMPLATE = f"""Dear {{first_name}},

I hope you're doing well.

I'm writing to check if {{company}} has any openings for an entry-level Software Developer or MERN Stack role. I've been working with React, Node, Express, MongoDB, Python, and have built a few full-stack projects to gain hands-on experience.

My resume is attached below. If my profile seems like a fit for anything you're hiring for, I'd really appreciate it if you could take a look or forward it to the right team.

Thank you for your time.

Best regards,
Swapnil Kale
Phone: {MOBILE}
Email: {SENDER_EMAIL}
LinkedIn: {LINKDIN_URL}
"""


DELAY_MEAN = 5
DELAY_JITTER = 3


def first_name(name):
    return name.split()[0] if name else "Hiring Manager"


def read_hr_csv(csv_file):
    contacts = []
    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append({
                "name": row.get("Name", "").strip(),
                "email": row.get("Email", "").strip(),
                "company": row.get("Company", "").strip()
            })
    return contacts


def create_message(to_email, contact):
    msg = MIMEMultipart()
    msg["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg["To"] = to_email
    msg["Subject"] = SUBJECT

    body = BODY_TEMPLATE.format(
        first_name=first_name(contact["name"]),
        company=contact["company"] or "your organization"
    )
    msg.attach(MIMEText(body, "plain"))

    # Attach resume
    with open(RESUME_PATH, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{os.path.basename(RESUME_PATH)}"'
    )
    msg.attach(part)

    return msg


def append_log(contact, status, info=""):
    exists = os.path.exists(LOG_CSV)
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "name", "email", "company", "status", "info"])

        writer.writerow([
            datetime.utcnow().isoformat(),
            contact["name"],
            contact["email"],
            contact["company"],
            status,
            info
        ])


def send_all():
    contacts = read_hr_csv(HR_CSV)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    print("✔ Logged in successfully.\n")

    for i, contact in enumerate(contacts, start=1):
        email = contact["email"]

        try:
            msg = create_message(email, contact)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print(f"[{i}/{len(contacts)}] ✔ Sent to {email}")
            append_log(contact, "SENT")
        except Exception as e:
            print(f"[{i}/{len(contacts)}] ❌ Failed for {email}: {e}")
            append_log(contact, "FAILED", str(e))

        time.sleep(max(1, random.gauss(DELAY_MEAN, DELAY_JITTER)))

    server.quit()
    print("\n🎉 All emails processed. Check log file:", LOG_CSV)


if __name__ == "__main__":
    send_all()
