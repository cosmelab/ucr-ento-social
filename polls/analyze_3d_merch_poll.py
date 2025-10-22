#!/usr/bin/env python3
"""
UCR Entomology Social Committee - 3D Merch Poll Analysis Script
Analyzes CSV data exported from Google Sheets 3D merchandise poll responses
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
    print("3D MERCHANDISE POLL SUMMARY")
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

def create_visualizations(df, output_dir="analysis_charts_3d_merch"):
    """Create visualization charts"""
    Path(output_dir).mkdir(exist_ok=True)
    print(f"\n\nGenerating charts in '{output_dir}/' folder...")

    # 1. Purchase Interest
    if 'Purchase Interest' in df.columns:
        plt.figure(figsize=(8, 6))
        interest = df['Purchase Interest'].value_counts()
        colors = ['#2ecc71', '#f39c12', '#e74c3c']
        interest.plot(kind='pie', autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Purchase Interest Level', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/purchase_interest.png', dpi=300, bbox_inches='tight')
        print("  ✓ purchase_interest.png")
        plt.close()

    # 2. All Product Types Combined
    plt.figure(figsize=(12, 8))
    keychain = split_multiselect(df, 'Keychain Products')
    decorative = split_multiselect(df, 'Decorative Products')
    functional = split_multiselect(df, 'Functional Products')

    all_products = pd.concat([keychain, decorative, functional])
    if len(all_products) > 0:
        top_products = all_products.nlargest(12)
        top_products.plot(kind='barh', color='steelblue')
        plt.title('Most Popular Product Types', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/all_products.png', dpi=300, bbox_inches='tight')
        print("  ✓ all_products.png")
    plt.close()

    # 3. Product Categories Comparison
    plt.figure(figsize=(10, 6))
    category_counts = {
        'Keychains': len(split_multiselect(df, 'Keychain Products')),
        'Decorative': len(split_multiselect(df, 'Decorative Products')),
        'Functional': len(split_multiselect(df, 'Functional Products'))
    }
    pd.Series(category_counts).plot(kind='bar', color=['coral', 'teal', 'gold'])
    plt.title('Product Category Popularity', fontsize=14, fontweight='bold')
    plt.xlabel('Category')
    plt.ylabel('Total Selections')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/product_categories.png', dpi=300, bbox_inches='tight')
    print("  ✓ product_categories.png")
    plt.close()

    # 4. Favorite Insects
    plt.figure(figsize=(12, 8))
    insects = split_multiselect(df, 'Favorite Insects')
    if len(insects) > 0:
        insects.plot(kind='barh', color='green')
        plt.title('Top Insect Preferences (MOST IMPORTANT!)', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/favorite_insects.png', dpi=300, bbox_inches='tight')
        print("  ✓ favorite_insects.png")
    plt.close()

    # 5. Design Style
    if 'Design Style' in df.columns:
        plt.figure(figsize=(10, 6))
        style = df['Design Style'].value_counts()
        style.plot(kind='barh', color='purple')
        plt.title('Design Style Preferences', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/design_style.png', dpi=300, bbox_inches='tight')
        print("  ✓ design_style.png")
        plt.close()

    # 6. Printing Method
    if 'Printing Method' in df.columns:
        plt.figure(figsize=(10, 6))
        printing = df['Printing Method'].value_counts()
        printing.plot(kind='barh', color='darkorange')
        plt.title('Printing Method Preferences', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/printing_method.png', dpi=300, bbox_inches='tight')
        print("  ✓ printing_method.png")
        plt.close()

    # 7. Color Preference
    if 'Color Preference' in df.columns:
        plt.figure(figsize=(10, 6))
        colors_pref = df['Color Preference'].value_counts()
        colors_pref.plot(kind='barh', color='indianred')
        plt.title('Color/Finish Preferences', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Responses')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/color_preference.png', dpi=300, bbox_inches='tight')
        print("  ✓ color_preference.png")
        plt.close()

    # 8. Price Ranges (Combined)
    if 'Price Small Items' in df.columns and 'Price Large Items' in df.columns:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        small_price = df['Price Small Items'].value_counts()
        small_price.plot(kind='barh', ax=ax1, color='lightblue')
        ax1.set_title('Price Range - Small Items (Keychains)', fontweight='bold')
        ax1.set_xlabel('Number of Responses')

        large_price = df['Price Large Items'].value_counts()
        large_price.plot(kind='barh', ax=ax2, color='lightcoral')
        ax2.set_title('Price Range - Large Items (Decorative)', fontweight='bold')
        ax2.set_xlabel('Number of Responses')

        plt.tight_layout()
        plt.savefig(f'{output_dir}/price_ranges.png', dpi=300, bbox_inches='tight')
        print("  ✓ price_ranges.png")
        plt.close()

def export_summary_csv(df, output_file="polls/3d_merch_poll_summary.csv"):
    """Export summary statistics to CSV"""
    summaries = []

    # Multi-select columns
    multiselect_cols = [
        'Keychain Products',
        'Decorative Products',
        'Functional Products',
        'Favorite Insects'
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
        'Purchase Interest',
        'Design Style',
        'Printing Method',
        'Color Preference',
        'Price Small Items',
        'Price Large Items'
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

def print_design_recommendations(df):
    """Print actionable design recommendations based on the data"""
    print("\n" + "="*60)
    print("DESIGN RECOMMENDATIONS")
    print("="*60)

    if 'Favorite Insects' in df.columns:
        insects = split_multiselect(df, 'Favorite Insects')
        if len(insects) > 0:
            top_3_insects = insects.head(3)
            print("\nTop 3 insects to prioritize for design:")
            for i, (insect, count) in enumerate(top_3_insects.items(), 1):
                percentage = (count / len(df)) * 100
                print(f"  {i}. {insect} ({count} responses, {percentage:.1f}%)")

    if 'Design Style' in df.columns:
        style = df['Design Style'].value_counts()
        if len(style) > 0:
            top_style = style.index[0]
            print(f"\nMost requested design style: {top_style}")

    if 'Printing Method' in df.columns:
        method = df['Printing Method'].value_counts()
        if len(method) > 0:
            top_method = method.index[0]
            print(f"Most requested printing method: {top_method}")

    if 'Color Preference' in df.columns:
        color = df['Color Preference'].value_counts()
        if len(color) > 0:
            top_color = color.index[0]
            print(f"Most requested color/finish: {top_color}")

    # Product recommendations
    keychain = split_multiselect(df, 'Keychain Products')
    decorative = split_multiselect(df, 'Decorative Products')
    functional = split_multiselect(df, 'Functional Products')

    all_products = pd.concat([keychain, decorative, functional])
    if len(all_products) > 0:
        print("\nTop 5 products to create first:")
        top_5 = all_products.head(5)
        for i, (product, count) in enumerate(top_5.items(), 1):
            percentage = (count / len(df)) * 100
            print(f"  {i}. {product} ({count} responses, {percentage:.1f}%)")

    print("\n" + "="*60)

def main():
    """Main analysis function"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_3d_merch_poll.py <csv_file>")
        print("Example: python analyze_3d_merch_poll.py 3d_merch_poll_responses.csv")
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

    analyze_singleselect_column(df, 'Purchase Interest', 'Purchase Interest Level')

    analyze_multiselect_column(df, 'Keychain Products', 'KEYCHAINS & ACCESSORIES')
    analyze_multiselect_column(df, 'Decorative Products', 'DECORATIVE ITEMS')
    analyze_multiselect_column(df, 'Functional Products', 'FUNCTIONAL ITEMS')

    analyze_multiselect_column(df, 'Favorite Insects', 'FAVORITE INSECTS (TOP PRIORITY!)')

    analyze_singleselect_column(df, 'Design Style', 'Design Style Preferences')
    analyze_singleselect_column(df, 'Printing Method', 'Printing Method Preferences')
    analyze_singleselect_column(df, 'Color Preference', 'Color/Finish Preferences')

    analyze_singleselect_column(df, 'Price Small Items', 'Price Range - Small Items')
    analyze_singleselect_column(df, 'Price Large Items', 'Price Range - Large Items')

    # Create visualizations
    create_visualizations(df)

    # Export summary
    export_summary_csv(df)

    # Print design recommendations
    print_design_recommendations(df)

    print("\nNext steps:")
    print("  1. Review the charts in 'analysis_charts_3d_merch/' folder")
    print("  2. Check '3d_merch_poll_summary.csv' for detailed statistics")
    print("  3. Look at 'Additional Suggestions' column in CSV for specific design ideas")
    print("  4. Start designing the top 3 insects in the most popular style")
    print("  5. Create test prints and get feedback before ordering in bulk")

if __name__ == "__main__":
    main()
