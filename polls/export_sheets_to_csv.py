#!/usr/bin/env python3
"""
Export Google Sheets poll data to CSV files for analysis
Reads .gsheet files from Google Drive folder and exports to CSV
"""

import json
import csv
import sys
from pathlib import Path

def read_gsheet_file(gsheet_path):
    """Read .gsheet file and extract document ID"""
    try:
        with open(gsheet_path, 'r') as f:
            data = json.load(f)
            return data.get('doc_id')
    except Exception as e:
        print(f"Error reading {gsheet_path}: {e}")
        return None

def export_sheet_to_csv(doc_id, output_csv):
    """
    Export Google Sheet to CSV using public export URL
    Note: This requires the sheet to be publicly accessible or shared
    """
    import urllib.request
    import urllib.error

    # Google Sheets CSV export URL
    export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv"

    try:
        print(f"Downloading from Google Sheets...")
        print(f"  Sheet ID: {doc_id}")
        print(f"  Output: {output_csv}")

        with urllib.request.urlopen(export_url) as response:
            csv_data = response.read().decode('utf-8')

        with open(output_csv, 'w', encoding='utf-8') as f:
            f.write(csv_data)

        # Count rows
        row_count = len(csv_data.strip().split('\n')) - 1  # -1 for header
        print(f"  ✓ Exported {row_count} responses\n")
        return True

    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"  ✗ Error: Sheet is private. Please make it publicly viewable or shared with link access.")
            print(f"    To fix: Open the sheet → Share → Change to 'Anyone with the link can view'\n")
        else:
            print(f"  ✗ HTTP Error {e.code}: {e.reason}\n")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        return False

def main():
    """Main export function"""
    google_drive_dir = Path("/Users/lucianocosme/My Drive/social_committee")
    polls_dir = Path("/Users/lucianocosme/Projects/ucr-ento-social/polls")

    # Define sheet mappings: .gsheet file -> output CSV name
    sheet_mappings = {
        "coffee_hours.gsheet": "coffee_hour_poll_responses.csv",
        "events_poll.gsheet": "events_poll_responses.csv",
        "3D-print_poll.gsheet": "3d_merch_poll_responses.csv"
    }

    print("="*70)
    print("EXPORTING GOOGLE SHEETS TO CSV")
    print("="*70)
    print()

    success_count = 0
    fail_count = 0

    for gsheet_file, output_csv in sheet_mappings.items():
        gsheet_path = google_drive_dir / gsheet_file
        output_path = polls_dir / output_csv

        print(f"Processing: {gsheet_file}")

        # Read document ID from .gsheet file
        doc_id = read_gsheet_file(gsheet_path)
        if not doc_id:
            print(f"  ✗ Could not read document ID\n")
            fail_count += 1
            continue

        # Export to CSV
        if export_sheet_to_csv(doc_id, output_path):
            success_count += 1
        else:
            fail_count += 1

    print("="*70)
    print(f"EXPORT COMPLETE: {success_count} succeeded, {fail_count} failed")
    print("="*70)

    if success_count > 0:
        print("\nNext steps:")
        print("  1. Run analysis scripts:")
        print(f"     python polls/analyze_coffee_hour_poll.py polls/coffee_hour_poll_responses.csv")
        print(f"     python polls/analyze_events_poll.py polls/events_poll_responses.csv")
        print(f"     python polls/analyze_3d_merch_poll.py polls/3d_merch_poll_responses.csv")
        print("  2. Review generated charts in analysis_charts_* folders")
        print("  3. Create HTML results page with insights")

    if fail_count > 0:
        print("\n⚠ Some sheets failed to export. Check that they are:")
        print("  - Shared with 'Anyone with the link can view' permission")
        print("  - Or publicly accessible")
        sys.exit(1)

if __name__ == "__main__":
    main()
