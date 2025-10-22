#!/usr/bin/env python3
"""
UCR Entomology Social Committee - Coffee Hour Poll Analysis Script
Analyzes CSV data exported from Google Sheets coffee hour poll responses
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
    print("COFFEE HOUR POLL SUMMARY")
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
        print(f"{item:<45} {count:>3} ({percentage:>5.1f}%) {bar}")

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
        print(f"{item:<45} {count:>3} ({percentage:>5.1f}%) {bar}")

    return counts

def create_visualizations(df, output_dir="analysis_charts_coffee_hour"):
    """Create visualization charts"""
    Path(output_dir).mkdir(exist_ok=True)
    print(f"\n\nGenerating charts in '{output_dir}/' folder...")

    # 1. Role Distribution
    if 'Role' in df.columns:
        plt.figure(figsize=(10, 6))
        role_counts = df['Role'].value_counts()
        role_counts.plot(kind='barh', color='steelblue')
        plt.title('Role Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/role_distribution.png', dpi=300, bbox_inches='tight')
        print("  ✓ role_distribution.png")
        plt.close()

    # 2. Frequency Preference
    if 'Frequency' in df.columns:
        plt.figure(figsize=(10, 6))
        freq_counts = df['Frequency'].value_counts()
        freq_counts.plot(kind='barh', color='green')
        plt.title('Frequency Preferences', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/frequency_preference.png', dpi=300, bbox_inches='tight')
        print("  ✓ frequency_preference.png")
        plt.close()

    # 3. Preferred Days (MOST IMPORTANT!)
    plt.figure(figsize=(10, 6))
    days = split_multiselect(df, 'Preferred Days')
    if len(days) > 0:
        # Sort by weekday order
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        days = days.reindex([d for d in weekday_order if d in days.index])
        days.plot(kind='bar', color='coral')
        plt.title('Preferred Days (MOST IMPORTANT!)', fontsize=14, fontweight='bold')
        plt.xlabel('Day of Week')
        plt.ylabel('Number of Responses')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/preferred_days.png', dpi=300, bbox_inches='tight')
        print("  ✓ preferred_days.png")
    plt.close()

    # 4. Start Time (MOST IMPORTANT!)
    plt.figure(figsize=(12, 8))
    start_times = split_multiselect(df, 'Start Time')
    if len(start_times) > 0:
        # Sort by time order
        time_order = [
            '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
            '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM'
        ]
        start_times = start_times.reindex([t for t in time_order if t in start_times.index])

        # Color code morning vs afternoon
        colors = ['#FFD700' if 'AM' in idx else '#FF8C00' for idx in start_times.index]
        start_times.plot(kind='barh', color=colors)
        plt.title('Preferred Start Times (MOST IMPORTANT!)', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.ylabel('Start Time')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/start_times.png', dpi=300, bbox_inches='tight')
        print("  ✓ start_times.png")
    plt.close()

    # 5. Duration Preference
    if 'Duration' in df.columns:
        plt.figure(figsize=(10, 6))
        duration_counts = df['Duration'].value_counts()
        duration_counts.plot(kind='barh', color='purple')
        plt.title('Duration Preferences', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/duration_preference.png', dpi=300, bbox_inches='tight')
        print("  ✓ duration_preference.png")
        plt.close()

    # 6. Coffee & Tea Preferences (Combined)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    coffee = split_multiselect(df, 'Coffee Types')
    if len(coffee) > 0:
        coffee.head(6).plot(kind='barh', ax=ax1, color='saddlebrown')
        ax1.set_title('Coffee Type Preferences', fontweight='bold')
        ax1.set_xlabel('Number of Responses')

    tea = split_multiselect(df, 'Tea Types')
    if len(tea) > 0:
        tea.head(6).plot(kind='barh', ax=ax2, color='darkgreen')
        ax2.set_title('Tea Type Preferences', fontweight='bold')
        ax2.set_xlabel('Number of Responses')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/beverages.png', dpi=300, bbox_inches='tight')
    print("  ✓ beverages.png")
    plt.close()

    # 7. Food Options
    plt.figure(figsize=(12, 6))
    food = split_multiselect(df, 'Food Options')
    if len(food) > 0:
        food.plot(kind='barh', color='tomato')
        plt.title('Food Preferences', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/food_preferences.png', dpi=300, bbox_inches='tight')
        print("  ✓ food_preferences.png")
    plt.close()

    # 8. Location Preference
    if 'Location Preference' in df.columns:
        plt.figure(figsize=(10, 6))
        location_counts = df['Location Preference'].value_counts()
        location_counts.plot(kind='barh', color='teal')
        plt.title('Location Preferences', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/location_preference.png', dpi=300, bbox_inches='tight')
        print("  ✓ location_preference.png")
        plt.close()

    # 9. Environment Preference
    if 'Environment Preference' in df.columns:
        plt.figure(figsize=(8, 6))
        env_counts = df['Environment Preference'].value_counts()
        env_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Indoor vs Outdoor Preference', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/environment_preference.png', dpi=300, bbox_inches='tight')
        print("  ✓ environment_preference.png")
        plt.close()

    # 10. Lab Hosting Willingness
    if 'Lab Hosting Willingness' in df.columns:
        plt.figure(figsize=(10, 6))
        hosting_counts = df['Lab Hosting Willingness'].value_counts()
        hosting_counts.plot(kind='barh', color='mediumseagreen')
        plt.title('Lab Hosting Willingness', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/lab_hosting.png', dpi=300, bbox_inches='tight')
        print("  ✓ lab_hosting.png")
        plt.close()

    # 11. Barriers to Attendance
    plt.figure(figsize=(12, 6))
    barriers = split_multiselect(df, 'Barriers')
    if len(barriers) > 0:
        barriers.plot(kind='barh', color='indianred')
        plt.title('Barriers to Attendance', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/barriers.png', dpi=300, bbox_inches='tight')
        print("  ✓ barriers.png")
    plt.close()

def export_summary_csv(df, output_file="polls/coffee_hour_poll_summary.csv"):
    """Export summary statistics to CSV"""
    summaries = []

    # Multi-select columns
    multiselect_cols = [
        'Preferred Days',
        'Start Time',
        'Coffee Types',
        'Tea Types',
        'Food Options',
        'Music Types',
        'Barriers'
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
    singleselect_cols = [
        'Role',
        'Frequency',
        'Duration',
        'Environment Preference',
        'Location Preference',
        'Lab Hosting Willingness'
    ]

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

def print_scheduling_recommendations(df):
    """Print actionable scheduling recommendations based on the data"""
    print("\n" + "="*60)
    print("SCHEDULING RECOMMENDATIONS")
    print("="*60)

    if 'Preferred Days' in df.columns:
        days = split_multiselect(df, 'Preferred Days')
        if len(days) > 0:
            top_day = days.index[0]
            top_day_count = days.iloc[0]
            percentage = (top_day_count / len(df)) * 100
            print(f"\nBest day to schedule: {top_day} ({top_day_count} responses, {percentage:.1f}%)")

            if len(days) > 1:
                second_day = days.index[1]
                print(f"Alternate day: {second_day}")

    # Start times
    if 'Start Time' in df.columns:
        start_times = split_multiselect(df, 'Start Time')
        if len(start_times) > 0:
            top_time = start_times.index[0]
            top_time_count = start_times.iloc[0]
            percentage = (top_time_count / len(df)) * 100
            print(f"\nBest start time: {top_time} ({top_time_count} responses, {percentage:.1f}%)")

            if len(start_times) > 1:
                second_time = start_times.index[1]
                second_count = start_times.iloc[1]
                percentage2 = (second_count / len(df)) * 100
                print(f"Alternate start time: {second_time} ({second_count} responses, {percentage2:.1f}%)")

    if 'Duration' in df.columns:
        duration = df['Duration'].value_counts()
        if len(duration) > 0:
            best_duration = duration.index[0]
            print(f"\nRecommended duration: {best_duration}")

    if 'Frequency' in df.columns:
        frequency = df['Frequency'].value_counts()
        if len(frequency) > 0:
            best_frequency = frequency.index[0]
            print(f"Recommended frequency: {best_frequency}")

    if 'Location Preference' in df.columns:
        location = df['Location Preference'].value_counts()
        if len(location) > 0:
            best_location = location.index[0]
            print(f"\nBest location: {best_location}")

    # Food recommendations
    food = split_multiselect(df, 'Food Options')
    if len(food) > 0:
        print("\nTop 3 food options:")
        for i, (food_item, count) in enumerate(food.head(3).items(), 1):
            percentage = (count / len(df)) * 100
            print(f"  {i}. {food_item} ({count} responses, {percentage:.1f}%)")

    # Check for dietary restrictions
    if len(food) > 0:
        dietary = [item for item in food.index if 'Gluten-free' in item or 'Vegan' in item or 'Vegetarian' in item]
        if dietary:
            print("\nImportant: Include dietary accommodations:")
            for item in dietary:
                print(f"  - {item}")

    print("\n" + "="*60)

def main():
    """Main analysis function"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_coffee_hour_poll.py <csv_file>")
        print("Example: python analyze_coffee_hour_poll.py coffee_hour_poll_responses.csv")
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

    analyze_singleselect_column(df, 'Role', 'Role Distribution')

    analyze_singleselect_column(df, 'Frequency', 'Frequency Preferences')
    analyze_multiselect_column(df, 'Preferred Days', 'PREFERRED DAYS (MOST IMPORTANT!)')
    analyze_singleselect_column(df, 'Duration', 'Duration Preferences')
    analyze_multiselect_column(df, 'Start Time', 'START TIMES (MOST IMPORTANT!)')

    analyze_multiselect_column(df, 'Coffee Types', 'Coffee Type Preferences')
    analyze_multiselect_column(df, 'Tea Types', 'Tea Type Preferences')
    analyze_multiselect_column(df, 'Food Options', 'Food Preferences')

    analyze_singleselect_column(df, 'Environment Preference', 'Indoor/Outdoor Preference')
    analyze_singleselect_column(df, 'Location Preference', 'Location Preferences')
    analyze_multiselect_column(df, 'Music Types', 'Music Type Preferences')

    analyze_singleselect_column(df, 'Lab Hosting Willingness', 'Lab Hosting Willingness')
    analyze_multiselect_column(df, 'Barriers', 'Barriers to Attendance')

    # Create visualizations
    create_visualizations(df)

    # Export summary
    export_summary_csv(df)

    # Print scheduling recommendations
    print_scheduling_recommendations(df)

    print("\nNext steps:")
    print("  1. Review the charts in 'analysis_charts_coffee_hour/' folder")
    print("  2. Check 'coffee_hour_poll_summary.csv' for detailed statistics")
    print("  3. Look at 'Additional Suggestions' column in CSV for specific feedback")
    print("  4. Schedule first coffee hour on the most popular day/time")
    print("  5. Contact labs willing to host (check 'Lab Hosting Willingness')")
    print("  6. Plan menu based on food preferences and dietary restrictions")

if __name__ == "__main__":
    main()
