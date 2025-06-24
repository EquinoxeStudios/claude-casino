import asyncio
import requests
from pathlib import Path
from jinja2 import Template
from utils import create_directory, save_json, get_file_extension, slugify, print_colored
from colorama import Fore

class WebsiteBuilder:
    def __init__(self):
        self.templates = {}
        self.load_templates()
    
    def load_templates(self):
        """Load HTML templates"""
        self.templates = {
            'base': self.get_base_template(),
            'homepage': self.get_homepage_template(),
            'games': self.get_games_template(),
            'game_detail': self.get_game_detail_template(),
            'about': self.get_about_template(),
            'legal': self.get_legal_template(),
            'contact': self.get_contact_template()
        }
    
    async def build_website(self, output_dir, content, design_system, images, games, deployment_type="noip"):
        """Build complete website"""
        print_colored(f"🏗️ Building website in: {output_dir}", Fore.YELLOW)
        
        # Create directory structure
        self.create_directory_structure(output_dir)
        
        # Download and save images
        await self.download_images(images, output_dir)
        
        # Generate CSS and JS files
        await self.generate_assets(design_system, output_dir)
        
        # Generate HTML pages
        await self.generate_pages(output_dir, content, design_system, images, games, deployment_type)
        
        # Generate additional files
        self.generate_additional_files(output_dir, content, games)
        
        print_colored("✅ Website build completed!", Fore.GREEN)
    
    def create_directory_structure(self, output_dir):
        """Create website directory structure"""
        directories = [
            f"{output_dir}",
            f"{output_dir}/css",
            f"{output_dir}/js",
            f"{output_dir}/images",
            f"{output_dir}/images/games",
            f"{output_dir}/games"
        ]
        
        for directory in directories:
            create_directory(directory)
    
    async def download_images(self, images, output_dir):
        """Download hero image and favicon"""
        try:
            # Download hero image
            if images.get('hero_url'):
                hero_response = requests.get(images['hero_url'])
                if hero_response.status_code == 200:
                    with open(f"{output_dir}/images/hero.jpg", 'wb') as f:
                        f.write(hero_response.content)
                    print_colored("✅ Hero image downloaded", Fore.GREEN)
            
            # Download favicon
            if images.get('favicon_url'):
                favicon_response = requests.get(images['favicon_url'])
                if favicon_response.status_code == 200:
                    with open(f"{output_dir}/images/favicon.ico", 'wb') as f:
                        f.write(favicon_response.content)
                    print_colored("✅ Favicon downloaded", Fore.GREEN)
                        
        except Exception as e:
            print_colored(f"❌ Error downloading images: {e}", Fore.RED)
    
    async def generate_assets(self, design_system, output_dir):
        """Generate CSS and JavaScript files"""
        # Generate base CSS
        base_css = self.generate_base_css(design_system)
        with open(f"{output_dir}/css/base.css", 'w', encoding='utf-8') as f:
            f.write(base_css)
        
        # Generate homepage CSS
        homepage_css = self.generate_homepage_css(design_system)
        with open(f"{output_dir}/css/homepage.css", 'w', encoding='utf-8') as f:
            f.write(homepage_css)
        
        # Generate games CSS
        games_css = self.generate_games_css(design_system)
        with open(f"{output_dir}/css/games.css", 'w', encoding='utf-8') as f:
            f.write(games_css)
        
        # Generate game detail CSS
        game_css = self.generate_game_css(design_system)
        with open(f"{output_dir}/css/game.css", 'w', encoding='utf-8') as f:
            f.write(game_css)
        
        # Generate legal CSS
        legal_css = self.generate_legal_css(design_system)
        with open(f"{output_dir}/css/legal.css", 'w', encoding='utf-8') as f:
            f.write(legal_css)
        
        # Generate JavaScript files
        self.generate_javascript_files(output_dir)
        
        print_colored("✅ CSS and JS assets generated", Fore.GREEN)
    
    async def generate_pages(self, output_dir, content, design_system, images, games, deployment_type):
        """Generate all HTML pages"""
        ext = get_file_extension(deployment_type)
        
        # Generate homepage
        homepage_html = self.render_homepage(content, design_system, games)
        filename = f"index{ext}" if deployment_type == "noip" else "index.php"
        with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write(homepage_html)
        
        # Generate games listing page
        games_html = self.render_games_page(content, design_system, games)
        filename = f"games{ext}"
        with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write(games_html)
        
        # Generate individual game pages
        for game in games:
            game_html = self.render_game_detail_page(content, design_system, game, games)
            game_dir = f"{output_dir}/games/{game['slug']}"
            create_directory(game_dir)
            filename = f"index{ext}" if deployment_type == "traffic_armor" else f"{game['slug']}{ext}"
            filepath = f"{game_dir}/index{ext}" if deployment_type == "traffic_armor" else f"{output_dir}/games/{filename}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(game_html)
        
        # Generate about page
        about_html = self.render_about_page(content, design_system)
        filename = f"about{ext}"
        with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write(about_html)
        
        # Generate legal pages
        legal_pages = ['terms', 'privacy', 'responsible']
        for page in legal_pages:
            legal_html = self.render_legal_page(content, design_system, page)
            filename = f"{page}{ext}"
            with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
                f.write(legal_html)
        
        # Generate contact page
        contact_html = self.render_contact_page(content, design_system)
        filename = f"contact{ext}"
        with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write(contact_html)
        
        print_colored("✅ HTML pages generated", Fore.GREEN)
    
    def generate_additional_files(self, output_dir, content, games):
        """Generate additional files like sitemap, robots.txt, etc."""
        # Generate robots.txt
        robots_content = """User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /

Sitemap: /sitemap.xml"""
        
        with open(f"{output_dir}/robots.txt", 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        # Generate sitemap.xml
        sitemap_content = self.generate_sitemap(content, games)
        with open(f"{output_dir}/sitemap.xml", 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        # Generate manifest.json
        manifest = {
            "name": content['site_name'],
            "short_name": content['site_name'],
            "description": f"{content['site_name']} - Social Casino Games",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#1a1a2e",
            "icons": [
                {
                    "src": "images/favicon.ico",
                    "sizes": "32x32",
                    "type": "image/x-icon"
                }
            ]
        }
        
        save_json(manifest, f"{output_dir}/manifest.json")
        
        print_colored("✅ Additional files generated", Fore.GREEN)
    
    def render_homepage(self, content, design_system, games):
        """Render homepage HTML"""
        template = Template(self.templates['homepage'])
        return template.render(
            content=content,
            design_system=design_system,
            featured_games=games[:6],
            new_games=games[6:14] if len(games) > 6 else games
        )
    
    def render_games_page(self, content, design_system, games):
        """Render games listing page"""
        template = Template(self.templates['games']) 
        return template.render(
            content=content,
            design_system=design_system,
            games=games
        )
    
    def render_game_detail_page(self, content, design_system, game, all_games):
        """Render individual game detail page"""
        # Get similar games (same category, exclude current)
        similar_games = [g for g in all_games if g['category'] == game['category'] and g['id'] != game['id']][:4]
        
        template = Template(self.templates['game_detail'])
        return template.render(
            content=content,
            design_system=design_system,
            game=game,
            similar_games=similar_games
        )
    
    def render_about_page(self, content, design_system):
        """Render about page"""
        template = Template(self.templates['about'])
        return template.render(
            content=content,
            design_system=design_system
        )
    
    def render_legal_page(self, content, design_system, page_type):
        """Render legal pages"""
        template = Template(self.templates['legal'])
        return template.render(
            content=content,
            design_system=design_system,
            page_type=page_type
        )
    
    def render_contact_page(self, content, design_system):
        """Render contact page"""
        template = Template(self.templates['contact'])
        return template.render(
            content=content,
            design_system=design_system
        )
    
    def generate_sitemap(self, content, games):
        """Generate XML sitemap"""
        sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>/games.html</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>/about.html</loc>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>"""
        
        # Add game pages
        for game in games:
            sitemap += f"""
    <url>
        <loc>/games/{game['slug']}.html</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>"""
        
        sitemap += """
</urlset>"""
        return sitemap
    
    # Template definitions will be in separate methods for clarity
    def get_base_template(self):
        """Base HTML template structure"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ content.site_name }}{% endblock %}</title>
    <meta name="description" content="{% block description %}{{ content.site_name }} - Social Casino Games{% endblock %}">
    <link rel="icon" href="images/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="css/base.css">
    {% block additional_css %}{% endblock %}
</head>
<body>
    <header class="main-header">
        <nav class="navbar">
            <div class="nav-container">
                <a href="index.html" class="nav-logo">{{ content.site_name }}</a>
                <div class="nav-menu">
                    <a href="index.html" class="nav-link">Home</a>
                    <a href="games.html" class="nav-link">Games</a>
                    <a href="about.html" class="nav-link">About</a>
                    <a href="contact.html" class="nav-link">Contact</a>
                </div>
                <div class="nav-toggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer class="main-footer">
        <div class="footer-container">
            <div class="footer-section">
                <h3>{{ content.site_name }}</h3>
                <p>The best social casino experience</p>
            </div>
            <div class="footer-section">
                <h4>Legal</h4>
                <a href="terms.html">Terms & Conditions</a>
                <a href="privacy.html">Privacy Policy</a>
                <a href="responsible.html">Responsible Gaming</a>
            </div>
            <div class="footer-section">
                <h4>Support</h4>
                <a href="contact.html">Contact Us</a>
                <a href="about.html">About Us</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 {{ content.site_name }}. Entertainment only. No real money gambling.</p>
        </div>
    </footer>
    
    <script src="js/base.js"></script>
    {% block additional_js %}{% endblock %}
</body>
</html>"""
    
    def get_homepage_template(self):
        """Homepage template"""
        return """{% extends "base" %}

{% block additional_css %}
<link rel="stylesheet" href="css/homepage.css">
{% endblock %}

{% block content %}
<section class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">{{ content.pages.homepage.hero.headline }}</h1>
        <p class="hero-subtitle">{{ content.pages.homepage.hero.subheadline }}</p>
        <a href="games.html" class="cta-button">{{ content.pages.homepage.cta.button }}</a>
    </div>
    <div class="hero-image">
        <img src="images/hero.jpg" alt="Casino Hero" loading="lazy">
    </div>
</section>

<section class="featured-games">
    <div class="container">
        <h2>Featured Games</h2>
        <div class="games-grid">
            {% for game in featured_games %}
            <div class="game-card">
                <img src="{{ game.local_thumbnail or game.thumbnail }}" alt="{{ game.name }}" loading="lazy">
                <h3>{{ game.name }}</h3>
                <p>{{ game.provider }}</p>
                <a href="games/{{ game.slug }}.html" class="play-button">Play Now</a>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<section class="about-section">
    <div class="container">
        <h2>{{ content.pages.homepage.about.title }}</h2>
        <p>{{ content.pages.homepage.about.content }}</p>
    </div>
</section>

<section class="features-section">
    <div class="container">
        <h2>Why Choose Us</h2>
        <div class="features-grid">
            {% for feature in content.pages.homepage.features %}
            <div class="feature-card">
                <h3>{{ feature.title }}</h3>
                <p>{{ feature.description }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}

{% block additional_js %}
<script src="js/homepage.js"></script>
{% endblock %}"""
    
    def get_games_template(self):
        """Games listing template"""
        return """{% extends "base" %}

{% block title %}Games - {{ content.site_name }}{% endblock %}

{% block additional_css %}
<link rel="stylesheet" href="css/games.css">
{% endblock %}

{% block content %}
<section class="games-header">
    <div class="container">
        <h1>Casino Games</h1>
        <p>Choose from our collection of exciting casino games</p>
    </div>
</section>

<section class="games-listing">
    <div class="container">
        <div class="games-filters">
            <button class="filter-btn active" data-category="all">All Games</button>
            <button class="filter-btn" data-category="slots">Slots</button>
            <button class="filter-btn" data-category="table">Table Games</button>
            <button class="filter-btn" data-category="card">Card Games</button>
        </div>
        
        <div class="games-grid">
            {% for game in games %}
            <div class="game-card" data-category="{{ game.category }}">
                <img src="{{ game.local_thumbnail or game.thumbnail }}" alt="{{ game.name }}" loading="lazy">
                <div class="game-info">
                    <h3>{{ game.name }}</h3>
                    <p class="game-provider">{{ game.provider }}</p>
                    <div class="game-stats">
                        <span>RTP: {{ game.rtp }}</span>
                        <span>{{ game.volatility }} Vol.</span>
                    </div>
                    <a href="games/{{ game.slug }}.html" class="play-button">Play Now</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}

{% block additional_js %}
<script src="js/games.js"></script>
{% endblock %}"""
    
    def get_game_detail_template(self):
        """Game detail template"""
        return """{% extends "base" %}

{% block title %}{{ game.name }} - {{ content.site_name }}{% endblock %}

{% block additional_css %}
<link rel="stylesheet" href="css/game.css">
{% endblock %}

{% block content %}
<section class="game-header">
    <div class="container">
        <nav class="breadcrumb">
            <a href="../index.html">Home</a> > 
            <a href="../games.html">Games</a> > 
            <span>{{ game.name }}</span>
        </nav>
        <h1>{{ game.name }}</h1>
        <p class="game-provider">by {{ game.provider }}</p>
    </div>
</section>

<section class="game-play">
    <div class="container">
        <div class="game-frame">
            {{ game.demo_url | safe if game.demo_url else '<div class="game-placeholder">Game demo not available</div>' }}
        </div>
        <button class="fullscreen-btn">⛶ Fullscreen</button>
    </div>
</section>

<section class="game-info">
    <div class="container">
        <div class="game-details">
            <h2>Game Information</h2>
            <div class="info-grid">
                <div class="info-item">
                    <strong>RTP:</strong> {{ game.rtp }}
                </div>
                <div class="info-item">
                    <strong>Volatility:</strong> {{ game.volatility }}
                </div>
                <div class="info-item">
                    <strong>Paylines:</strong> {{ game.paylines }}
                </div>
                <div class="info-item">
                    <strong>Reels:</strong> {{ game.reels }}
                </div>
            </div>
            {% if game.description %}
            <p class="game-description">{{ game.description }}</p>
            {% endif %}
        </div>
    </div>
</section>

{% if similar_games %}
<section class="similar-games">
    <div class="container">
        <h2>Similar Games</h2>
        <div class="games-grid">
            {% for similar_game in similar_games %}
            <div class="game-card">
                <img src="{{ similar_game.local_thumbnail or similar_game.thumbnail }}" alt="{{ similar_game.name }}" loading="lazy">
                <h3>{{ similar_game.name }}</h3>
                <p>{{ similar_game.provider }}</p>
                <a href="{{ similar_game.slug }}.html" class="play-button">Play Now</a>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endif %}
{% endblock %}

