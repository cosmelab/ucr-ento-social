#!/usr/bin/env python3
"""
UCR Entomology Social Committee - Events Poll Analysis Script
Analyzes CSV data exported from Google Sheets events poll responses
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data(csv_file):
    """Load poll data from CSV file"""
    try:
        df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(df)} responses")
        return df
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def split_multiselect(df, column):
    """Split comma-separated values into individual items and count them"""
    if column not in df.columns:
        return pd.Series()

    # Split comma-separated values and flatten
    all_items = []
    for value in df[column].dropna():
        items = [item.strip() for item in str(value).split(',')]
        all_items.extend(items)

    # Count occurrences
    counts = pd.Series(all_items).value_counts()
    return counts

def print_summary(df):
    """Print summary statistics"""
    print("\n" + "="*60)
    print("EVENTS POLL SUMMARY")
    print("="*60)
    print(f"Total Responses: {len(df)}")
    if 'Timestamp' in df.columns:
        print(f"Date Range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
    print("\n")

def analyze_multiselect_column(df, column, title):
    """Analyze and display results for multi-select questions"""
    print(f"\n{title}")
    print("-" * 60)

    counts = split_multiselect(df, column)
    total = len(df)

    if len(counts) == 0:
        print("  (No data)")
        return None

    for item, count in counts.items():
        percentage = (count / total) * 100
        bar = "█" * int(percentage / 2)
        print(f"{item:<40} {count:>3} ({percentage:>5.1f}%) {bar}")

    return counts

def analyze_singleselect_column(df, column, title):
    """Analyze and display results for single-select questions"""
    print(f"\n{title}")
    print("-" * 60)

    if column not in df.columns:
        print("  (No data)")
        return None

    counts = df[column].value_counts()
    total = len(df)

    for item, count in counts.items():
        percentage = (count / total) * 100
        bar = "█" * int(percentage / 2)
        print(f"{item:<40} {count:>3} ({percentage:>5.1f}%) {bar}")

    return counts

def create_visualizations(df, output_dir="analysis_charts_events"):
    """Create visualization charts"""
    Path(output_dir).mkdir(exist_ok=True)
    print(f"\n\nGenerating charts in '{output_dir}/' folder...")

    # 1. Event Frequency
    if 'Event Frequency' in df.columns:
        plt.figure(figsize=(10, 6))
        freq_counts = df['Event Frequency'].value_counts()
        freq_counts.plot(kind='barh', color='steelblue')
        plt.title('Preferred Event Frequency', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/event_frequency.png', dpi=300, bbox_inches='tight')
        print("  ✓ event_frequency.png")
        plt.close()

    # 2. Event Budget
    if 'Event Budget' in df.columns:
        plt.figure(figsize=(10, 6))
        budget_counts = df['Event Budget'].value_counts()
        budget_counts.plot(kind='barh', color='green')
        plt.title('Event Budget Willingness', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/event_budget.png', dpi=300, bbox_inches='tight')
        print("  ✓ event_budget.png")
        plt.close()

    # 3. Top On-Campus Events
    plt.figure(figsize=(12, 8))
    oncampus_social = split_multiselect(df, 'On-Campus Social Events')
    oncampus_games = split_multiselect(df, 'On-Campus Games & Entertainment')

    # Combine and get top 10
    all_oncampus = pd.concat([oncampus_social, oncampus_games])
    if len(all_oncampus) > 0:
        top_oncampus = all_oncampus.nlargest(10)
        top_oncampus.plot(kind='barh', color='coral')
        plt.title('Top 10 On-Campus Events', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/top_oncampus_events.png', dpi=300, bbox_inches='tight')
        print("  ✓ top_oncampus_events.png")
    plt.close()

    # 4. Off-Campus Activities
    plt.figure(figsize=(12, 8))
    outdoor = split_multiselect(df, 'Outdoor Activities')
    daytrips = split_multiselect(df, 'Day Trips')
    entertainment = split_multiselect(df, 'Entertainment Outings')

    all_offcampus = pd.concat([outdoor, daytrips, entertainment])
    if len(all_offcampus) > 0:
        top_offcampus = all_offcampus.nlargest(10)
        top_offcampus.plot(kind='barh', color='teal')
        plt.title('Top 10 Off-Campus Activities', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/top_offcampus_activities.png', dpi=300, bbox_inches='tight')
        print("  ✓ top_offcampus_activities.png")
    plt.close()

    # 5. Seasonal Events
    plt.figure(figsize=(10, 6))
    seasonal = split_multiselect(df, 'Seasonal Celebrations')
    if len(seasonal) > 0:
        seasonal.plot(kind='barh', color='orange')
        plt.title('Seasonal Celebration Preferences', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/seasonal_events.png', dpi=300, bbox_inches='tight')
        print("  ✓ seasonal_events.png")
    plt.close()

    # 6. Availability Times
    plt.figure(figsize=(10, 6))
    availability = split_multiselect(df, 'Availability Times')
    if len(availability) > 0:
        availability.plot(kind='barh', color='purple')
        plt.title('When People Can Attend Events', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/availability_times.png', dpi=300, bbox_inches='tight')
        print("  ✓ availability_times.png")
    plt.close()

    # 7. Main Barriers
    plt.figure(figsize=(10, 6))
    barriers = split_multiselect(df, 'Main Barriers')
    if len(barriers) > 0:
        barriers.plot(kind='barh', color='indianred')
        plt.title('Barriers to Attendance', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/barriers.png', dpi=300, bbox_inches='tight')
        print("  ✓ barriers.png")
    plt.close()

    # 8. 3D Print Interest (if present)
    if '3D Print Interest' in df.columns:
        plt.figure(figsize=(8, 6))
        print_interest = df['3D Print Interest'].value_counts()
        colors = ['#2ecc71', '#f39c12', '#e74c3c']
        print_interest.plot(kind='pie', autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Interest in 3D Printed Merchandise', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/3d_print_interest.png', dpi=300, bbox_inches='tight')
        print("  ✓ 3d_print_interest.png")
        plt.close()

    # 9. Alcohol Preference
    if 'Alcohol Preference' in df.columns:
        plt.figure(figsize=(8, 6))
        alcohol = df['Alcohol Preference'].value_counts()
        alcohol.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Alcohol Preference for Events', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/alcohol_preference.png', dpi=300, bbox_inches='tight')
        print("  ✓ alcohol_preference.png")
        plt.close()

    # 10. Participation Level
    plt.figure(figsize=(10, 6))
    participation = split_multiselect(df, 'Participation Level')
    if len(participation) > 0:
        participation.plot(kind='barh', color='mediumseagreen')
        plt.title('How People Want to Participate', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/participation_level.png', dpi=300, bbox_inches='tight')
        print("  ✓ participation_level.png")
    plt.close()

def export_summary_csv(df, output_file="polls/events_poll_summary.csv"):
    """Export summary statistics to CSV"""
    summaries = []

    # Multi-select columns
    multiselect_cols = [
        'On-Campus Social Events',
        'On-Campus Games & Entertainment',
        'Seasonal Celebrations',
        'Outdoor Activities',
        'Day Trips',
        'Entertainment Outings',
        'Availability Times',
        'Main Barriers',
        'Participation Level'
    ]

    for col in multiselect_cols:
        if col in df.columns:
            counts = split_multiselect(df, col)
            for item, count in counts.items():
                percentage = (count / len(df)) * 100
                summaries.append({
                    'Category': col,
                    'Item': item,
                    'Count': count,
                    'Percentage': f"{percentage:.1f}%"
                })

    # Single-select columns
    singleselect_cols = ['Event Frequency', 'Event Budget', '3D Print Interest', 'Alcohol Preference']

    for col in singleselect_cols:
        if col in df.columns:
            counts = df[col].value_counts()
            for item, count in counts.items():
                percentage = (count / len(df)) * 100
                summaries.append({
                    'Category': col,
                    'Item': item,
                    'Count': count,
                    'Percentage': f"{percentage:.1f}%"
                })

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(output_file, index=False)
    print(f"\n✓ Summary exported to '{output_file}'")

def main():
    """Main analysis function"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_events_poll.py <csv_file>")
        print("Example: python analyze_events_poll.py events_poll_responses.csv")
        sys.exit(1)

    csv_file = sys.argv[1]

    # Load data
    df = load_data(csv_file)

    # Print summary
    print_summary(df)

    # Analyze each section
    print("\n" + "="*60)
    print("DETAILED ANALYSIS")
    print("="*60)

    analyze_multiselect_column(df, 'On-Campus Social Events', 'ON-CAMPUS: Social Events')
    analyze_multiselect_column(df, 'On-Campus Games & Entertainment', 'ON-CAMPUS: Games & Entertainment')
    analyze_multiselect_column(df, 'Seasonal Celebrations', 'Seasonal Celebrations')

    analyze_multiselect_column(df, 'Outdoor Activities', 'OFF-CAMPUS: Outdoor Activities')
    analyze_multiselect_column(df, 'Day Trips', 'OFF-CAMPUS: Day Trips')
    analyze_multiselect_column(df, 'Entertainment Outings', 'OFF-CAMPUS: Entertainment')

    analyze_singleselect_column(df, 'Event Frequency', 'Event Frequency Preference')
    analyze_multiselect_column(df, 'Availability Times', 'When People Can Attend')
    analyze_multiselect_column(df, 'Main Barriers', 'Barriers to Attendance')

    analyze_singleselect_column(df, 'Event Budget', 'Event Budget Willingness')
    analyze_singleselect_column(df, '3D Print Interest', '3D Print Merchandise Interest')

    analyze_multiselect_column(df, 'Participation Level', 'How People Want to Participate')
    analyze_singleselect_column(df, 'Alcohol Preference', 'Alcohol Preference')

    # Create visualizations
    create_visualizations(df)

    # Export summary
    export_summary_csv(df)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Review the charts in 'analysis_charts_events/' folder")
    print("  2. Check 'events_poll_summary.csv' for detailed statistics")
    print("  3. Look at 'Additional Suggestions' column in CSV for open-ended feedback")
    print("  4. If 3D print interest is high (>60%), launch the 3D merch poll")

if __name__ == "__main__":
    main()
