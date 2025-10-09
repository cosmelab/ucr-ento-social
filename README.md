# UCR Entomology Social Committee Website

A modern, responsive website for the UCR Entomology Department Social Committee, designed to facilitate community engagement, event planning, and anonymous feedback collection.

## Features

- **Event Planning & RSVP** - Interactive calendar and RSVP system for department social events
- **Polls & Surveys** - Active polls and surveys for gathering community input
- **Anonymous Suggestions** - Secure feedback system for department improvements
- **Modern Design** - Clean, professional styling with a cohesive color scheme
- **Mobile Responsive** - Works seamlessly on all devices

## Quick Start

1. Clone the repository
   ```bash
   git clone https://github.com/cosmelab/ucr-ento-social.git
   cd ucr-ento-social
   ```

2. Open `index.html` in your browser or use a local server:
   ```bash
   # Using Python
   python -m http.server 8000

   # Using Node.js
   npx serve

   # Or use VS Code Live Server extension
   ```

3. Visit `http://localhost:8000` in your browser

## Project Structure

```
ucr-ento-social/
├── css/                  # Styling files
│   ├── main.css         # Main theme styles
│   ├── components/      # Component styles
│   └── pages/           # Page-specific styles
├── js/                  # JavaScript functionality
│   └── main.js         # Navigation and interactions
├── assets/
│   └── images/         # Event photos and graphics
├── index.html          # Main hub page
├── events.html         # Event planning page
├── polls.html          # Active polls page
└── suggestions.html    # Anonymous feedback page
```

## Theme Customization

The website uses CSS variables for easy theme customization. Colors and styling can be easily modified by editing the CSS variables in the main stylesheet.

## Technologies

- HTML5 & CSS3
- Vanilla JavaScript
- Google Forms integration for data collection
- Google Apps Script for form processing
- Responsive design with CSS Grid and Flexbox

## Development

### Customizing the Theme

The site's appearance can be customized by editing CSS variables in `css/main.css`. This allows for easy theme changes without modifying the core structure.

### Adding New Pages

1. Create new HTML file based on existing structure
2. Link to `css/main.css` for consistent theming
3. Add navigation link in `js/main.js`
4. Use existing CSS classes for consistent styling

## Deployment

### GitHub Pages

1. Push code to GitHub
2. Go to Settings → Pages
3. Select source branch (main)
4. Site will be available at `https://cosmelab.github.io/ucr-ento-social/`

### Custom Domain (Optional)

1. Add CNAME file with your domain
2. Configure DNS settings with your provider
3. Enable HTTPS in GitHub Pages settings

## Contributing

We welcome contributions from the UCR Entomology community!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please maintain the existing code style and theme consistency.

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contact

UCR Entomology Department Social Committee

For questions or suggestions, please open an issue on GitHub.

## Acknowledgments

- UCR Entomology Department
- All committee members and contributors