# UCR Entomology Social Committee Website

> Building community through shared experiences in the Department of Entomology at UC Riverside

[![UC Riverside](https://img.shields.io/badge/UC%20Riverside-003DA5?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdOb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIGZpbGw9IiMwMDNEQTUiLz48L3N2Zz4=)](https://www.ucr.edu)
[![Department](https://img.shields.io/badge/Entomology-FFC947?style=flat)](https://entomology.ucr.edu/)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/cosmelab/ucr-ento-social)

## Overview

The official website for the UCR Entomology Social Committee, established in September 2025. This platform serves as a central hub for department social activities, fostering collaboration and community among faculty, postdocs, graduate students, and staff.

## Live Website

Visit the site: [https://cosmelab.github.io/ucr-ento-social/](https://cosmelab.github.io/ucr-ento-social/)

## Key Features

### 🎨 Visual Design
- **Animated Hero Gallery** - Ken Burns effect slideshow featuring 12 department images
- **Custom Theme System** - UCR-branded blue and gold color scheme with dark mode interface
- **Interactive Elements** - Button animations with rotating insect icons on hover
- **Responsive Layout** - Fully optimized mobile navigation with collapsible hamburger menu
- **Progress Tracking** - Visual progress indicators for poll completion

### 📱 Core Functionality
- **Member Directory** - Complete committee roster with contact information
- **Interactive Polls** - Three comprehensive surveys with real-time progress tracking:
  - Coffee Hour Planning Poll
  - Events & Activities Poll
  - 3D Print Merchandise Poll
- **Contact Form** - Direct communication with committee via Google Apps Script
- **Feedback System** - Anonymous suggestion submission with email notifications
- **Visitor Analytics** - Real-time visitor counter with Google Analytics integration

## Technical Architecture

### Frontend Stack
```
HTML5                  - Semantic markup structure
CSS3                   - Custom properties, Grid/Flexbox layouts
Vanilla JavaScript     - No framework dependencies
Google Apps Script     - Form submission backend
Google Analytics       - Visitor tracking
Inter Font             - Professional typography
```

### Design System
- **Primary Color**: `#4A90E2` (Custom Blue)
- **Accent Color**: `#FFC947` (UCR Gold)
- **Background**: Dark theme (`#1a1a1a`)
- **Text**: High contrast pale turquoise (`#e8e8e8`)

### Performance
- Optimized images (1200px max width)
- Minimal dependencies (no frameworks)
- CSS-based animations (GPU accelerated)
- Fast load times (<2 seconds)

## Project Structure

```
ucr-ento-social/
├── 📄 Core Pages
│   ├── index.html              # Landing page with animated gallery
│   ├── about.html              # Mission and committee members
│   ├── polls.html              # Poll directory
│   ├── poll-coffee-hour.html   # Coffee hour planning survey
│   ├── poll-events.html        # Events & activities survey
│   ├── poll-3d-merch.html      # 3D merchandise survey
│   ├── contact.html            # Contact form with email notifications
│   └── feedback.html           # Anonymous feedback submission
│
├── 🎨 Styling
│   ├── css/
│   │   ├── social.css          # Main stylesheet
│   │   ├── themes.css          # Theme variations
│   │   ├── mobile-nav.css      # Mobile navigation overrides
│   │   ├── poll-form.css       # Poll form styling
│   │   ├── progress-circle.css # Progress indicator
│   │   └── visitor-widget.css  # Visitor counter
│
├── ⚡ Scripts
│   └── js/
│       ├── main.js             # Navigation and gallery
│       ├── poll-progress.js    # Form completion tracking
│       └── visitor-counter.js  # Analytics integration
│
├── 📁 Assets
│   └── images/
│       ├── gallery/            # Slideshow images
│       ├── headers/            # Page backgrounds
│       ├── members/            # Committee photos
│       ├── logos/              # UCR branding
│       ├── icons/              # Social Committee logo
│       └── backgrounds/        # Textures
│
└── 🔧 Configuration
    ├── robots.txt              # SEO directives
    ├── sitemap.xml             # Site structure
    └── .gitignore              # Version control
```

## Installation & Development

### Quick Start
```bash
# Clone repository
git clone https://github.com/cosmelab/ucr-ento-social.git
cd ucr-ento-social

# Serve locally (choose one)
python -m http.server 8000        # Python 3
npx http-server                   # Node.js
# Or use VS Code Live Server extension
```

### Development Guidelines

#### Adding Pages
1. Duplicate existing page template
2. Update navigation in all HTML files
3. Add custom header background to `assets/images/headers/`
4. Maintain consistent margin/padding (4rem top, 2rem bottom)

#### Styling Updates
```css
/* Edit CSS variables in social.css */
:root {
    --primary: #4A90E2;        /* Main blue */
    --accent: #FFC947;         /* Gold accent */
    --bg-dark: #1a1a1a;        /* Background */
    --text-card: #e8e8e8;      /* Body text */
}
```

#### Image Specifications
- **Gallery**: 1200px width, PNG format
- **Members**: 400x400px, circular crop
- **Headers**: 1920px width, 15% opacity

## Committee Information

### Leadership
- **Chair**: Luciano Cosme (Faculty)

### Members
- Faculty Representatives (3)
- Project Scientists (2)
- Assistant Specialist (1)
- Graduate Student (1)
- Undergraduate Student (1)

View full committee details on the [About page](https://cosmelab.github.io/ucr-ento-social/about.html).

## Deployment

### GitHub Pages (Current)
The site is automatically deployed via GitHub Pages:
1. Push changes to `main` branch
2. GitHub Actions builds and deploys
3. Live at: https://cosmelab.github.io/ucr-ento-social/

### Custom Domain Setup
```bash
# Add CNAME file
echo "social.entomology.ucr.edu" > CNAME
# Configure DNS with domain provider
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS 14+, Android 10+)

## Contributing

We welcome contributions from the UCR Entomology community.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-event`)
3. Commit changes (`git commit -m 'Add new event type'`)
4. Push to branch (`git push origin feature/new-event`)
5. Open a Pull Request

### Code Standards
- Use semantic HTML5 elements
- Follow existing CSS naming conventions
- Maintain responsive design principles
- Test on multiple devices before submitting

## Recent Updates

### October 2025
- ✅ Added three interactive polls with Google Sheets backend
- ✅ Implemented progress circle tracking for poll completion
- ✅ Connected contact and feedback forms to Google Apps Script
- ✅ Added email notifications for form submissions
- ✅ Optimized mobile navigation with fixed header
- ✅ Integrated visitor counter with Google Analytics
- ✅ Added SEO improvements (robots.txt, sitemap.xml)

## Future Roadmap

- [ ] Google Calendar integration for events
- [ ] Event RSVP system with capacity limits
- [ ] Photo gallery from past social events
- [ ] Newsletter subscription
- [ ] Resource library for event planning
- [ ] Member portal with login

## License

© 2025 UCR Entomology Social Committee. All rights reserved.

This project is proprietary software. Redistribution is not permitted without explicit written consent.

## Acknowledgments

- UC Riverside Department of Entomology
- Social Committee volunteers
- Department faculty and students for feedback
- UCR IT Services for hosting support

## Contact

**Website Issues**: Open an [issue](https://github.com/cosmelab/ucr-ento-social/issues)
**Committee Contact**: [lcosme@ucr.edu](mailto:lcosme@ucr.edu)
**Department**: [entomology.ucr.edu](https://entomology.ucr.edu/)

---

*Last Updated: October 2025*