{% block additional_js %}
<script src="../js/game.js"></script>
{% endblock %}"""
    
    def get_about_template(self):
        """About page template"""
        return """{% extends "base" %}

{% block title %}About - {{ content.site_name }}{% endblock %}

{% block content %}
<section class="page-header">
    <div class="container">
        <h1>{{ content.pages.about.title }}</h1>
    </div>
</section>

<section class="about-content">
    <div class="container">
        {% for section in content.pages.about.sections %}
        <div class="content-section">
            <h2>{{ section.title }}</h2>
            <p>{{ section.content }}</p>
        </div>
        {% endfor %}
    </div>
</section>
{% endblock %}"""
    
    def get_legal_template(self):
        """Legal pages template"""
        return """{% extends "base" %}

{% block title %}{{ content.pages.legal[page_type].title }} - {{ content.site_name }}{% endblock %}

{% block additional_css %}
<link rel="stylesheet" href="css/legal.css">
{% endblock %}

{% block content %}
<section class="page-header">
    <div class="container">
        <h1>{{ content.pages.legal[page_type].title }}</h1>
    </div>
</section>

<section class="legal-content">
    <div class="container">
        <div class="content-text">
            <p>{{ content.pages.legal[page_type].content }}</p>
        </div>
    </div>
</section>
{% endblock %}"""
    
    def get_contact_template(self):
        """Contact page template"""
        return """{% extends "base" %}

