#!/usr/bin/env python3
"""
Create interactive Plotly visualizations for poll results
These can be embedded directly in the website HTML
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# UCR Colors
UCR_BLUE = '#003DA5'
UCR_GOLD = '#FFC947'
UCR_COLORS = ['#003DA5', '#4A90E2', '#6BA3F5', '#FFC947', '#FFD700', '#F4D03F']

def split_multiselect(df, column):
    """Split comma-separated values and count"""
    if column not in df.columns:
        return pd.Series()

    all_items = []
    for value in df[column].dropna():
        items = [item.strip() for item in str(value).split(',')]
        all_items.extend(items)

    return pd.Series(all_items).value_counts()

def create_interactive_bar(data, title, output_path, orientation='h'):
    """Create interactive horizontal bar chart with hover info"""
    total = data.sum()
    percentages = (data.values / total * 100).round(1)

    # Create custom hover text
    hover_text = [f'<b>{item}</b><br>Count: {count}<br>Percentage: {pct:.1f}%'
                  for item, count, pct in zip(data.index, data.values, percentages)]

    if orientation == 'h':
        fig = go.Figure(go.Bar(
            y=data.index,
            x=data.values,
            orientation='h',
            text=[f'N={count} ({pct:.1f}%)' for count, pct in zip(data.values, percentages)],
            textposition='outside',
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(color=UCR_BLUE, opacity=0.8)
        ))
    else:
        fig = go.Figure(go.Bar(
            x=data.index,
            y=data.values,
            text=[f'N={count}<br>({pct:.1f}%)' for count, pct in zip(data.values, percentages)],
            textposition='outside',
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(color=UCR_BLUE, opacity=0.8)
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, family='Inter, sans-serif', color='#003DA5')),
        xaxis=dict(title='Number of Responses' if orientation == 'h' else '',
                   gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(title='' if orientation == 'h' else 'Number of Responses',
                   gridcolor='rgba(0,0,0,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=12),
        height=max(400, len(data) * 40) if orientation == 'h' else 500,
        margin=dict(l=20, r=100, t=60, b=40),
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Inter, sans-serif")
    )

    fig.write_html(output_path, config={'displayModeBar': False})
    print(f"  ✓ {output_path.name}")

def create_interactive_donut(data, title, output_path):
    """Create interactive donut chart"""
    total = data.sum()
    percentages = (data.values / total * 100).round(1)

    # Custom hover text
    hover_text = [f'<b>{item}</b><br>Count: {count}<br>{pct:.1f}% of responses'
                  for item, count, pct in zip(data.index, data.values, percentages)]

    fig = go.Figure(go.Pie(
        labels=data.index,
        values=data.values,
        hole=0.4,
        marker=dict(colors=UCR_COLORS[:len(data)]),
        textinfo='label+percent',
        textposition='outside',
        hovertext=hover_text,
        hoverinfo='text'
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, family='Inter, sans-serif', color='#003DA5')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=12),
        height=500,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1),
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Inter, sans-serif")
    )

    fig.write_html(output_path, config={'displayModeBar': False})
    print(f"  ✓ {output_path.name}")

def analyze_coffee_hour_poll():
    """Generate interactive visualizations for coffee hour poll"""
    print("\n" + "="*70)
    print("CREATING INTERACTIVE COFFEE HOUR CHARTS (Plotly)")
    print("="*70)

    df = pd.read_csv('polls/coffee_hour_poll_responses.csv')
    output_dir = Path('polls/analysis_results/interactive_charts_coffee_hour')
    output_dir.mkdir(exist_ok=True, parents=True)

    print(f"\nTotal responses: {len(df)}")
    print(f"Output directory: {output_dir}\n")

    # 1. Preferred Days
    days = split_multiselect(df, 'Preferred Days')
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    days = days.reindex([d for d in weekday_order if d in days.index])
    create_interactive_bar(days, 'Preferred Days for Coffee Hour',
                          output_dir / 'preferred_days.html')

    # 2. Start Times
    times = split_multiselect(df, 'Start Time')
    create_interactive_bar(times.head(10), 'Top 10 Preferred Start Times',
                          output_dir / 'start_times.html')

    # 3. Frequency - Donut
    if 'Frequency' in df.columns:
        freq = df['Frequency'].value_counts()
        create_interactive_donut(freq, 'How Often Should We Meet?',
                                output_dir / 'frequency.html')

    # 4. Duration - Donut
    if 'Duration' in df.columns:
        duration = df['Duration'].value_counts()
        create_interactive_donut(duration, 'Preferred Duration',
                                output_dir / 'duration.html')

    # 5. Food Preferences
    food = split_multiselect(df, 'Food Options')
    create_interactive_bar(food, 'Food Preferences',
                          output_dir / 'food.html')

    # 6. Coffee Types
    coffee = split_multiselect(df, 'Coffee Types')
    create_interactive_bar(coffee, 'Coffee Preferences',
                          output_dir / 'coffee.html')

    # 7. Tea Types
    tea = split_multiselect(df, 'Tea Types')
    create_interactive_bar(tea, 'Tea Preferences',
                          output_dir / 'tea.html')

    # 8. Location
    if 'Location Preference' in df.columns:
        location = df['Location Preference'].value_counts()
        create_interactive_donut(location, 'Preferred Location',
                                output_dir / 'location.html')

    # 9. Barriers
    barriers = split_multiselect(df, 'Barriers')
    create_interactive_bar(barriers, 'Barriers to Attendance',
                          output_dir / 'barriers.html')

    print(f"\n✓ Interactive charts saved to {output_dir}/\n")
    print("These HTML files can be embedded in your website using <iframe>")

def main():
    analyze_coffee_hour_poll()

if __name__ == "__main__":
    main()
