# poll analysis guide

## overview

This guide explains how to analyze poll responses from Google Sheets using Python.

We have two separate analysis scripts:
- `analyze_events_poll.py` - For the events and activities poll
- `analyze_3d_merch_poll.py` - For the 3D merchandise poll

## quick start

### step 1: export data from google sheets

1. Open your poll responses spreadsheet
2. Click **File > Download > Comma Separated Values (.csv)**
3. Save with a descriptive name in the `polls/` folder:
   - `events_poll_responses.csv` for events poll
   - `3d_merch_poll_responses.csv` for 3D merch poll

### step 2: install required python packages

```bash
pip install pandas matplotlib seaborn
```

### step 3: run the analysis

For events poll:
```bash
cd polls
python analyze_events_poll.py events_poll_responses.csv
```

For 3D merch poll:
```bash
cd polls
python analyze_3d_merch_poll.py 3d_merch_poll_responses.csv
```

## what the scripts do

### 1. console output

Both scripts display text-based analysis with:
- Total number of responses
- Date range of responses
- Breakdown of each question with counts and percentages
- Visual bars showing popularity (█████)

Example output from events poll:
```
ON-CAMPUS: Social Events
------------------------------------------------------------
Happy hours                              45 ( 75.0%) ████████████████████████████████████████
Lab Lightning Talks                      38 ( 63.3%) ███████████████████████████████████
Potluck dinners                          32 ( 53.3%) ██████████████████████████
BBQs and picnics                         28 ( 46.7%) ███████████████████████
```

### 2. charts (saved to folders)

**Events poll** creates charts in `analysis_charts_events/` folder:
- `event_frequency.png` - How often people want events
- `event_budget.png` - What people will pay
- `top_oncampus_events.png` - Most popular on-campus events
- `top_offcampus_activities.png` - Most popular off-campus activities
- `seasonal_events.png` - Seasonal celebration preferences
- `availability_times.png` - When people can attend
- `barriers.png` - What prevents people from attending
- `3d_print_interest.png` - Interest in 3D printed merchandise
- `alcohol_preference.png` - Alcohol preferences
- `participation_level.png` - How people want to help

**3D merch poll** creates charts in `analysis_charts_3d_merch/` folder:
- `purchase_interest.png` - Overall purchase interest level
- `all_products.png` - Most popular product types
- `product_categories.png` - Category comparison (keychains vs decorative vs functional)
- `favorite_insects.png` - Top insect preferences (MOST IMPORTANT!)
- `design_style.png` - Design style preferences
- `printing_method.png` - Printing method preferences (FDM/PLA, FDM/PETG, Resin)
- `color_preference.png` - Color/finish preferences
- `price_ranges.png` - Price willingness for small and large items

### 3. summary csv files

**Events poll**: Creates `events_poll_summary.csv`

**3D merch poll**: Creates `3d_merch_poll_summary.csv`

Both are structured CSV files with all statistics for further analysis in Excel or Google Sheets.

Columns:
- Category (question name)
- Item (response option)
- Count (number of people who selected it)
- Percentage (% of total responses)

### 4. design recommendations (3D merch poll only)

The 3D merch analysis script includes actionable design recommendations:
- Top 3 insects to prioritize
- Most requested design style
- Most requested printing method
- Most requested color/finish
- Top 5 products to create first

## analyzing results

### events poll - key questions to answer

**1. what events should we prioritize?**
- Look at `top_oncampus_events.png` and `top_offcampus_activities.png`
- Focus on items with >50% interest

**2. how often should we hold events?**
- Check `event_frequency.png`
- Use the most popular option

**3. when should events be scheduled?**
- Review `availability_times.png`
- Schedule at times with highest availability
- Cross-reference with `barriers.png` to avoid conflicts

**4. what budget should we plan for?**
- Check `event_budget.png`
- Balance between "free" and paid options
- Most people likely okay with $5-10 for special events

**5. should we pursue 3D print fundraising?**
- Look at `3d_print_interest.png`
- If >60% say "Yes" or "Maybe", launch the detailed 3D merch poll