{% block title %}Contact - {{ content.site_name }}{% endblock %}

{% block content %}
<section class="page-header">
    <div class="container">
        <h1>Contact Us</h1>
    </div>
</section>

<section class="contact-content">
    <div class="container">
        <div class="contact-info">
            <h2>Get in Touch</h2>
            <p>Have questions? We'd love to hear from you!</p>
            <p>Email: support@{{ content.site_name.lower().replace(' ', '') }}.com</p>
        </div>
    </div>
</section>
{% endblock %}"""
    
    def generate_base_css(self, design_system):
        """Generate base CSS with design system"""
        return f"""/* Base Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --primary-color: {design_system['colors']['primary']};
    --secondary-color: {design_system['colors']['secondary']};
    --accent-color: {design_system['colors']['accent']};
    --background-color: {design_system['colors']['background']};
    --surface-color: {design_system['colors']['surface']};
    --text-primary: {design_system['colors']['text_primary']};
    --text-secondary: {design_system['colors']['text_secondary']};
    --success-color: {design_system['colors']['success']};
    --warning-color: {design_system['colors']['warning']};
    --error-color: {design_system['colors']['error']};
    
    --heading-font: '{design_system['typography']['heading_font']}', sans-serif;
    --body-font: '{design_system['typography']['body_font']}', sans-serif;
    
    --gradient-1: {design_system['gradients'][0]};
    --gradient-2: {design_system['gradients'][1] if len(design_system['gradients']) > 1 else design_system['gradients'][0]};
}}

@import url('https://fonts.googleapis.com/css2?family={design_system['typography']['heading_font'].replace(' ', '+')}:wght@400;500;600;700&family={design_system['typography']['body_font'].replace(' ', '+')}:wght@300;400;500&display=swap');

body {{
    font-family: var(--body-font);
    line-height: 1.6;
    color: var(--text-primary);
    background: var(--background-color);
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Navigation */
.main-header {{
    background: var(--primary-color);
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}}

