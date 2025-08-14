# AI Researcher Portfolio

A modern, responsive portfolio website for AI researchers at GIST AI Convergence Laboratory.

## 🚀 Live Demo

[View on GitHub Pages](https://seongjulee.github.io)

## 📋 Project Information

- **Tech Stack**: HTML5, CSS3, JavaScript (ES6+), Tailwind CSS
- **Deployment**: GitHub Pages
- **Responsive Design**: Mobile, tablet, and desktop optimized
- **Icons**: Font Awesome, Lucide Icons
- **Fonts**: Inter (Google Fonts)

## 🛠️ Local Development

1. Clone the repository
```bash
git clone https://github.com/SeongjuLee/SeongjuLee.github.io.git
cd SeongjuLee.github.io
```

2. Open `index.html` in your browser or use a local server
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000
```

## 📁 Project Structure

```
SeongjuLee.github.io/
├── index.html                    # Main homepage
├── test.sh                      # Test script
├── .gitignore                   # Git ignore rules
├── docs/
│   └── README.md               # Project documentation
├── assets/                      # Static assets
│   ├── images/                 # Image files
│   │   ├── profile/           # Profile pictures
│   │   ├── icons/             # Icon images
│   │   ├── papers/            # Publication images
│   │   └── projects/          # Project images
│   ├── css/                   # Custom CSS files
│   ├── fonts/                 # Font files
│   └── media/                 # Media files
└── src/                        # Source code
    ├── components/             # Reusable HTML components
    │   ├── navigation.html    # Sub-page navigation
    │   ├── navigation-main.html # Main page navigation
    │   └── footer.html        # Common footer
    ├── pages/                 # Individual page files
    │   ├── projects.html      # Projects page
    │   ├── publications.html  # Publications page
    │   ├── patents.html       # Patents page
    │   ├── awards.html        # Awards page
    │   └── experiences.html   # Experiences page
    ├── js/                    # JavaScript files
    │   ├── navigation.js      # Navigation and footer loader
    │   ├── projects-data.js   # Projects data
    │   ├── publications-data.js # Publications data
    │   ├── patents-data.js    # Patents data
    │   ├── awards-data.js     # Awards data
    │   ├── experiences-data.js # Experiences data
    │   └── education-data.js  # Education data
    ├── data/                  # Additional data files
    └── hidden/                # Hidden files
```

## 🎨 Key Features

- **Responsive Design**: Optimized experience across all devices
- **Modern UI/UX**: Glass morphism effects, smooth animations, and hover effects
- **Modular Architecture**: Reusable components for navigation and footer
- **Dynamic Content Loading**: JavaScript-based content management
- **Section Navigation**: Smooth scrolling between sections
- **Social Media Integration**: Links to academic and professional profiles
- **Contact Form**: Interactive contact form with validation
- **Custom Cursor**: Enhanced user experience with custom cursor effects

## 📝 Page Structure

### Main Page (`index.html`)
1. **Hero Section**: Introduction and call-to-action
2. **About Me**: Personal introduction and research interests
3. **Education**: Academic background and timeline
4. **Research Projects**: Featured research projects with cards
5. **Selected Publications**: Highlighted academic publications
6. **Contact**: Contact information and message form

### Sub Pages
- **Projects** (`src/pages/projects.html`): Complete list of research projects
- **Publications** (`src/pages/publications.html`): All academic publications with filtering
- **Patents** (`src/pages/patents.html`): Patent applications and registrations
- **Awards** (`src/pages/awards.html`): Awards and honors received
- **Experiences** (`src/pages/experiences.html`): Professional experiences and positions

## 🔧 Customization

### Adding New Pages
1. Create HTML file in `src/pages/`
2. Add data file in `src/js/` (e.g., `newpage-data.js`)
3. Update `src/js/navigation.js`:
   - Add page detection in `getCurrentPage()`
   - Add active state handling in `setActiveState()`
4. Add navigation link in `src/components/navigation.html`
5. Add main page link in `src/components/navigation-main.html`

### Modifying Content
- **Personal Information**: Update data files in `src/js/`
- **Styling**: Modify Tailwind classes or add custom CSS
- **Images**: Replace images in `assets/images/`
- **Social Links**: Update links in `src/components/footer.html`

### Component System
- **Navigation**: Automatically loads based on current page
- **Footer**: Common footer across all pages
- **Data Management**: Centralized data files for easy updates

## 🎯 Technical Details

### CSS Framework
- **Tailwind CSS**: Utility-first CSS framework
- **Custom Animations**: Keyframe animations for interactive elements
- **Glass Morphism**: Modern glass card effects
- **Gradient Text**: Custom gradient text effects

### JavaScript Features
- **Dynamic Content Loading**: Fetch and render content from data files
- **Navigation Management**: Automatic page detection and active state
- **Component Loading**: Modular component system
- **Form Handling**: Contact form with validation
- **Smooth Scrolling**: Enhanced navigation experience

### Performance Optimizations
- **CDN Resources**: External libraries loaded from CDN
- **Lazy Loading**: Images and components loaded on demand
- **Minimal Dependencies**: Lightweight framework usage
- **Responsive Images**: Optimized for different screen sizes

## 📄 License

MIT License

---

## 🧪 Testing

Run the test script:
```bash
./test.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Contact

For questions or suggestions, please contact:
- **Email**: lsj2121@gm.gist.ac.kr
- **GitHub**: [@SeongjuLee](https://github.com/SeongjuLee)
- **Google Scholar**: [Seongju Lee](https://scholar.google.com/citations?user=Q0LR04AAAAAJ&hl=ko&oi=ao)