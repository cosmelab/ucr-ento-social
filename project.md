# UCR Entomology Social Committee Website - Project Documentation

## Project Overview

The UCR Entomology Social Committee website serves as a central hub for fostering community within the Department of Entomology at UC Riverside. Established in September 2025, this platform coordinates social activities, facilitates communication, and builds connections among faculty, postdocs, graduate students, staff, and undergraduates.

## Website Purpose

**Primary Goals:**
1. Centralize information about department social events
2. Gather community input through interactive polls
3. Facilitate communication between committee and department members
4. Build a sense of community and belonging
5. Provide easy access to event details, RSVPs, and feedback channels

## Target Audience

- Department of Entomology faculty
- Graduate students and postdocs
- Research staff and specialists
- Undergraduate students
- Administrative staff
- Visiting researchers

## Core Features

### 1. Interactive Polls System
- Coffee Hour Planning Poll
- Events & Activities Preferences Poll
- 3D Print Merchandise Poll
- Real-time progress tracking
- Google Sheets backend integration
- Visual completion indicators

### 2. Events Management
- **NEW**: Events timeline page showcasing upcoming and past events
- Individual event detail pages
- Event flyers and promotional materials
- RSVP capabilities (future enhancement)
- Photo galleries from past events (future enhancement)

### 3. Email Communication System
- Professional HTML email templates
- Gmail API integration for sending announcements
- Consistent branding across all communications
- Dark-themed design matching website aesthetics
- Automated email scripts for committee use

### 4. Contact & Feedback
- Direct contact form with email notifications
- Anonymous feedback submission system
- Committee member directory
- Multiple communication channels

### 5. Visual Identity
- Custom blue and gold color scheme (UCR branding)
- Dark theme interface for modern, professional look
- Animated hero gallery with Ken Burns effect
- Responsive mobile-first design
- Interactive button animations with rotating insect icons

## Technical Stack

### Frontend
- HTML5 with semantic markup
- CSS3 (Grid, Flexbox, custom properties)
- Vanilla JavaScript (no framework dependencies)
- Inter font for typography
- Font Awesome for icons

### Backend Services
- Google Apps Script for form submissions
- Google Sheets for data storage
- Gmail API for email sending
- Google Analytics for visitor tracking

### Development Tools
- Git version control
- GitHub Pages for hosting
- Python 3 for email automation scripts
- Local development server (Python http.server)

## Project Structure

```
ucr-ento-social/
├── Core Pages
│   ├── index.html              # Landing page with animated gallery
│   ├── about.html              # Mission and committee members
│   ├── polls.html              # Poll directory
│   ├── events.html             # NEW: Events timeline
│   ├── contact.html            # Contact form
│   └── feedback.html           # Anonymous feedback
│
├── Poll Pages
│   ├── poll-coffee-hour.html   # Coffee hour planning
│   ├── poll-events.html        # Events preferences
│   └── poll-3d-merch.html      # Merchandise poll
│
├── Event Pages (NEW)
│   └── coffee-hour-halloween.html  # First event: Halloween Coffee Hour
│
├── Email Templates (NEW)
│   ├── poll-announcement.html      # Poll invitation template
│   ├── coffee-hour-announcement.html  # Event announcement template
│   ├── send-poll-announcement.py   # Poll email sender script
│   └── send-coffee-hour-announcement.py  # Event email sender script
│
├── Styling
│   ├── css/social.css          # Main stylesheet
│   ├── css/themes.css          # Theme variations
│   ├── css/mobile-nav.css      # Mobile navigation
│   ├── css/poll-form.css       # Poll styling
│   └── css/visitor-widget.css  # Analytics widget
│
├── Scripts
│   ├── js/main.js              # Navigation and gallery
│   ├── js/poll-progress.js     # Form tracking
│   └── js/visitor-counter.js   # Analytics
│
└── Assets
    ├── images/gallery/         # Slideshow images
    ├── images/headers/         # Page backgrounds
    ├── images/members/         # Committee photos
    ├── images/events/          # Event flyers
    ├── images/logos/           # UCR branding
    └── images/icons/           # Social Committee logo
```

## Design System

### Color Palette
- **Primary Blue**: `#4A90E2` (custom blue for buttons, links)
- **UCR Gold**: `#FFC947` (accent color, highlights)
- **Dark Background**: `#1a1a1a` (main background)
- **Card Background**: `#0d0d0d` (content cards)
- **Text Color**: `#e8e8e8` (pale turquoise, high contrast)
- **Cyan Accent**: `#00CED1` (body text, emphasis)
- **Dark Blue**: `#003DA5` (UCR official blue)
- **Orange**: `#FF8C00` (deadlines, urgent items)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Headings**: 600-700 weight
- **Body Text**: 400 weight
- **Navigation**: 500 weight

### Spacing System
- Section padding: 4rem top, 2rem bottom
- Card padding: 2rem
- Button padding: 0.75rem 2rem
- Consistent 1rem-2rem margins

## Current Phase: Events Integration - COMPLETED ✅

### Completed Features
- Three interactive polls with progress tracking
- Contact and feedback forms with email notifications
- Mobile-responsive navigation
- Visitor counter with Google Analytics
- Email template system with Gmail API integration
- Professional HTML email templates
- **NEW**: Full events system with timeline page
- **NEW**: Individual event detail pages
- **NEW**: Event email announcements
- **NEW**: Google Calendar .ics integration