.navbar {{
    padding: 1rem 0;
}}

.nav-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

.nav-logo {{
    font-family: var(--heading-font);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent-color);
    text-decoration: none;
}}

.nav-menu {{
    display: flex;
    gap: 2rem;
}}

.nav-link {{
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.nav-link:hover {{
    color: var(--accent-color);
}}

.nav-toggle {{
    display: none;
    flex-direction: column;
    cursor: pointer;
}}

.nav-toggle span {{
    width: 25px;
    height: 3px;
    background: var(--text-primary);
    margin: 3px 0;
    transition: 0.3s;
}}

/* Main Content */
main {{
    margin-top: 80px;
    min-height: calc(100vh - 160px);
}}

/* Buttons */
.cta-button, .play-button {{
    background: var(--gradient-1);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    display: inline-block;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}}

.cta-button:hover, .play-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}}

/* Footer */
.main-footer {{
    background: var(--primary-color);
    color: var(--text-primary);
    padding: 3rem 0 1rem;
    margin-top: 4rem;
}}

.footer-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}}

.footer-section h3, .footer-section h4 {{
    font-family: var(--heading-font);
    color: var(--accent-color);
    margin-bottom: 1rem;
}}

.footer-section a {{
    color: var(--text-secondary);
    text-decoration: none;
    display: block;
    margin-bottom: 0.5rem;
    transition: color 0.3s ease;
}}

