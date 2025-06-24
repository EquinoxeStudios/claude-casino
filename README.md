# Casino Website Generator

A Complete Dynamic Casino Website Generator that automatically creates fully-functional social casino websites with AI-powered content and real casino games.

## Features

### Core Functionality
- **AI-Powered Content Generation**: Uses OpenAI's GPT-4 for dynamic content creation
- **Real Casino Games**: Integrates with SlotsLaunch API for actual playable games
- **Custom Themes**: Generates 3 unique theme concepts based on domain analysis
- **Professional Design**: Creates cohesive color palettes and responsive layouts
- **Anti-Fingerprinting**: Advanced uniqueness features to ensure each site is unique

### Generated Content
- Complete homepage with hero sections, featured games, and about content
- Games listing page with filtering and search capabilities
- Individual game pages with embedded gameplay
- Legal pages (Terms, Privacy Policy, Responsible Gaming)
- About Us and Contact pages
- Sitemap, robots.txt, and other SEO files

### Technical Features
- **Responsive Design**: Mobile-first approach with fluid typography
- **Performance Optimized**: Concurrent image downloads and optimized API calls
- **SEO Ready**: Meta tags, canonical URLs, and structured data
- **Accessibility**: ARIA labels, semantic HTML, keyboard navigation
- **Cross-Browser**: Modern web standards with fallback support

## Installation

1. Clone or download the project files
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Add your API keys to `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
SLOTSLAUNCH_API_TOKEN=your_slotslaunch_token_here
```

## Usage

1. Run the main application:
```bash
python main.py
```

2. Enter your domain name when prompted (e.g., "mycasino.com")

3. Choose from deployment options:
   - Standard: Uses .html extensions
   - Traffic Armor: Uses folder structure with index.php files

4. Select from 3 AI-generated theme concepts

5. Wait for the complete website to be generated in the `output/` directory

## Project Structure

```
casino-generator/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── ai_content_generator.py # OpenAI integration for content generation
├── game_manager.py        # SlotsLaunch API integration
├── website_builder.py     # HTML/CSS/JS generation
├── unique_generator.py    # Anti-fingerprinting features
├── utils.py              # Helper functions
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## API Requirements

### OpenAI API
- GPT-4 access for content generation
- DALL-E 3 access for image generation
- Sufficient credits for content and image generation

### SlotsLaunch API
- Valid API token for game access
- Rate limiting compliance (built-in delays)

## Generated Website Structure

```
output/domain_name/
├── index.html           # Homepage
├── games.html          # Games listing
├── about.html          # About page
├── contact.html        # Contact page
├── terms.html          # Terms & Conditions
├── privacy.html        # Privacy Policy
├── responsible.html    # Responsible Gaming
├── css/               # Stylesheets
│   ├── base.css
│   ├── homepage.css
│   ├── games.css
│   ├── game.css
│   └── legal.css
├── js/                # JavaScript files
│   ├── base.js
│   ├── homepage.js
│   ├── games.js
│   └── game.js
├── images/            # Generated and downloaded images
│   ├── hero.jpg
│   ├── favicon.ico
│   └── games/
├── games/             # Individual game pages
│   └── [game-slug].html
├── sitemap.xml        # SEO sitemap
├── robots.txt         # Search engine directives
├── manifest.json      # Web app manifest
├── .htaccess         # Apache configuration
└── build.json        # Build information
```

## Customization

### Themes
The AI generates themes based on domain analysis, but you can modify theme generation in `ai_content_generator.py`:
- Adjust theme prompts for different styles
- Modify color palette generation
- Change font selection criteria

### Games Integration
Customize game handling in `game_manager.py`:
- Modify game processing logic
- Add custom game categories
- Implement custom game filtering

### Design System
Adjust design elements in `website_builder.py`:
- Modify CSS generation templates
- Change responsive breakpoints
- Update JavaScript functionality

### Anti-Fingerprinting
Configure uniqueness features in `unique_generator.py`:
- Adjust randomization levels
- Add custom obfuscation methods
- Modify comment injection patterns

## Legal Compliance

This generator creates **social casino websites for entertainment purposes only**:
- No real money gambling
- Includes required legal disclaimers
- Generates responsible gaming content
- Complies with social casino regulations

Ensure you understand and comply with all applicable laws and regulations in your jurisdiction before deploying any generated websites.

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your OpenAI API key is valid and has sufficient credits
   - Check your SlotsLaunch API token is active

2. **Generation Failures**
   - Check internet connectivity
   - Verify API rate limits haven't been exceeded
   - Review error messages in console output

3. **Missing Images**
   - Ensure sufficient OpenAI credits for DALL-E 3
   - Check image download permissions
   - Verify output directory write permissions

### Support
For issues, questions, or feature requests, please check the error logs and verify your API configurations.

## License

This project is for educational and development purposes. Ensure compliance with all applicable laws and API terms of service.

## Version History

- v1.0: Initial release with full casino website generation
- AI-powered content creation
- Real games integration
- Anti-fingerprinting features
- Professional responsive design