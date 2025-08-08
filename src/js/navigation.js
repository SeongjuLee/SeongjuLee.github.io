// Navigation Component Loader
class NavigationLoader {
    constructor() {
        this.currentPage = this.getCurrentPage();
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('projects.html')) return 'projects';
        if (path.includes('publications.html')) return 'publications';
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

    setActiveState() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            // Set active based on current page
            if (this.currentPage === 'projects' && link.href.includes('projects.html')) {
                link.classList.add('active');
            } else if (this.currentPage === 'publications' && link.href.includes('publications.html')) {
                link.classList.add('active');
            } else if (this.currentPage === 'home' && link.href.includes('#hero')) {
                link.classList.add('active');
            }
        });
    }
}

// Initialize navigation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const navLoader = new NavigationLoader();
    navLoader.loadNavigation();
}); 