.footer-section a:hover {{
    color: var(--accent-color);
}}

.footer-bottom {{
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--secondary-color);
    margin-top: 2rem;
    color: var(--text-secondary);
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .nav-menu {{
        display: none;
    }}
    
    .nav-toggle {{
        display: flex;
    }}
    
    .container {{
        padding: 0 15px;
    }}
}}"""
    
    def generate_homepage_css(self, design_system):
        """Generate homepage-specific CSS"""
        return f"""/* Homepage Styles */
.hero-section {{
    background: var(--gradient-1);
    padding: 6rem 0 4rem;
    display: flex;
    align-items: center;
    min-height: 600px;
}}

.hero-content {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}}

.hero-title {{
    font-family: var(--heading-font);
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    margin-bottom: 1rem;
    color: white;
}}

.hero-subtitle {{
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: rgba(255,255,255,0.9);
}}

.hero-image img {{
    width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}}

/* Featured Games */
.featured-games {{
    padding: 4rem 0;
    background: var(--surface-color);
}}

.featured-games h2 {{
    font-family: var(--heading-font);
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 3rem;
    color: var(--accent-color);
}}

.games-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}}

.game-card {{
    background: var(--primary-color);
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.game-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}}

.game-card img {{
    width: 100%;
    height: 200px;
    object-fit: cover;
}}

