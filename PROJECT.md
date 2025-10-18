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

## Current Phase: Events Integration

### Completed Features
- Three interactive polls with progress tracking
- Contact and feedback forms with email notifications
- Mobile-responsive navigation
- Visitor counter with Google Analytics
- Email template system with Gmail API integration
- Professional HTML email templates

### Active Development (October 17, 2025)
1. **Events Timeline Page**
   - Create events.html modeled after lab website news.html structure
   - Timeline layout showing upcoming and past events
   - Visual cards for each event with images
   - Links to individual event detail pages

2. **First Event: Halloween Coffee Hour**
   - Individual event page (coffee-hour-halloween.html)
   - Event details: October 31, 9:30 AM, courtyard
   - Hosted by Mauck Lab (https://maucklab.ucr.edu)
   - Integration of event flyer images
   - RSVP information (costume encouraged!)

3. **Event Email System**
   - Email template for event announcements
   - Python script for sending event emails
   - Consistent branding with website
   - Testing workflow with personal email

### Next Steps (Priority Order)
1. Create events.html with timeline structure
2. Create coffee-hour-halloween.html event detail page
3. Create coffee-hour-announcement.html email template
4. Create send-coffee-hour-announcement.py script
5. Test email delivery to cosme.simple@gmail.com
6. After approval, send to department mailing list

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
