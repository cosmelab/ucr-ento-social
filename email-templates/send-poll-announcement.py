#!/usr/bin/env python3
"""
Send poll announcement email via Gmail API
This script sends HTML email that preserves dark background formatting

Note: If you see "Exam PDF Sender" during authentication, update the OAuth app name:
1. Go to https://console.cloud.google.com/
2. Navigate to APIs & Services → OAuth consent screen
3. Edit app name to "UCR Social Committee Emailer" or similar
"""

import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- CONFIGURATIONS ---
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CREDENTIALS_FILE = "/Users/lucianocosme/Library/CloudStorage/Dropbox/teaching/luciano/email_results/final/luciano.json"
TOKEN_FILE = "/Users/lucianocosme/Library/CloudStorage/Dropbox/teaching/luciano/email_results/final/token.json"
HTML_FILE = "poll-announcement.html"

# Email settings
FROM_EMAIL = "lcosme@ucr.edu"
TO_EMAIL = "luciano.cosme@ucr.edu"  # Updated to UCR email
SUBJECT = "Social Committee Polls - Your Input Needed"

# --- AUTHENTICATE GMAIL API ---
def authenticate_gmail():
    """Authenticate with Gmail API using existing credentials"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

# --- SEND HTML EMAIL ---
def send_html_email(to_email, subject, html_content):
    """Send HTML email via Gmail API"""
    service = build("gmail", "v1", credentials=authenticate_gmail())

    # Create email message
    msg = MIMEMultipart("alternative")
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach HTML content
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    # Convert message to raw format and send
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    message = {"raw": raw_message}

    try:
        service.users().messages().send(userId="me", body=message).execute()
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

# --- MAIN ---
def main():
    # Read HTML file
    if not os.path.exists(HTML_FILE):
        print(f"❌ HTML file not found: {HTML_FILE}")
        print(f"   Current directory: {os.getcwd()}")
        return

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    print(f"📧 Sending poll announcement email...")
    print(f"   From: {FROM_EMAIL}")
    print(f"   To: {TO_EMAIL}")
    print(f"   Subject: {SUBJECT}")
    print()

    # Send email
    success = send_html_email(TO_EMAIL, SUBJECT, html_content)

    if success:
        print()
        print("🎉 Test email sent! Check your inbox at cosme.simple@gmail.com")
        print()
        print("Next steps:")
        print("1. Check if the email has the dark background and correct formatting")
        print("2. If it looks good, you can forward it to the department mailing list")
        print("3. Or send directly to department members by updating TO_EMAIL in this script")

if __name__ == "__main__":
    main()
