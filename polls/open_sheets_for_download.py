#!/usr/bin/env python3
"""
Open Google Sheets in browser for manual CSV download
"""

import webbrowser
import json
from pathlib import Path
import time

def read_sheet_id(gsheet_path):
    """Read .gsheet file and extract document ID"""
    try:
        with open(gsheet_path, 'r') as f:
            data = json.load(f)
            return data.get('doc_id')
    except Exception as e:
        print(f"Error reading {gsheet_path}: {e}")
        return None

def main():
    google_drive_dir = Path("/Users/lucianocosme/My Drive/social_committee")
    polls_dir = Path("/Users/lucianocosme/Projects/ucr-ento-social/polls")

    # Sheet mappings
    sheets = {
        "Coffee Hours Poll": ("coffee_hours.gsheet", "coffee_hour_poll_responses.csv"),
        "Events Poll": ("events_poll.gsheet", "events_poll_responses.csv"),
        "3D Print Poll": ("3D-print_poll.gsheet", "3d_merch_poll_responses.csv")
    }

    print("="*70)
    print("OPENING GOOGLE SHEETS FOR DOWNLOAD")
    print("="*70)
    print()
    print("Instructions:")
    print("  1. Each sheet will open in your browser")
    print("  2. Click: File → Download → Comma Separated Values (.csv)")
    print(f"  3. Save to: {polls_dir}/")
    print("  4. Use these exact filenames:")
    print()

    for poll_name, (gsheet_file, output_csv) in sheets.items():
        gsheet_path = google_drive_dir / gsheet_file
        sheet_id = read_sheet_id(gsheet_path)

        if not sheet_id:
            print(f"  ✗ Could not read {poll_name}")
            continue

        print(f"  - {output_csv}")

        # Open in browser
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        webbrowser.open(url)
        time.sleep(1)  # Small delay between opening tabs

    print()
    print("="*70)
    print("After downloading all 3 CSV files, run:")
    print("  /opt/homebrew/Caskroom/miniforge/base/bin/python3 polls/analyze_all_polls.py")
    print("="*70)

if __name__ == "__main__":
    main()