.game-card h3 {{
    font-family: var(--heading-font);
    padding: 1rem;
    margin: 0;
    color: var(--accent-color);
}}

.game-card p {{
    padding: 0 1rem;
    color: var(--text-secondary);
    margin: 0;
}}

.game-card .play-button {{
    margin: 1rem;
    width: calc(100% - 2rem);
    text-align: center;
}}

/* About Section */
.about-section {{
    padding: 4rem 0;
    text-align: center;
}}

.about-section h2 {{
    font-family: var(--heading-font);
    font-size: 2.5rem;
    margin-bottom: 2rem;
    color: var(--accent-color);
}}

.about-section p {{
    font-size: 1.1rem;
    max-width: 800px;
    margin: 0 auto;
    color: var(--text-secondary);
}}

/* Features Section */
.features-section {{
    padding: 4rem 0;
    background: var(--surface-color);
}}

.features-section h2 {{
    font-family: var(--heading-font);
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 3rem;
    color: var(--accent-color);
}}

.features-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}}

.feature-card {{
    background: var(--primary-color);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    transition: transform 0.3s ease;
}}

.feature-card:hover {{
    transform: translateY(-3px);
}}

.feature-card h3 {{
    font-family: var(--heading-font);
    color: var(--accent-color);
    margin-bottom: 1rem;
}}

.feature-card p {{
    color: var(--text-secondary);
}}

/* Responsive */
@media (max-width: 768px) {{
    .hero-content {{
        grid-template-columns: 1fr;
        text-align: center;
    }}
    
    .games-grid {{
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    }}
}}"""
    
    def generate_games_css(self, design_system):
        """Generate games page CSS"""
        return """/* Games Page Styles */
.games-header {
    background: var(--gradient-1);
    padding: 4rem 0 2rem;
    text-align: center;
    color: white;
}

.games-header h1 {
    font-family: var(--heading-font);
    font-size: 3rem;
    margin-bottom: 1rem;
}

.games-filters {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}

.filter-btn {
    background: var(--secondary-color);
    color: var(--text-primary);
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.filter-btn:hover,
.filter-btn.active {
    background: var(--accent-color);
    color: var(--primary-color);
}

.games-listing {
    padding: 2rem 0 4rem;
}

.games-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
}

