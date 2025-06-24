# Casino Website Generator - Usage Guide

## Quick Start

### Option 1: Automatic Setup & Run
```bash
python quickstart.py
```
This will automatically set up everything and launch the generator.

### Option 2: Manual Setup
```bash
# 1. Run setup
python setup.py

# 2. Edit .env file with your API keys
# 3. Launch generator
python run.py
```

### Option 3: Direct Run (if already configured)
```bash
python main.py
```

## What You Need

### Required API Keys

1. **OpenAI API Key**
   - Sign up at https://platform.openai.com/
   - Get API key from dashboard
   - Ensure you have GPT-4 and DALL-E 3 access
   - Need sufficient credits (approximately $5-10 per website)

2. **SlotsLaunch API Token** (Optional)
   - Contact SlotsLaunch for API access
   - If not provided, will use demo games
   - Required for real casino games integration

### System Requirements
- Python 3.8 or higher
- Internet connection
- 500MB+ free disk space per generated website

## Generation Process

### Step 1: Domain Input
- Enter your desired domain name (e.g., "mycasino.com")
- Used for theme generation and branding

### Step 2: Deployment Type
- **Standard**: Regular .html files (most compatible)
- **Traffic Armor**: PHP folder structure for certain hosting

### Step 3: Theme Selection
- AI generates 3 unique themes based on your domain
- Choose the one that fits your vision
- Themes include color schemes, fonts, and visual style

### Step 4: Automated Generation
The system will automatically:
1. Generate design system and assets
2. Create hero images and favicon with DALL-E
3. Fetch real casino games from API
4. Generate all website content with AI
5. Build complete HTML/CSS/JS website
6. Apply anti-fingerprinting uniqueness features

### Step 5: Output
Your complete website will be in `output/[domain_name]/`

## Generated Website Features

### Pages Created
- **Homepage**: Hero section, featured games, about content
- **Games**: Full game library with filtering
- **Individual Game Pages**: Playable games with info
- **About**: Company information and story
- **Contact**: Contact form and information
- **Legal Pages**: Terms, Privacy, Responsible Gaming

### Technical Features
- **Responsive Design**: Works on all devices
- **SEO Optimized**: Meta tags, sitemap, structured data
- **Performance**: Optimized images and code
- **Accessibility**: WCAG compliant markup
- **Security**: CSP headers, XSS protection

### Unique Features
- **Anti-Fingerprinting**: Each site is uniquely obfuscated
- **Real Games**: Actual playable casino games
- **Professional Quality**: Production-ready code
- **Legal Compliance**: Social casino legal pages included

## Customization Options

### Modifying Themes
Edit `ai_content_generator.py` to adjust:
- Theme generation prompts
- Color palette preferences  
- Font selection criteria
- Content style and tone

### Game Integration
Modify `game_manager.py` to:
- Add custom game categories
- Implement different game filtering
- Customize game display options

### Design Changes
Update `website_builder.py` for:
- HTML template modifications
- CSS styling adjustments
- JavaScript functionality changes
- Page structure updates

### Uniqueness Features
Adjust `unique_generator.py` to:
- Change obfuscation levels
- Add custom randomization
- Modify comment injection patterns

## Troubleshooting

### Common Issues

**"API Key Invalid"**
- Verify your OpenAI API key is correct
- Check if you have GPT-4 access enabled
- Ensure sufficient API credits

**"Generation Failed"**
- Check internet connection
- Verify API rate limits not exceeded
- Review console error messages

**"No Games Found"**
- SlotsLaunch API token might be invalid
- API might be temporarily unavailable
- Fallback demo games will be used

**"Image Generation Failed"**
- DALL-E 3 might be unavailable
- Insufficient OpenAI credits
- Fallback placeholder images will be used

### File Permissions
If you get permission errors:
```bash
chmod +x *.py
```

### Python Dependencies
If modules are missing:
```bash
pip install -r requirements.txt --upgrade
```

## Best Practices

### Before Generation
- Ensure stable internet connection
- Have sufficient API credits
- Choose meaningful domain names
- Plan your website's purpose

### After Generation
- Review all generated content
- Test website functionality
- Verify legal compliance for your jurisdiction
- Customize content as needed

### Deployment
- Use professional web hosting
- Configure SSL certificates
- Set up proper DNS records
- Test mobile responsiveness

## Legal Considerations

### Social Casino Compliance
- Generated sites are for entertainment only
- No real money gambling features
- Includes responsible gaming information
- Legal disclaimers automatically included

### Content Ownership
- AI-generated content is typically public domain
- Images created with DALL-E follow OpenAI terms
- Casino games remain property of their providers
- Ensure compliance with local regulations

### API Usage
- Respect OpenAI API terms of service
- Follow SlotsLaunch API guidelines
- Monitor usage and costs
- Don't abuse rate limits

## Support

### Getting Help
1. Check this usage guide
2. Review README.md
3. Examine error messages carefully
4. Verify API configurations

### Common Solutions
- Restart the application
- Clear temporary files
- Update Python dependencies
- Check API key validity

Remember: Each generated website is unique and production-ready, but always review content and ensure legal compliance before deployment!