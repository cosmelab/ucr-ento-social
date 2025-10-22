#!/usr/bin/env python3
"""
Create improved poll visualizations with transparent backgrounds,
N + % labels, and modern styling
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set modern style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# UCR Colors
UCR_BLUE = '#003DA5'
UCR_GOLD = '#FFC947'
COLORS = ['#003DA5', '#4A90E2', '#6BA3F5', '#FFC947', '#FFD700']

def split_multiselect(df, column):
    """Split comma-separated values and count"""
    if column not in df.columns:
        return pd.Series()

    all_items = []
    for value in df[column].dropna():
        items = [item.strip() for item in str(value).split(',')]
        all_items.extend(items)

    return pd.Series(all_items).value_counts()

def create_horizontal_bar_with_labels(data, title, output_path, top_n=None):
    """Create horizontal bar chart with N + % labels"""
    total = data.sum()

    if top_n:
        data = data.head(top_n)

    # Create figure with transparent background
    fig, ax = plt.subplots(figsize=(12, max(6, len(data) * 0.4)))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Create bars
    bars = ax.barh(range(len(data)), data.values, color=UCR_BLUE, alpha=0.8)

    # Add N + % labels on bars
    for i, (count, bar) in enumerate(zip(data.values, bars)):
        percentage = (count / total) * 100
        label = f'N={count} ({percentage:.1f}%)'
        ax.text(count + max(data.values)*0.02, i, label,
                va='center', fontsize=10, fontweight='bold')

    # Styling
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data.index, fontsize=11)
    ax.set_xlabel('Number of Responses', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"  ✓ {output_path.name}")

def create_donut_chart(data, title, output_path):
    """Create modern donut chart with N + %"""
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Create donut
    wedges, texts, autotexts = ax.pie(data.values, labels=data.index,
                                        autopct=lambda pct: f'{pct:.1f}%\n(N={int(pct/100.*sum(data.values))})',
                                        colors=COLORS[:len(data)],
                                        startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})

    # Create donut hole
    centre_circle = plt.Circle((0, 0), 0.70, fc='white', alpha=0.0)
    ax.add_artist(centre_circle)

    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"  ✓ {output_path.name}")

def create_lollipop_chart(data, title, output_path, top_n=10):
    """Create modern lollipop chart"""
    data = data.head(top_n)
    total = data.sum()

    fig, ax = plt.subplots(figsize=(12, max(6, len(data) * 0.5)))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Create lollipop
    ax.hlines(y=range(len(data)), xmin=0, xmax=data.values,
              color=UCR_BLUE, alpha=0.4, linewidth=5)
    ax.plot(data.values, range(len(data)), "o",
            markersize=12, color=UCR_BLUE, alpha=0.8)

    # Add labels
    for i, count in enumerate(data.values):
        percentage = (count / total) * 100
        ax.text(count + max(data.values)*0.02, i,
                f'N={count} ({percentage:.1f}%)',
                va='center', fontsize=10, fontweight='bold')

    # Styling
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data.index, fontsize=11)
    ax.set_xlabel('Number of Responses', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines='right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"  ✓ {output_path.name}")

def analyze_coffee_hour_poll():
    """Generate improved visualizations for coffee hour poll"""
    print("\n" + "="*70)
    print("CREATING IMPROVED COFFEE HOUR VISUALIZATIONS")
    print("="*70)

    df = pd.read_csv('polls/coffee_hour_poll_responses.csv')
    output_dir = Path('polls/analysis_results/improved_charts_coffee_hour')
    output_dir.mkdir(exist_ok=True, parents=True)

    print(f"\nTotal responses: {len(df)}\n")

    # 1. Preferred Days - Horizontal bar
    days = split_multiselect(df, 'Preferred Days')
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    days = days.reindex([d for d in weekday_order if d in days.index])
    create_horizontal_bar_with_labels(days, 'Preferred Days for Coffee Hour',
                                       output_dir / 'preferred_days.png')

    # 2. Start Times - Lollipop chart
    times = split_multiselect(df, 'Start Time')
    create_lollipop_chart(times, 'Preferred Start Times',
                          output_dir / 'start_times.png')

    # 3. Frequency - Donut chart
    if 'Frequency' in df.columns:
        freq = df['Frequency'].value_counts()
        create_donut_chart(freq, 'Preferred Frequency',
                          output_dir / 'frequency.png')

    # 4. Duration - Donut chart
    if 'Duration' in df.columns:
        duration = df['Duration'].value_counts()
        create_donut_chart(duration, 'Preferred Duration',
                          output_dir / 'duration.png')

    # 5. Food Preferences - Horizontal bar
    food = split_multiselect(df, 'Food Options')
    create_horizontal_bar_with_labels(food, 'Food Preferences',
                                       output_dir / 'food.png')

    # 6. Beverages - Side by side
    coffee = split_multiselect(df, 'Coffee Types')
    create_horizontal_bar_with_labels(coffee.head(6), 'Coffee Preferences',
                                       output_dir / 'coffee.png', top_n=6)

    tea = split_multiselect(df, 'Tea Types')
    create_horizontal_bar_with_labels(tea.head(6), 'Tea Preferences',
                                       output_dir / 'tea.png', top_n=6)

    # 7. Location - Donut
    if 'Location Preference' in df.columns:
        location = df['Location Preference'].value_counts()
        create_donut_chart(location, 'Location Preferences',
                          output_dir / 'location.png')

    print(f"\n✓ Charts saved to {output_dir}/\n")

def main():
    analyze_coffee_hour_poll()

if __name__ == "__main__":
    main()
