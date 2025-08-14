// Navigation and Footer Component Loader
// 
// IMPORTANT NOTES FOR ADDING NEW PAGES:
// =====================================
// 1. Add page detection in getCurrentPage() method:
//    - Add: if (path.includes('newpage.html')) return 'newpage';
//    - Make sure to add this BEFORE the 'return home;' line
//
// 2. Add navigation link in src/components/navigation.html:
//    - Add: <a href="newpage.html" class="nav-link">New Page</a>
//    - Place it in the appropriate position in the navigation menu
//
// 3. Add active state handling in setActiveState() method:
//    - Add: else if (this.currentPage === 'newpage' && link.href.includes('newpage.html'))
//    - This ensures the correct menu item is highlighted when on the new page
//
// 4. Page structure requirements:
//    - Use <div id="navigation-placeholder"> for navigation container
//    - Use <div id="footer-placeholder"> for footer container
//    - Include navigation.js script: <script src="../js/navigation.js"></script>
//    - Follow the same structure as existing pages (projects.html, publications.html, patents.html)
//
// 5. File organization:
//    - Place new page HTML files in src/pages/
//    - Place new page data JS files in src/js/
//    - Use consistent naming convention: pagename-data.js for data files
//
// 6. Common issues to avoid:
//    - Don't forget to add the page to getCurrentPage() - this causes 404 errors
//    - Don't forget to add navigation link - this breaks navigation flow
//    - Don't forget to add active state - this confuses users about current page
//    - Use correct relative paths for scripts and components
//
// =====================================

class NavigationLoader {
    constructor() {
        this.currentPage = this.getCurrentPage();
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('projects.html')) return 'projects';
        if (path.includes('publications.html')) return 'publications';
        if (path.includes('patents.html')) return 'patents';
        if (path.includes('awards.html')) return 'awards';
        if (path.includes('experiences.html')) return 'experiences';
        return 'home';
    }

    async loadNavigation() {
        try {
            let navigationPath;
            if (this.currentPage === 'home') {
                navigationPath = 'src/components/navigation-main.html';
            } else {
                navigationPath = '../components/navigation.html';
            }

            const response = await fetch(navigationPath);
            const navigationHtml = await response.text();
            
            // Replace the navigation placeholder
            const navPlaceholder = document.getElementById('navigation-placeholder');
            if (navPlaceholder) {
                navPlaceholder.innerHTML = navigationHtml;
            }

            // Set active state
            this.setActiveState();
            
        } catch (error) {
            console.error('Error loading navigation:', error);
        }
    }

    async loadFooter() {
        try {
            let footerPath;
            if (this.currentPage === 'home') {
                footerPath = 'src/components/footer.html';
            } else {
                footerPath = '../components/footer.html';
            }

            const response = await fetch(footerPath);
            const footerHtml = await response.text();
            
            // Replace the footer placeholder
            const footerPlaceholder = document.getElementById('footer-placeholder');
            if (footerPlaceholder) {
                footerPlaceholder.innerHTML = footerHtml;
            }
            
        } catch (error) {
            console.error('Error loading footer:', error);
        }
    }

    setActiveState() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            // Set active based on current page
            if (this.currentPage === 'projects' && link.href.includes('projects.html')) {
                link.classList.add('active');
            } else if (this.currentPage === 'publications' && link.href.includes('publications.html')) {
                link.classList.add('active');
            } else if (this.currentPage === 'patents' && link.href.includes('patents.html')) {
                link.classList.add('active');
            } else if (this.currentPage === 'awards' && link.href.includes('awards.html')) {
                link.classList.add('active');
            } else if (this.currentPage === 'experiences' && link.href.includes('experiences.html')) {
                link.classList.add('active');
            } else if (this.currentPage === 'home' && link.href.includes('#hero')) {
                link.classList.add('active');
            }
        });
    }
}

// Initialize navigation and footer when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const navLoader = new NavigationLoader();
    navLoader.loadNavigation();
    navLoader.loadFooter();
}); 