### Halloween Coffee Hour Event Launch (October 17, 2025) ✅
Successfully launched the first Social Committee event with complete website and email integration:

1. **Events Timeline Page (events.html)**
   - Created timeline layout with upcoming/past events sections
   - Implemented alternating left-right card layout
   - Added year label styled as button-like badge with gradient
   - Timeline line positioned to start below headers (80px offset)
   - Year badge (2025) with z-index layering to cover timeline
   - Integrated animated Halloween ghost graphic
   - Event flyer displayed with proper sizing and hover effects

2. **Event Detail Page (coffee-hour-halloween.html)**
   - Full event information: Friday, October 31, 2025 at 9:30 AM
   - Location: Courtyard
   - Hosted by Mauck Lab with attribution link
   - Google Calendar .ics download integration
   - Event flyer with gray background for better visibility
   - Costume encouragement messaging
   - Responsive design matching site aesthetic

3. **Email Announcement System**
   - Created coffee-hour-announcement.html template
   - Dark-themed HTML email with inline CSS for compatibility
   - Gmail API integration via send-coffee-hour-announcement.py
   - Successfully sent to recipients:
     - TO: pol.sarkar@ucr.edu (for department forwarding)
     - CC: Social Committee members (cosme.simple@gmail.com, lcosme@gmail.com, andrelut@ucr.edu, mtana016@ucr.edu)
   - Email includes link to event details page
   - Calendar invite download prompt included

4. **Bug Fixes & Polish**
   - Fixed date correction: Thursday → Friday, October 31, 2025
   - Fixed white overscroll background (changed to black via html element in css/social.css)
   - Fixed missing images on GitHub Pages (.gitignore was blocking assets/images/events/)
   - Improved timeline layout to prevent line cutting through headers
   - Added responsive year label as styled badge
   - Verified .ics calendar file has correct date (DTSTART:20251031T163000Z)

### Technical Achievements
**Timeline Layout Innovation:**
```css
.timeline-line {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 3px;
    height: calc(100% - 80px);  /* Shortened to avoid header */
    top: 80px;  /* Start below "UPCOMING EVENTS" */
    background: linear-gradient(to bottom, var(--primary), var(--accent));
    opacity: 0.3;
}

.event-year-label {
    display: inline-block;
    background: linear-gradient(135deg, var(--bg-surface), #252525);
    color: var(--primary);
    font-size: 2rem;
    font-weight: 700;
    padding: 1rem 3rem;
    border-radius: 50px;
    border: 2px solid rgba(74, 144, 226, 0.4);
    box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    position: relative;
    z-index: 20;  /* Above timeline line */
    transition: all 0.3s ease;
}
```

**Overscroll Fix:**
```css
html {
    scroll-behavior: smooth;
    background-color: #000000;  /* Black background for overscroll */
}
```

**Git Configuration:**
- Uncommented `# assets/images/events/` in .gitignore
- Committed all event flyers and animation graphics
- Successfully deployed to GitHub Pages with all assets visible

### Next Event Planning Phase

## Future Roadmap

### Short-term (Next 2-3 months)
- [ ] Google Calendar integration
- [ ] Event RSVP system with capacity limits
- [ ] Photo galleries from events
- [ ] Email newsletter subscription
- [ ] Committee member portal

### Long-term (Next 6 months)
- [ ] Member login system
- [ ] Event planning resource library
- [ ] Budget tracking for events
- [ ] Volunteer sign-up system
- [ ] Archive of past events with photos

## Deployment

**Current Hosting**: GitHub Pages
**Live URL**: https://cosmelab.github.io/ucr-ento-social/
**Repository**: https://github.com/cosmelab/ucr-ento-social

### Deployment Process
1. Push changes to `main` branch
2. GitHub Actions automatically builds
3. Site updates within 1-2 minutes
4. No manual deployment needed

## Email System Workflow

### For Committee Members
1. Navigate to email-templates directory
2. Choose appropriate template (poll, event, general)
3. Edit HTML content as needed
4. Run Python script with miniforge Python
5. Authenticate if needed
6. Test send to personal email
7. Once approved, send to department list

### Email Templates Available
- **poll-announcement.html**: For announcing department polls
- **coffee-hour-announcement.html**: For event invitations
- **general-announcement.html**: For other communications

### Python Scripts
- **send-poll-announcement.py**: Sends poll invitations
- **send-coffee-hour-announcement.py**: Sends event announcements
- Both use Gmail API for perfect formatting preservation

## Collaboration Lab Partnership

**Mauck Lab Collaboration**
- First event hosted by Mauck Lab
- Halloween Coffee Hour sponsorship
- Professional flyer design
- Future rotation of lab sponsorships planned
- URL: https://maucklab.ucr.edu

## Success Metrics

### Engagement
- Poll participation rates (target: >50%)
- Event attendance (target: 20+ people)
- Website visitor count (tracked via Google Analytics)
- Feedback submission rate

### Technical Performance
- Page load time: <2 seconds
- Mobile responsiveness: 100%
- Email deliverability: >95%
- Form submission success rate: >98%

## Contact & Support

**Committee Chair**: Luciano Cosme (lcosme@ucr.edu)
**GitHub Issues**: https://github.com/cosmelab/ucr-ento-social/issues
**Department Website**: https://entomology.ucr.edu/

## License

© 2025 UCR Entomology Social Committee. All rights reserved.
Proprietary software - redistribution not permitted without consent.

---

**Last Updated**: October 17, 2025
**Version**: 1.1
**Status**: Active Development - Events Phase
