#!/usr/bin/env python3
"""
Download Google Sheets data to CSV using OAuth credentials (same as email scripts)
"""

import os
import json
import csv
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OAuth credentials for UCR Entomology Social Committee project
# Project ID: ucr-ento-social
# Client ID: 669189357521-bsceob8p9koi5snd4v9lkdk038tl88vm.apps.googleusercontent.com
# Credentials stored at: polls/credentials.json (in .gitignore)
# Token stored at: polls/token_sheets.json (in .gitignore)
CREDENTIALS_FILE = "polls/credentials.json"
TOKEN_FILE = "polls/token_sheets.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate_sheets():
    """Authenticate with Google Sheets API using existing OAuth credentials"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        print("Authenticating with Google Sheets...")
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds

def download_sheet_to_csv(sheet_id, output_path):
    """Download a Google Sheet to CSV"""
    try:
        creds = authenticate_sheets()
        service = build('sheets', 'v4', credentials=creds)

        # Get all data from the sheet
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range='A:Z').execute()
        values = result.get('values', [])

        if not values:
            print(f"  ✗ No data found in sheet")
            return False

        # Write to CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(values)

        print(f"  ✓ Downloaded {len(values)-1} responses to {output_path}")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    polls_dir = Path("/Users/lucianocosme/Projects/ucr-ento-social/polls")

    # Sheet mappings: (sheet_id, output_filename)
    sheets = {
        "Coffee Hours Poll": ("1tk7wZq2Dtn1hiqdS1e4_s6QELMp0GjZZskl9n4XrnHc", "coffee_hour_poll_responses.csv"),
        "Events Poll": ("155M7Lwj5cehBWV0_qSamorFlA53l3psgXwB5WbnOgxU", "events_poll_responses.csv"),
        "3D Print Poll": ("1JnP38azOm1ipd5aJ1qaXKz_-6ea7T9KoPYXXoEkHfb0", "3d_merch_poll_responses.csv")
    }

    print("="*70)
    print("DOWNLOADING GOOGLE SHEETS TO CSV")
    print("="*70)
    print()

    success_count = 0
    fail_count = 0

    for poll_name, (sheet_id, output_csv) in sheets.items():
        print(f"Processing: {poll_name}")
        output_path = polls_dir / output_csv

        if download_sheet_to_csv(sheet_id, output_path):
            success_count += 1
        else:
            fail_count += 1
        print()

    print("="*70)
    print(f"DOWNLOAD COMPLETE: {success_count} succeeded, {fail_count} failed")
    print("="*70)

    if success_count > 0:
        print("\nNext steps:")
        print("  Run analysis scripts:")
        print(f"    /opt/homebrew/Caskroom/miniforge/base/bin/python3 polls/analyze_coffee_hour_poll.py polls/coffee_hour_poll_responses.csv")
        print(f"    /opt/homebrew/Caskroom/miniforge/base/bin/python3 polls/analyze_events_poll.py polls/events_poll_responses.csv")
        print(f"    /opt/homebrew/Caskroom/miniforge/base/bin/python3 polls/analyze_3d_merch_poll.py polls/3d_merch_poll_responses.csv")

if __name__ == "__main__":
    main()
