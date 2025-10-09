# UCR Entomology Social Committee Website Setup

## Project Structure
```
ucr-ento-social/
├── css/                  # Styling files (theme TBD)
│   ├── main.css         # Main theme styles
│   ├── components/      # Component styles
│   └── pages/           # Page-specific styles
├── js/                  # JavaScript files
│   └── main.js         # Navigation functionality
├── assets/
│   └── images/         # Images for events/gallery
├── assistant_rules.md   # Rules for AI assistance
└── index.html          # Main page (to be created)
```

## Potential Theme Options

### 1. Warm & Friendly (Orange/Coral)
- Primary: #FF6B6B or #FFA500
- Accent: #4ECDC4
- Background: #FFF5F5
- Good for: Creating welcoming, social atmosphere

### 2. Nature-Inspired (Green/Earth)
- Primary: #52B788
- Accent: #D4A574
- Background: #F8F9FA
- Good for: Reflecting entomology/nature connection

### 3. Modern & Clean (Blue/Gray)
- Primary: #4C6EF5
- Accent: #748FFC
- Background: #F8F9FA
- Good for: Professional, academic look

### 4. Vibrant & Fun (Teal/Magenta)
- Primary: #20C997
- Accent: #F06292
- Background: #FAFAFA
- Good for: Energetic social vibe

### 5. UCR Colors (Blue/Gold)
- Primary: #003DA5 (UCR Blue)
- Accent: #FFB81C (UCR Gold)
- Background: #FFFFFF
- Good for: University branding alignment

## To Create Initial Pages:

### 1. index.html - Main Hub
- Current polls/surveys section
- Quick links to all active forms
- Upcoming events preview
- Use the form-section styling from recruitment.html

### 2. events.html - Event Planning
- Calendar of upcoming events
- RSVP forms
- Event details cards

### 3. polls.html - Active Polls
- Embedded Google Forms
- Custom styled containers
- Progress indicators for multi-page forms

### 4. suggestions.html - Anonymous Feedback
- Anonymous suggestion box
- Uses Google Apps Script backend (like recruitment form)

## Google Forms Integration Options:

### Option A: Embedded iframe
```html
<div class="form-section">
    <iframe src="[Google Form URL]"
            width="100%"
            height="800"
            frameborder="0">
    </iframe>
</div>
```

### Option B: Custom Form (like recruitment.html)
- Full control over styling
- Uses Google Apps Script for backend
- More work but perfect theme match

## Quick Start Commands:
1. Initialize git: `git init`
2. Create GitHub repo: `gh repo create ucr-ento-social --public`
3. First commit: `git add . && git commit -m "Initial setup for social committee website"`
4. Push: `git push -u origin main`

## CSS Classes to Create:
- `.card` - Standard bordered cards
- `.form-section` - Form containers
- `.btn-primary` - Primary action buttons
- `.btn-secondary` - Secondary buttons
- `.hover-effect` - Hover animations

## Theme Implementation:
To implement chosen theme, create CSS variables in main.css:
```css
:root {
    --primary: [chosen primary color];
    --accent: [chosen accent color];
    --background: [chosen background];
    --text: [text color];
}
```

## Form Backend Setup:
1. Create Google Sheet for responses
2. Create Google Apps Script (Tools > Script editor)
3. Deploy as Web App
4. Update form action URL

## Notes:
- Navigation menu will need updating for social committee pages
- Consider adding event RSVP tracking
- Maybe add photo gallery for past events
- Could integrate with Google Calendar for events