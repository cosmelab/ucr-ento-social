#!/usr/bin/env python3
"""
Create .eml file for poll announcement
Double-click the .eml file to open it in Mail.app, then send
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Read HTML file
html_file = "poll-announcement.html"
output_file = "poll-announcement.eml"

print(f"📧 Creating email file from {html_file}...")

with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

# Create email message
msg = MIMEMultipart("alternative")
msg["From"] = "lcosme@ucr.edu"
msg["To"] = "cosme.simple@gmail.com"  # Change this to your test email
msg["Subject"] = "Social Committee Polls - Your Input Needed"

# Attach HTML content
html_part = MIMEText(html_content, "html", "utf-8")
msg.attach(html_part)

# Write to .eml file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(msg.as_string())

print(f"✅ Created {output_file}")
print()
print("Next steps:")
print(f"1. Double-click '{output_file}' to open it in Mail.app")
print("2. The email will open with the HTML formatting preserved")
print("3. Update the recipient if needed, then click Send")
print()
print("If you want to send to the mailing list:")
print("- Change the 'To' address in this script")
print("- Run the script again to generate a new .eml file")
