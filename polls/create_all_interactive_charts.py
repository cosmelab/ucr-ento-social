#!/usr/bin/env python3
"""
Create interactive Plotly visualizations for ALL poll results
With DARK THEME and varied colors - NO MONOTONE BLUE!
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Diverse color palette - NO ALL BLUE!
COLORS = ['#4A90E2', '#FFC947', '#90EE90', '#FF6B6B', '#9B59B6', '#1ABC9C', '#F39C12', '#E74C3C', '#3498DB', '#2ECC71']
UCR_BLUE = '#003DA5'
UCR_GOLD = '#FFC947'

def wrap_label(text, max_length=20):
    """Wrap long labels into multiple lines"""
    if len(text) <= max_length:
        return text

    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(' '.join(current_line))

    return '<br>'.join(lines)

def shorten_labels(data):
    """Shorten long labels for better chart readability"""
    label_map = {
        # Purchase Interest
        "Yes, definitely": "Yes",
        "Maybe, depends on design/price": "Maybe",
        "No, not interested": "No",

        # Coffee/Tea
        "Espresso-based drinks (latte, cappuccino)": "Espresso drinks",
        "cappuccino)": "Espresso drinks",  # Handle split case

        # Food
        "Pastries and baked goods": "Pastries",
        "Cultural foods from different countries": "Cultural foods",
        "Vegan/Vegetarian options": "Vegan/Vegetarian",
        "Gluten-free options": "Gluten-free",

        # Location
        "Mix of both depending on weather": "Weather dependent",
        "Building lobby/atrium": "Lobby/Atrium",
        "Department conference room": "Conference room",
        "Rotating between labs": "Rotating labs",

        # Hosting
        "Maybe, need to discuss with lab": "Maybe",
        "Yes, occasionally": "Yes (occasionally)",
        "Yes, regularly": "Yes (regularly)",

        # Music
        "No music, quiet conversation only": "No music",
        "Cultural music from hosting lab": "Cultural music",

        # Barriers
        "Time constraints": "Time",
        "Class conflicts": "Classes",
        "Meeting conflicts": "Meetings",
        "Research commitments": "Research",
        "Family obligations": "Family",
        "Social anxiety": "Anxiety",
        "Transportation": "Transport",
        "Time doesn't work": "Timing",
        "Dietary restrictions not met": "Dietary needs",
        "Location too far": "Location",

        # Events - Availability
        "Weekday lunch": "Lunch",
        "Weekday afternoon": "Afternoon",
        "Weekday evening": "Evening",
        "Friday afternoon": "Fri afternoon",

        # Design/Printing
        "Realistic/Scientific": "Realistic",
        "Cute/Stylized": "Cute",
        "Mix of styles": "Mixed",
        "No preference": "No pref",
        "FDM/PETG": "PETG",
        "FDM/PLA": "PLA",

        # Colors
        "Bright colors": "Bright",
        "Natural colors": "Natural",
        "Single color": "Single",

        # Size
        "Small (1-2 inches)": "Small",
        "Medium (3-4 inches)": "Medium",
        "Large (5+ inches)": "Large",
    }

    # Create new series with shortened labels
    new_data = pd.Series(dtype='int64')
    for label, value in data.items():
        short_label = label_map.get(label, label)
        new_data[short_label] = value

    return new_data

def split_multiselect(df, column):
    """Split comma-separated values and count"""
    if column not in df.columns:
        return pd.Series()

    all_items = []
    for value in df[column].dropna():
        items = [item.strip() for item in str(value).split(',')]
        all_items.extend(items)

    return pd.Series(all_items).value_counts()

def consolidate_small_categories(data, min_percent=10, max_others_percent=20):
    """
    Consolidate categories below min_percent into 'Others' category
    Only if total 'Others' stays below max_others_percent
    """
    if len(data) == 0:
        return data

    total = data.sum()
    percentages = (data / total * 100)

    # Find small categories
    small_categories = data[percentages < min_percent]
    large_categories = data[percentages >= min_percent]

    # Check if Others would be too large
    others_total = small_categories.sum()
    others_percent = (others_total / total * 100)

    # Only consolidate if Others is reasonable size and there are small categories
    if len(small_categories) > 1 and others_percent <= max_others_percent and others_percent > 0:
        result = large_categories.copy()
        result['Others'] = others_total
        return result.sort_values(ascending=False)

    return data

def create_interactive_bar(data, title, output_path, orientation='h', consolidate=False):
    """Create interactive horizontal bar chart with VARIED COLORS"""
    # Handle empty data
    if len(data) == 0 or data.sum() == 0:
        print(f"  ⚠ Skipping {output_path.name} - no data")
        return

    # Shorten labels for better readability
    data = shorten_labels(data)

    # Consolidate small categories if requested
    if consolidate:
        data = consolidate_small_categories(data)

    total = data.sum()
    percentages = (data.values / total * 100).round(1)

    # Wrap long labels for better display
    original_labels = data.index.tolist()
    wrapped_labels = [wrap_label(str(label)) for label in original_labels]

    # Use different colors for each bar!
    bar_colors = [COLORS[i % len(COLORS)] for i in range(len(data))]

    hover_text = [f'<b>{item}</b><br>Count: {count}<br>Percentage: {pct:.1f}%'
                  for item, count, pct in zip(original_labels, data.values, percentages)]

    # Smart label positioning: inside for large bars, outside for small ones
    max_value = data.values.max()
    text_positions = ['inside' if val > max_value * 0.15 else 'outside' for val in data.values]

    if orientation == 'h':
        fig = go.Figure(go.Bar(
            y=wrapped_labels,
            x=data.values,
            orientation='h',
            text=[f'<b>{count} ({pct:.1f}%)</b>' for count, pct in zip(data.values, percentages)],
            textposition=text_positions,
            textfont=dict(color='#9FC5E8', size=12, family='Inter, sans-serif'),
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(color=bar_colors, opacity=0.9, line=dict(width=1, color='rgba(255,255,255,0.2)')),
            cliponaxis=False  # Ensure text labels are not clipped
        ))
        xaxis_title = 'Number of Responses'
        yaxis_title = ''
    else:
        fig = go.Figure(go.Bar(
            x=wrapped_labels,
            y=data.values,
            text=[f'<b>{count}<br>({pct:.1f}%)</b>' for count, pct in zip(data.values, percentages)],
            textposition=text_positions,
            textfont=dict(color='#9FC5E8', size=12, family='Inter, sans-serif'),
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(color=bar_colors, opacity=0.9, line=dict(width=1, color='rgba(255,255,255,0.2)')),
            cliponaxis=False  # Ensure text labels are not clipped
        ))
        xaxis_title = ''
        yaxis_title = 'Number of Responses'

    # DARK THEME with explicit axis settings
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family='Inter, sans-serif', color='#4A90E2', weight=600)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=13, color='#9FC5E8'),
        xaxis=dict(
            title=dict(text=xaxis_title, font=dict(color='#9FC5E8', size=13, family='Inter, sans-serif', weight='bold')),
            tickfont=dict(color='#9FC5E8', size=12, family='Inter, sans-serif', weight='bold'),
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True,
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title=dict(text=yaxis_title, font=dict(color='#9FC5E8', size=13, family='Inter, sans-serif', weight='bold')),
            tickfont=dict(color='#9FC5E8', size=12, family='Inter, sans-serif', weight='bold'),
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True,
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        height=max(400, len(data) * 50) if orientation == 'h' else 500,
        margin=dict(l=20, r=100, t=80, b=40),  # More right margin for labels
        hoverlabel=dict(
            bgcolor="rgba(26, 26, 26, 0.95)",
            font_size=14,
            font_family="Inter, sans-serif",
            font_color="#FFC947",
            bordercolor="#4A90E2"
        )
    )

    fig.write_html(output_path, config={'displayModeBar': False})
    print(f"  ✓ {output_path.name}")

def create_interactive_donut(data, title, output_path, legend_position='right', consolidate=False, scale=1.0):
    """Create interactive donut chart with VARIED COLORS"""
    # Handle empty data
    if len(data) == 0 or data.sum() == 0:
        print(f"  ⚠ Skipping {output_path.name} - no data")
        return

    # Shorten labels for better readability
    data = shorten_labels(data)

    # Consolidate small categories if requested
    if consolidate:
        data = consolidate_small_categories(data)

    total = data.sum()
    percentages = (data.values / total * 100).round(1)

    hover_text = [f'<b>{item}</b><br>Count: {count}<br>{pct:.1f}% of responses'
                  for item, count, pct in zip(data.index, data.values, percentages)]

    # Use our varied color palette
    pie_colors = [COLORS[i % len(COLORS)] for i in range(len(data))]

    # Smaller hole for charts with fewer categories (makes pie look bigger)
    hole_size = 0.2 if len(data) <= 3 else 0.35

    # Simpler labels for small pies to reduce clutter
    if len(data) <= 3:
        text_template = '%{label}<br>%{percent}'
        font_size = 13
    else:
        text_template = '%{label}<br>%{value} (%{percent})'
        font_size = 12

    fig = go.Figure(go.Pie(
        labels=data.index,
        values=data.values,
        hole=hole_size,
        marker=dict(colors=pie_colors, line=dict(color='rgba(255,255,255,0.2)', width=2)),
        textinfo='label+percent+value' if len(data) > 3 else 'label+percent',
        texttemplate=text_template,
        textposition='outside',
        textfont=dict(color='#9FC5E8', size=font_size, family='Inter, sans-serif'),
        hovertext=hover_text,
        hoverinfo='text'
    ))

    # DARK THEME - NO LEGEND (labels are already on chart)
    # Taller height and smaller margins for better mobile display
    base_height = 650 if len(data) <= 3 else 550
    chart_height = int(base_height * scale)
    chart_margins = dict(l=10, r=10, t=80, b=10) if len(data) <= 3 else dict(l=20, r=20, t=80, b=20)

    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family='Inter, sans-serif', color='#4A90E2', weight=600)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=13, color='#9FC5E8'),
        height=chart_height,
        showlegend=False,
        hoverlabel=dict(
            bgcolor="rgba(26, 26, 26, 0.95)",
            font_size=14,
            font_family="Inter, sans-serif",
            font_color="#FFC947",
            bordercolor="#4A90E2"
        ),
        margin=chart_margins
    )

    fig.write_html(output_path, config={'displayModeBar': False})
    print(f"  ✓ {output_path.name}")

def analyze_coffee_hour_poll():
    """Generate interactive visualizations for coffee hour poll"""
    print("\n" + "="*70)
    print("CREATING INTERACTIVE COFFEE HOUR CHARTS")
    print("="*70)

    df = pd.read_csv('polls/coffee_hour_poll_responses.csv')
    output_dir = Path('polls/analysis_results/interactive_charts_coffee_hour')
    output_dir.mkdir(exist_ok=True, parents=True)

    print(f"\nTotal responses: {len(df)}")
    print(f"Output directory: {output_dir}\n")

    # 0. Role Demographics - Donut
    if 'Role' in df.columns:
        role = df['Role'].value_counts()
        create_interactive_donut(role, 'Respondent Demographics',
                                output_dir / 'role.html')

    # 1. Preferred Days
    days = split_multiselect(df, 'Preferred Days')
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    days = days.reindex([d for d in weekday_order if d in days.index])
    create_interactive_bar(days, 'Preferred Days for Coffee Hour',
                          output_dir / 'preferred_days.html')

    # 2. Start Times - sorted chronologically
    times = split_multiselect(df, 'Start Time')
    # Sort by time order instead of frequency
    time_order = ['9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
                  '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM']
    times = times.reindex([t for t in time_order if t in times.index])
    create_interactive_bar(times, 'Preferred Start Times',
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

    print(f"\n✓ Coffee Hour charts saved to {output_dir}/\n")

def analyze_events_poll():
    """Generate interactive visualizations for events poll"""
    print("\n" + "="*70)
    print("CREATING INTERACTIVE EVENTS CHARTS")
    print("="*70)

    df = pd.read_csv('polls/events_poll_responses.csv')
    output_dir = Path('polls/analysis_results/interactive_charts_events')
    output_dir.mkdir(exist_ok=True, parents=True)

    print(f"\nTotal responses: {len(df)}")
    print(f"Output directory: {output_dir}\n")

    # On-Campus Social Events
    if 'On-Campus Social Events' in df.columns:
        events = split_multiselect(df, 'On-Campus Social Events')
        create_interactive_bar(events, 'On-Campus Social Events',
                              output_dir / 'on_campus_social.html')

    # On-Campus Games & Entertainment
    if 'On-Campus Games & Entertainment' in df.columns:
        games = split_multiselect(df, 'On-Campus Games & Entertainment')
        create_interactive_bar(games, 'Games & Entertainment Preferences',
                              output_dir / 'games_entertainment.html')

    # Seasonal Celebrations
    if 'Seasonal Celebrations' in df.columns:
        seasonal = split_multiselect(df, 'Seasonal Celebrations')
        create_interactive_bar(seasonal, 'Seasonal Celebrations',
                              output_dir / 'seasonal.html')

    # Outdoor Activities
    if 'Outdoor Activities' in df.columns:
        outdoor = split_multiselect(df, 'Outdoor Activities')
        create_interactive_bar(outdoor, 'Outdoor Activities',
                              output_dir / 'outdoor.html')

    # Day Trips
    if 'Day Trips' in df.columns:
        trips = split_multiselect(df, 'Day Trips')
        create_interactive_bar(trips, 'Day Trip Preferences',
                              output_dir / 'day_trips.html')

    # Entertainment Outings
    if 'Entertainment Outings' in df.columns:
        entertainment = split_multiselect(df, 'Entertainment Outings')
        create_interactive_bar(entertainment, 'Entertainment Outings',
                              output_dir / 'entertainment_outings.html')

    # Event Frequency
    if 'Event Frequency' in df.columns:
        freq = df['Event Frequency'].value_counts()
        create_interactive_donut(freq, 'Preferred Event Frequency',
                                output_dir / 'frequency.html')

    # Availability Times
    if 'Availability Times' in df.columns:
        times = split_multiselect(df, 'Availability Times')
        create_interactive_bar(times, 'Best Times for Events',
                              output_dir / 'availability_times.html')

    # Main Barriers
    if 'Main Barriers' in df.columns:
        barriers = split_multiselect(df, 'Main Barriers')
        create_interactive_bar(barriers, 'Main Barriers to Attendance',
                              output_dir / 'barriers.html')

    # Event Budget
    if 'Event Budget' in df.columns:
        budget = df['Event Budget'].value_counts()
        create_interactive_donut(budget, 'Event Budget Preferences',
                                output_dir / 'budget.html')

    # Participation Level - with consolidation
    if 'Participation Level' in df.columns:
        participation = df['Participation Level'].value_counts()
        create_interactive_donut(participation, 'Participation Level',
                                output_dir / 'participation.html', consolidate=True)

    print(f"\n✓ Events charts saved to {output_dir}/\n")

def analyze_3d_merch_poll():
    """Generate interactive visualizations for 3D merch poll"""
    print("\n" + "="*70)
    print("CREATING INTERACTIVE 3D MERCH CHARTS")
    print("="*70)

    df = pd.read_csv('polls/3d_merch_poll_responses.csv')
    output_dir = Path('polls/analysis_results/interactive_charts_3d_merch')
    output_dir.mkdir(exist_ok=True, parents=True)

    print(f"\nTotal responses: {len(df)}")
    print(f"Output directory: {output_dir}\n")

    # Purchase interest - smaller size
    if 'Purchase Interest' in df.columns:
        interest = df['Purchase Interest'].value_counts()
        create_interactive_donut(interest, 'Purchase Interest Level',
                                output_dir / 'purchase_interest.html', scale=0.8)

    # Keychain Products
    if 'Keychain Products' in df.columns:
        keychain = split_multiselect(df, 'Keychain Products')
        create_interactive_bar(keychain, 'Keychain Product Preferences',
                              output_dir / 'keychain_products.html')

    # Decorative Products
    if 'Decorative Products' in df.columns:
        decorative = split_multiselect(df, 'Decorative Products')
        create_interactive_bar(decorative, 'Decorative Product Preferences',
                              output_dir / 'decorative_products.html')

    # Functional Products
    if 'Functional Products' in df.columns:
        functional = split_multiselect(df, 'Functional Products')
        create_interactive_bar(functional, 'Functional Product Preferences',
                              output_dir / 'functional_products.html')

    # Favorite insects
    if 'Favorite Insects' in df.columns:
        insects = split_multiselect(df, 'Favorite Insects')
        create_interactive_bar(insects, 'Favorite Insects to Feature',
                              output_dir / 'insects.html')

    # Design style - smaller size
    if 'Design Style' in df.columns:
        style = df['Design Style'].value_counts()
        create_interactive_donut(style, 'Design Style Preferences',
                                output_dir / 'design_style.html', scale=0.8)

    # Printing Method - smaller size
    if 'Printing Method' in df.columns:
        printing = df['Printing Method'].value_counts()
        create_interactive_donut(printing, 'Printing Method Preferences',
                                output_dir / 'printing_method.html', scale=0.8)

    # Color Preference - smaller size
    if 'Color Preference' in df.columns:
        color = df['Color Preference'].value_counts()
        create_interactive_donut(color, 'Color Preferences',
                                output_dir / 'color_preference.html', scale=0.8)

    # Size Preference - smaller size
    if 'Size Preference' in df.columns:
        size = df['Size Preference'].value_counts()
        create_interactive_donut(size, 'Size Preferences',
                                output_dir / 'size_preference.html', scale=0.8)

    # Price range - small items - smaller size
    if 'Price Small Items' in df.columns:
        price_small = df['Price Small Items'].value_counts()
        create_interactive_donut(price_small, 'Price Range - Small Items',
                                output_dir / 'price_small.html', scale=0.8)

    # Price range - large items - smaller size
    if 'Price Large Items' in df.columns:
        price_large = df['Price Large Items'].value_counts()
        create_interactive_donut(price_large, 'Price Range - Large Items',
                                output_dir / 'price_large.html', scale=0.8)

    print(f"\n✓ 3D Merch charts saved to {output_dir}/\n")

def main():
    analyze_coffee_hour_poll()
    analyze_events_poll()
    analyze_3d_merch_poll()
    print("\n" + "="*70)
    print("ALL INTERACTIVE CHARTS CREATED WITH DARK THEME!")
    print("="*70)

if __name__ == "__main__":
    main()
