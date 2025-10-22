#!/usr/bin/env python3
"""
Send coffee hour announcement email via Gmail API
This script sends the Halloween Coffee Hour invitation with perfect HTML formatting

Usage:
    cd /Users/lucianocosme/Projects/ucr-ento-social/email-templates
    /opt/homebrew/Caskroom/miniforge/base/bin/python3 send-coffee-hour-announcement.py
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
HTML_FILE = "coffee-hour-announcement.html"

# Email settings
FROM_EMAIL = "lcosme@ucr.edu"
TO_EMAIL = "pol.sarkar@ucr.edu"  # Pol will forward to department
CC_EMAILS = "cosme.simple@gmail.com, lcosme@gmail.com, andrelut@ucr.edu, mtana016@ucr.edu"  # Social Committee members
SUBJECT = "You're Invited: Spooktacular Coffee Hour - Oct 31st"

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
def send_html_email(to_email, subject, html_content, cc_emails=None):
    """Send HTML email via Gmail API with optional CC"""
    service = build("gmail", "v1", credentials=authenticate_gmail())

    # Create email message
    msg = MIMEMultipart("alternative")
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    if cc_emails:
        msg["Cc"] = cc_emails
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
        if cc_emails:
            print(f"   CC: {cc_emails}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

# --- MAIN ---
def main():
    print("=" * 70)
    print("  Spooktacular Coffee Hour Email Sender")
    print("=" * 70)
    print()

    # Read HTML file
    if not os.path.exists(HTML_FILE):
        print(f"❌ HTML file not found: {HTML_FILE}")
        print(f"   Current directory: {os.getcwd()}")
        print()
        print("Make sure you're in the email-templates directory:")
        print("   cd /Users/lucianocosme/Projects/ucr-ento-social/email-templates")
        return

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    print(f"📧 Sending coffee hour announcement...")
    print(f"   From: {FROM_EMAIL}")
    print(f"   To: {TO_EMAIL}")
    print(f"   CC: {CC_EMAILS}")
    print(f"   Subject: {SUBJECT}")
    print()

    # Send email
    success = send_html_email(TO_EMAIL, SUBJECT, html_content, CC_EMAILS)

    if success:
        print()
        print("=" * 70)
        print("🎉 Success! Coffee hour invitation sent!")
        print("=" * 70)
        print()
        print(f"Check your inbox at {TO_EMAIL}")
        print()
        print("Next steps:")
        print("  1. Open the email and verify it looks good")
        print("  2. Check that the flyer image displays correctly")
        print("  3. Verify all links work (events page, website, contact)")
        print("  4. If everything looks perfect, update TO_EMAIL to send to:")
        print("     - Department mailing list")
        print("     - Or individual recipients")
        print()
        print("To send to multiple people, edit line 24 in this script:")
        print('  TO_EMAIL = "person1@ucr.edu, person2@ucr.edu"')
        print()

if __name__ == "__main__":
    main()
