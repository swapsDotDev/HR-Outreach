# HR-Outreach
# AutoApply — README

A simple Python tool to send personalized job-application emails with your resume attached to a list of HR contacts.

---

## Features

* Reads contacts from a CSV (`hr_list.csv`) with headers: `Name,Email,Title,Company`.
* Personalizes greeting with the contact's first name and company.
* Attaches your resume (PDF/DOCX) to each email.
* Stores configuration and secrets in a `.env` file.
* Logs send results to `sent_log.csv` (timestamp, name, email, company, status, info).
* Adds a short, randomized delay between sends to reduce deliverability risk.

---

## Quick Start (Windows)

1. Clone or copy the project to a folder, e.g. `E:\Swappy\Projects\hrEmail`.

2. Open PowerShell in that folder.

3. (Optional but recommended) Create a virtual environment:

```powershell
python -m venv .venv
```

4. Allow script activation for the current session and activate venv:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\.venv\Scripts\Activate.ps1
```

> Or use Command Prompt activation:
>
> ```cmd
> .\.venv\Scripts\activate.bat
> ```

5. Install required package(s):

```powershell
pip install python-dotenv
```

6. Prepare files in the project folder:

* `send_personalized_resumes.py` (script)
* `hr_list.csv` (contacts)
* `resume_swapnil.pdf` (or whatever your resume file is named)
* `.env` (configuration file — see example below)

7. Run the script:

```powershell
python send_personalized_resumes.py
```

---

## `.env` example

Create a file named `.env` in the project folder and add the following (replace values):

```
SENDER_NAME=Swapnil Kale
SENDER_EMAIL=swapnilkale2002@gmail.com
SENDER_PASSWORD=your_app_password_here

RESUME_PATH=resume_swapnil.pdf
HR_CSV=hr_list.csv
LOG_CSV=sent_log.csv

SUBJECT=Application: MERN / Full Stack - Entry Level

MOBILE_NUMBER=+91-XXXXXXXXXX
LINKDIN_URL=https://www.linkedin.com/in/your-profile
```

**Important:** Do not share or commit `.env` to a public repo. Add `.env` to `.gitignore`.

---

## `hr_list.csv` format example

CSV header must be present. If any field contains commas, wrap that field in double quotes.

```csv
Name,Email,Title,Company
Akanksha Puri,akanksha.puri@sourcefuse.com,Associate Director HR,SourceFuse Technologies
Nikhil Mooley,nikhil.m@purplle.com,"Head Of Human Resources, L&D",Purplle
```

Notes:

* The script reads `Name`, `Email`, and `Company` fields. `Title` is optional and not used in the default template.
* If your CSV is messy, open it in Excel and export as CSV (Excel will quote fields with commas automatically).

---

## Gmail / SMTP notes

* For Gmail, enable 2-Step Verification and create an **App Password** at [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords). Use that App Password in `SENDER_PASSWORD`.
* SMTP config in the script uses:

  * Server: `smtp.gmail.com`
  * Port: `587` (STARTTLS)

**Limits & best practices:**

* Gmail imposes daily sending limits (personal accounts have limits around a few hundred messages/day). Avoid sending thousands from a single account.
* Send in small batches and avoid long consecutive runs to reduce spam risk.

---

## Logs

After running, `sent_log.csv` will be created/appended with rows:

```
timestamp,name,email,company,status,info
```

Use this file to filter failed addresses and retry later.

---

## Customization ideas

* Use an HTML email template and provide a plain-text fallback.
* Read contacts from Excel (.xlsx) using `pandas`.
* Add per-contact custom fields (e.g., `project_name`, `custom_note`) and extend the template.
* Use an email API provider (SendGrid, Mailgun, Amazon SES) for higher throughput and better deliverability.

---

## Troubleshooting

**`smtplib.SMTPAuthenticationError`**

* Check `SENDER_EMAIL` and `SENDER_PASSWORD`. For Gmail, use App Password.
* Make sure 2FA is enabled and the App Password is active.

**`FileNotFoundError` for resume or CSV**

* Ensure `RESUME_PATH` and `HR_CSV` match filenames in the project folder.

**PowerShell: activation or execution policy errors**

* Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force` in the session before activating.
* Or use `activate.bat` in Command Prompt.

**Emails show only address (no display name)**

* Ensure `.env` `SENDER_NAME` is set. The script uses `From: "Swapnil Kale <email>"` header.
* Gmail may sometimes override the display name to what’s configured in your Gmail account settings.

---

## Security & etiquette

* Never hard-code passwords in your script. Keep them in the `.env` file.
* Don’t send unsolicited spam. Personalize messages and respect recipients.
* Consider adding an unsubscribe footer if sending at scale.

---

## License

This project is provided as-is for personal use. Feel free to copy, modify, and use it for your job outreach.

---

## Contact

If you want help customizing templates, adding HTML, or batching logic, reach out by updating the script or open an issue in your repo.
