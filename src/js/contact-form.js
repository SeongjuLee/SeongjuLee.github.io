// Contact Form Handler using GitHub Issues API
// 
// This script handles the contact form submission by creating GitHub issues
// Users can send messages through the form and they will appear as issues in the repository
//
// Setup required:
// 1. Create a GitHub Personal Access Token with 'repo' permissions
// 2. Replace 'YOUR_GITHUB_TOKEN' with your actual token
// 3. Replace 'YOUR_USERNAME' and 'YOUR_REPO' with your GitHub details
// =====================================

class ContactFormHandler {
    constructor() {
        this.githubToken = 'YOUR_GITHUB_TOKEN'; // Replace with your token
        this.username = 'SeongjuLee'; // Replace with your GitHub username
        this.repo = 'SeongjuLee.github.io'; // Replace with your repository name
        this.form = document.getElementById('contactForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.statusDiv = document.getElementById('formStatus');
        
        this.init();
    }
    
    init() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.githubToken || this.githubToken === 'YOUR_GITHUB_TOKEN') {
            this.showStatus('GitHub token not configured. Please set up the token in contact-form.js', 'error');
            return;
        }
        
        const formData = new FormData(this.form);
        const name = formData.get('name');
        const email = formData.get('email');
        const subject = formData.get('subject');
        const message = formData.get('message');
        
        // Validate form
        if (!name || !email || !subject || !message) {
            this.showStatus('Please fill in all fields.', 'error');
            return;
        }
        
        if (!this.isValidEmail(email)) {
            this.showStatus('Please enter a valid email address.', 'error');
            return;
        }
        
        this.setLoading(true);
        
        try {
            await this.createGitHubIssue(name, email, subject, message);
            this.showStatus('Message sent successfully! I will get back to you soon.', 'success');
            this.form.reset();
        } catch (error) {
            console.error('Error sending message:', error);
            this.showStatus('Failed to send message. Please try again or contact me directly via email.', 'error');
        } finally {
            this.setLoading(false);
        }
    }
    
    async createGitHubIssue(name, email, subject, message) {
        const issueData = {
            title: `Contact Form: ${subject}`,
            body: this.formatIssueBody(name, email, subject, message),
            labels: ['contact-form', 'portfolio']
        };
        
        const response = await fetch(`https://api.github.com/repos/${this.username}/${this.repo}/issues`, {
            method: 'POST',
            headers: {
                'Authorization': `token ${this.githubToken}`,
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            },
            body: JSON.stringify(issueData)
        });
        
        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status}`);
        }
        
        return await response.json();
    }
    
    formatIssueBody(name, email, subject, message) {
        return `## Contact Form Submission

**From:** ${name}
**Email:** ${email}
**Subject:** ${subject}

**Message:**
${message}

---
*This message was sent through the portfolio contact form on ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}*`;
    }
    
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    setLoading(loading) {
        if (this.submitBtn) {
            this.submitBtn.disabled = loading;
            this.submitBtn.textContent = loading ? 'Sending...' : 'Send Message';
        }
    }
    
    showStatus(message, type) {
        if (this.statusDiv) {
            this.statusDiv.textContent = message;
            this.statusDiv.className = `text-${type === 'success' ? 'green' : 'red'}-600 text-sm mt-2`;
            this.statusDiv.style.display = 'block';
            
            // Auto-hide success messages after 5 seconds
            if (type === 'success') {
                setTimeout(() => {
                    this.statusDiv.style.display = 'none';
                }, 5000);
            }
        }
    }
}

// Alternative: Simple email link fallback
class SimpleContactForm {
    constructor() {
        this.form = document.getElementById('contactForm');
        this.init();
    }
    
    init() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }
    
    handleSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.form);
        const name = formData.get('name');
        const email = formData.get('email');
        const subject = formData.get('subject');
        const message = formData.get('message');
        
        // Validate form
        if (!name || !email || !subject || !message) {
            alert('Please fill in all fields.');
            return;
        }
        
        // Create mailto link
        const mailtoLink = `mailto:lsj2121@gm.gist.ac.kr?subject=${encodeURIComponent(`Portfolio Contact: ${subject}`)}&body=${encodeURIComponent(`Name: ${name}\nEmail: ${email}\nSubject: ${subject}\n\nMessage:\n${message}`)}`;
        
        // Open default email client
        window.open(mailtoLink);
        
        // Show success message
        alert('Opening your email client. Please send the message manually.');
        this.form.reset();
    }
}

// Initialize contact form when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Try GitHub Issues API first, fallback to simple email
    try {
        new ContactFormHandler();
    } catch (error) {
        console.log('GitHub Issues API not available, using simple email fallback');
        new SimpleContactForm();
    }
}); 