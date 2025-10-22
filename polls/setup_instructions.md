# Poll Setup Instructions

## Coffee Hour Planning Survey

### Step 1: Create Google Form

1. Go to [Google Forms](https://forms.google.com)
2. Create a new blank form
3. Title: "Coffee Hour Planning Survey"
4. Description: "Help us plan the perfect coffee hour schedule for the UCR Entomology Department"

### Step 2: Add Questions

Copy the questions from `coffee-hour-questions.csv` in this order:

1. **What is your role in the department?** (Multiple choice, Required)
   - Faculty
   - Postdoc
   - Graduate Student
   - Undergraduate Student
   - Staff/Researcher
   - Visiting Scholar
   - Other

2. **How often should we hold coffee hours?** (Multiple choice, Required)
   - Three times a week
   - Weekly
   - Every two weeks
   - Once a month

3. **Which day(s) work best for you to attend coffee hour?** (Checkboxes, Required)
   - Monday
   - Tuesday
   - Wednesday
   - Thursday
   - Friday

4. **What time of day works best for you?** (Multiple choice, Required)
   - Morning (9 AM - 12 PM)
   - Afternoon (1 PM - 5 PM)

5. **If you selected Morning, which time slot works best?** (Multiple choice, Optional - use section logic)
   - 9:00-9:30 AM
   - 9:30-10:00 AM
   - 10:00-10:30 AM
   - 10:30-11:00 AM
   - 11:00-11:30 AM
   - 11:30 AM-12:00 PM
   - Any morning time

6. **If you selected Afternoon, which time slot works best?** (Multiple choice, Optional - use section logic)
   - 1:00-1:30 PM
   - 1:30-2:00 PM
   - 2:00-2:30 PM
   - 2:30-3:00 PM
   - 3:00-3:30 PM
   - 3:30-4:00 PM
   - 4:00-4:30 PM
   - 4:30-5:00 PM
   - Any afternoon time

7. **What type of coffee would you prefer?** (Checkboxes, Optional)
   - Drip/Pour-over coffee
   - Espresso-based drinks (latte, cappuccino)
   - Cold brew
   - French press
   - Instant coffee
   - Decaf options
   - I don't drink coffee

8. **What type of tea would you prefer?** (Checkboxes, Optional)
   - Black tea
   - Green tea
   - Herbal tea
   - Chai
   - Iced tea
   - I don't drink tea

9. **What food options would you like to see?** (Checkboxes, Optional)
   - Pastries and baked goods
   - Fresh fruits
   - Cultural foods from different countries
   - Gluten-free options
   - Vegan/Vegetarian options
   - No food needed

10. **Would you prefer indoor or outdoor coffee hours?** (Multiple choice, Required)
    - Indoor only
    - Outdoor only
    - Mix of both depending on weather
    - No preference

11. **Where would be the best location for coffee hour?** (Multiple choice, Required)
    - Courtyard
    - Building lobby/atrium
    - Rotating between labs
    - Department conference room
    - No preference

12. **Would your lab group be willing to host and provide food for a coffee hour? (We provide the coffee)** (Multiple choice, Required)
    - Yes, regularly
    - Yes, occasionally
    - Maybe, need to discuss with lab
    - No
    - Not applicable

13. **How long should coffee hour last?** (Multiple choice, Required)
    - 30 minutes
    - 45 minutes
    - 1 hour
    - 1.5 hours
    - Flexible/open-ended

14. **If you prefer background music, what type?** (Checkboxes, Optional)
    - Classical/Instrumental
    - Jazz
    - Cultural music from hosting lab
    - Ambient/Lo-fi
    - Seasonal music
    - No music, quiet conversation only

15. **What would prevent you from attending coffee hour?** (Checkboxes, Optional)
    - Class conflicts
    - Research commitments
    - Meeting conflicts
    - Location too far
    - Time doesn't work
    - Dietary restrictions not met
    - Other commitments

16. **Any additional suggestions for making coffee hour successful?** (Paragraph text, Optional)

### Step 3: Form Settings

1. Click Settings (gear icon)
2. Under "General":
   - ✓ Collect email addresses
   - ✓ Limit to 1 response
   - ✓ Restrict to users in University of California, Riverside and its trusted organizations
   - ✗ Edit after submit (unchecked)
3. Under "Presentation":
   - ✓ Show progress bar
   - Confirmation message: "Thank you for your feedback! We'll compile responses and share results at our first event in November."

### Step 4: Set Up Response Spreadsheet

1. Go to "Responses" tab
2. Click spreadsheet icon to create/link spreadsheet
3. Name it: "Coffee Hour Survey Responses"

### Step 5: Add Apps Script

1. In the Google Form, click three dots menu → Script editor
2. Delete default code
3. Copy entire contents of `coffee-hour-apps-script.js`
4. Paste into script editor
5. Update line 16: Replace `YOUR_SPREADSHEET_ID_HERE` with actual spreadsheet ID
   (Get ID from spreadsheet URL: docs.google.com/spreadsheets/d/**SPREADSHEET_ID**/edit)
6. Save (Ctrl+S or Cmd+S)
7. Name the project: "Coffee Hour Poll Handler"

### Step 6: Deploy as Web App (Optional - for additional features)

1. In Apps Script editor, click "Deploy" → "New Deployment"
2. Type: Web app
3. Execute as: Me
4. Who has access: Anyone with UCR account
5. Deploy and copy the Web App URL
6. Your deployed URL: `https://script.google.com/a/macros/ucr.edu/s/AKfycbzGZ2Ep6OIB1jQTdS0U9Y8h270s7zsb7RchVVUPKK7bEXGB5NutBVn0HB-hCm4O6Nrx/exec`

### Step 7: Set Up Trigger

1. In Apps Script editor, click "Triggers" (clock icon)
2. Click "+ Add Trigger"
3. Configure:
   - Choose function: `onFormSubmit`
   - Event source: From form
   - Event type: On form submit
4. Click "Save"
5. Authorize the script when prompted

### Step 7: Get Embed Code

1. In Google Form, click "Send" button
2. Click "< >" embed icon
3. Copy the iframe code
4. You'll get something like:
```html
<iframe src="https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform?embedded=true" width="640" height="2000" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
```

### Step 8: Update HTML Page

1. Open `poll-coffee-hour.html`
2. Replace the placeholder div with your iframe code
3. Adjust width to "100%" and height as needed:
```html
<iframe src="YOUR_GOOGLE_FORM_URL" width="100%" height="2000" frameborder="0" marginheight="0" marginwidth="0" style="border: 1px solid rgba(74, 144, 226, 0.2); border-radius: 8px;">Loading…</iframe>
```

### Step 9: Test

1. Submit a test response
2. Check that:
   - Response appears in spreadsheet
   - Confirmation email is sent (if email collected)
   - Admin notification is sent
   - Statistics sheet is updated

### Step 10: Share Form

The form will be embedded in the website, but you can also share direct link:
- Short URL: Create at https://forms.gle/YOUR_FORM_ID
- Full URL: https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform

## Events & Activities Poll

Follow the same steps for the second poll with different questions focused on:
- Types of social events preferred
- Frequency of different event types
- Budget considerations
- Venue preferences
- Special interest groups
- Professional development activities
- Seasonal celebrations

## Tips

- Keep forms concise (10-15 questions max)
- Use required fields sparingly
- Test on mobile devices
- Consider adding images to make forms more engaging
- Set up response validation where appropriate
- Enable "Show summary of responses" after submission to build engagement

## Troubleshooting

If emails aren't sending:
1. Check script authorization
2. Verify email addresses
3. Check Gmail quotas (100 emails/day for free accounts)

If trigger isn't working:
1. Delete and recreate trigger
2. Check for script errors in View → Executions
3. Make sure form is linked to script properly