**6. alcohol at events?**
- Check `alcohol_preference.png`
- If "Mix of both" is popular, alternate events

### 3D merch poll - key questions to answer

**1. is there enough demand?**
- Look at `purchase_interest.png`
- If <50% say "Yes, definitely", may need to adjust pricing or designs
- "Maybe" responses can convert with good designs and reasonable prices

**2. what insects should we design first?**
- Check `favorite_insects.png` - this is THE MOST IMPORTANT chart
- Start with top 3 insects
- Consider printability notes from the poll responses

**3. what products should we make?**
- Review `all_products.png` for most popular items
- Check `product_categories.png` to balance portfolio
- Start with quick-to-print items (keychains, magnets) for fast turnaround

**4. what printing method to use?**
- Look at `printing_method.png`
- If resin is popular, invest in resin printer for detail work
- FDM is good for larger, functional items

**5. how to finish the products?**
- Check `design_style.png` and `color_preference.png`
- "Natural colors" means hand-painting = more time and cost
- "Single color" is faster but less detailed

**6. what prices to set?**
- Review `price_ranges.png`
- Price small items at the most popular range
- Consider cost of materials + time when setting prices
- Leave room for fundraising markup

### reading "other" suggestions

Open the original CSV file and look at the "Additional Suggestions" column for:
- Specific event ideas people mentioned
- Concerns about timing/location
- Suggestions for improvement

## advanced analysis

### finding correlations

Want to see if certain groups prefer certain events? Use pandas:

```python
import pandas as pd

df = pd.read_csv('events_poll_responses.csv')

# Example: Do people who want frequent events also prefer paid events?
freq_budget = pd.crosstab(df['Event Frequency'], df['Event Budget'])
print(freq_budget)
```

### filtering responses

```python
# Find people interested in 3D prints
interested_in_3d = df[df['3D Print Interest'] == 'Yes']

# What events do they prefer?
print(interested_in_3d['On-Campus Social Events'].value_counts())
```

## troubleshooting

### "module not found" error

Install missing packages:
```bash
pip install pandas matplotlib seaborn
```

### "file not found" error

Make sure:
1. CSV file is in the same folder as the script
2. Filename is correct (check spelling)
3. You're running the command from the `polls/` directory

### chart not displaying

Charts are saved as PNG files, not displayed on screen. Look in the `analysis_charts/` folder.

### weird characters in output

If you see encoding issues, export from Google Sheets as UTF-8:
```bash
python analyze_poll.py events_poll_responses.csv > results.txt
```

## tips for presenting results

### to the committee
- Show the PNG charts
- Highlight top 3-5 events in each category
- Present budget willingness to inform fundraising needs
- Share barriers so you can address them

### to the department
- Send summary email with key findings
- Attach 2-3 most relevant charts
- Include quote from "Additional Suggestions" that resonates
- Announce first event based on results

### for future planning
- Keep the CSV file for year-over-year comparison
- Re-run the analysis after each major event season
- Track if preferences change over time

## next steps after analysis

### events poll

1. **pick top 5 events** (3 on-campus, 2 off-campus)
2. **set frequency** based on majority preference
3. **schedule first event** at most popular time
4. **set budget** based on willingness to pay
5. **if 3D print interest >60%**, launch the 3D merch poll
6. **book venue** (The Barn/Stable) using contact info in main readme
7. **announce to department** with poll results summary

### 3D merch poll

1. **select top 3 insects** based on favorite_insects.png
2. **choose 3-5 products** that are quick to print and popular
3. **decide printing method** (buy resin printer if needed)
4. **create test designs** using free models or commission designer
5. **print test samples** and get feedback from committee
6. **set prices** based on cost + labor + fundraising margin
7. **create catalog** with photos of actual prints
8. **sell at first major event** (Halloween coffee, potluck, etc.)
9. **track sales** and adjust designs/prices as needed

## questions?

If you need help analyzing specific patterns or have questions about the data, the analysis script can be modified. The code is well-commented and easy to customize.