.game-card {
    background: var(--primary-color);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.game-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

.game-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.game-info {
    padding: 1.5rem;
}

.game-info h3 {
    font-family: var(--heading-font);
    color: var(--accent-color);
    margin-bottom: 0.5rem;
}

.game-provider {
    color: var(--text-secondary);
    margin-bottom: 1rem;
}

.game-stats {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.play-button {
    width: 100%;
    text-align: center;
}"""
    
    def generate_game_css(self, design_system):
        """Generate game detail page CSS"""
        return """/* Game Detail Page Styles */
.game-header {
    background: var(--gradient-1);
    padding: 4rem 0 2rem;
    color: white;
}

.breadcrumb {
    margin-bottom: 1rem;
    font-size: 0.9rem;
}

.breadcrumb a {
    color: rgba(255,255,255,0.8);
    text-decoration: none;
}

.breadcrumb a:hover {
    color: white;
}

.game-header h1 {
    font-family: var(--heading-font);
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

.game-provider {
    font-size: 1.2rem;
    opacity: 0.8;
}

.game-play {
    padding: 2rem 0;
    text-align: center;
}

.game-frame {
    background: var(--surface-color);
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1rem;
    min-height: 600px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.game-placeholder {
    color: var(--text-secondary);
    font-size: 1.2rem;
}

.fullscreen-btn {
    background: var(--secondary-color);
    color: var(--text-primary);
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.fullscreen-btn:hover {
    background: var(--accent-color);
    color: var(--primary-color);
}

.game-info {
    padding: 4rem 0;
    background: var(--surface-color);
}

.game-details h2 {
    font-family: var(--heading-font);
    color: var(--accent-color);
    margin-bottom: 2rem;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.info-item {
    background: var(--primary-color);
    padding: 1rem;
    border-radius: 8px;
}

.info-item strong {
    color: var(--accent-color);
}

.game-description {
    font-size: 1.1rem;
    line-height: 1.8;
    color: var(--text-secondary);
}

.similar-games {
    padding: 4rem 0;
}

.similar-games h2 {
    font-family: var(--heading-font);
    color: var(--accent-color);
    margin-bottom: 2rem;
    text-align: center;
}"""
    
    def generate_legal_css(self, design_system):
        """Generate legal pages CSS"""
        return """/* Legal Pages Styles */
.page-header {
    background: var(--gradient-1);
    padding: 4rem 0 2rem;
    text-align: center;
    color: white;
}

.page-header h1 {
    font-family: var(--heading-font);
    font-size: 3rem;
}

.legal-content {
    padding: 4rem 0;
}

.content-text {
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.8;
    font-size: 1.1rem;
    color: var(--text-secondary);
}

.contact-content {
    padding: 4rem 0;
    text-align: center;
}

.contact-info h2 {
    font-family: var(--heading-font);
    color: var(--accent-color);
    margin-bottom: 2rem;
}

.contact-info p {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin-bottom: 1rem;
}"""
    
    def generate_javascript_files(self, output_dir):
        """Generate JavaScript files"""
        
        # Base JavaScript
        base_js = """// Base JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});"""
        
        # Homepage JavaScript
        homepage_js = """// Homepage specific functionality
document.addEventListener('DOMContentLoaded', function() {
    // Game cards hover effects
    const gameCards = document.querySelectorAll('.game-card');
    
    gameCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
});"""
        
        # Games page JavaScript
        games_js = """// Games page functionality
document.addEventListener('DOMContentLoaded', function() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const gameCards = document.querySelectorAll('.game-card');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Filter games
            gameCards.forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeIn 0.5s ease';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // Search functionality (if implemented)
    const searchInput = document.querySelector('#game-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            gameCards.forEach(card => {
                const gameName = card.querySelector('h3').textContent.toLowerCase();
                if (gameName.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}"""
        
        # Game detail JavaScript
        game_js = """// Game detail page functionality
document.addEventListener('DOMContentLoaded', function() {
    const fullscreenBtn = document.querySelector('.fullscreen-btn');
    const gameFrame = document.querySelector('.game-frame');
    
    if (fullscreenBtn && gameFrame) {
        fullscreenBtn.addEventListener('click', function() {
            if (gameFrame.requestFullscreen) {
                gameFrame.requestFullscreen();
            } else if (gameFrame.mozRequestFullScreen) {
                gameFrame.mozRequestFullScreen();
            } else if (gameFrame.webkitRequestFullscreen) {
                gameFrame.webkitRequestFullscreen();
            } else if (gameFrame.msRequestFullscreen) {
                gameFrame.msRequestFullscreen();
            }
        });
    }
    
    // Handle fullscreen change
    document.addEventListener('fullscreenchange', function() {
        if (document.fullscreenElement) {
            fullscreenBtn.textContent = '✕ Exit Fullscreen';
        } else {
            fullscreenBtn.textContent = '⛶ Fullscreen';
        }
    });
});"""
        
        # Write JavaScript files
        with open(f"{output_dir}/js/base.js", 'w', encoding='utf-8') as f:
            f.write(base_js)
        
        with open(f"{output_dir}/js/homepage.js", 'w', encoding='utf-8') as f:
            f.write(homepage_js)
        
        with open(f"{output_dir}/js/games.js", 'w', encoding='utf-8') as f:
            f.write(games_js)
        
        with open(f"{output_dir}/js/game.js", 'w', encoding='utf-8') as f:
            f.write(game_js)