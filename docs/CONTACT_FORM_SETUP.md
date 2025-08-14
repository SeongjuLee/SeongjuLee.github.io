# Contact Form Setup Guide

This guide explains how to set up the contact form to receive messages through GitHub Issues.

## 🚀 Option 1: GitHub Issues API (Recommended)

### Step 1: Create GitHub Personal Access Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "Portfolio Contact Form"
4. Select the following scopes:
   - `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

### Step 2: Configure the Contact Form

1. Open `src/js/contact-form.js`
2. Replace `YOUR_GITHUB_TOKEN` with your actual token:
   ```javascript
   this.githubToken = 'ghp_your_actual_token_here';
   ```
3. Update your GitHub username and repository name if different:
   ```javascript
   this.username = 'SeongjuLee'; // Your GitHub username
   this.repo = 'SeongjuLee.github.io'; // Your repository name
   ```

### Step 3: Test the Form

1. Deploy your website
2. Fill out the contact form
3. Submit the form
4. Check your GitHub repository's Issues tab
5. You should see a new issue created with the contact form message

### How It Works

- When someone submits the contact form, it creates a GitHub issue
- The issue title will be "Contact Form: [Subject]"
- The issue body contains the sender's information and message
- Issues are automatically labeled with "contact-form" and "portfolio"
- You'll receive email notifications for new issues

## 📧 Option 2: Simple Email Fallback

If you don't want to set up GitHub Issues, the form will automatically fall back to opening the user's email client:

1. User fills out the form
2. Form opens their default email client
3. Pre-fills the email with the form data
4. User sends the email manually

## 🔒 Security Considerations

### GitHub Token Security

- **Never commit your token to version control**
- Consider using environment variables or a secure configuration method
- The token has full repository access, so keep it secure
- You can revoke the token at any time in GitHub settings

### Alternative: Environment Variables

For better security, you can use environment variables:

```javascript
// In contact-form.js
this.githubToken = process.env.GITHUB_TOKEN || 'YOUR_GITHUB_TOKEN';
```

## 🛠️ Customization

### Customizing Issue Labels

You can modify the labels that are applied to contact form issues:

```javascript
// In contact-form.js, line ~85
labels: ['contact-form', 'portfolio', 'urgent'] // Add your own labels
```

### Customizing Issue Template

You can modify the issue body format:

```javascript
// In contact-form.js, formatIssueBody method
formatIssueBody(name, email, subject, message) {
    return `## New Contact Form Message

**From:** ${name}
**Email:** ${email}
**Subject:** ${subject}
**Date:** ${new Date().toLocaleString()}

**Message:**
${message}

---
*Sent via portfolio contact form*`;
}
```

### Adding Form Validation

The form already includes basic validation, but you can add more:

```javascript
// Add custom validation rules
if (message.length < 10) {
    this.showStatus('Message must be at least 10 characters long.', 'error');
    return;
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"GitHub token not configured"**
   - Make sure you've replaced `YOUR_GITHUB_TOKEN` with your actual token

2. **"GitHub API error: 401"**
   - Your token might be invalid or expired
   - Generate a new token and update the configuration

3. **"GitHub API error: 403"**
   - Your token doesn't have the required permissions
   - Make sure you selected the `repo` scope

4. **"GitHub API error: 404"**
   - Check that your username and repository name are correct
   - Make sure the repository exists and is accessible

### Debug Mode

To enable debug logging, add this to your contact form:

```javascript
// Add to ContactFormHandler constructor
this.debug = true; // Enable debug mode

// Add to handleSubmit method
if (this.debug) {
    console.log('Form data:', { name, email, subject, message });
}
```

## 📱 Alternative Solutions

### 1. Netlify Forms
If you're using Netlify, you can use their built-in form handling:
- Add `netlify` attribute to your form
- Messages will be available in your Netlify dashboard

### 2. Formspree
Use Formspree service:
- Sign up at [formspree.io](https://formspree.io)
- Replace form action with your Formspree endpoint

### 3. EmailJS
Use EmailJS for client-side email sending:
- Sign up at [emailjs.com](https://emailjs.com)
- Configure email templates
- Send emails directly from the browser

## 📞 Support

If you need help setting up the contact form:

1. Check the browser console for error messages
2. Verify your GitHub token has the correct permissions
3. Test with a simple message first
4. Check your GitHub repository's Issues tab

For additional support, please create an issue in this repository. 