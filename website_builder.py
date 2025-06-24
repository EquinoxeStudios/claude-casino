import asyncio
import requests
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader
from utils import create_directory, save_json, get_file_extension, slugify, print_colored
from colorama import Fore

class WebsiteBuilder:
    def __init__(self):
        # Use FileSystemLoader to load external template files
        template_dir = Path(__file__).parent  # Current directory where templates are located
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.filters['safe'] = lambda x: x  # Add safe filter for HTML content
    
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
        """Generate CSS and JavaScript files for the new template structure"""
        # Generate main stylesheet that matches the template design
        main_css = self.generate_main_css(design_system)
        with open(f"{output_dir}/css/style.css", 'w', encoding='utf-8') as f:
            f.write(main_css)
        
        # Generate JavaScript files for sidebar and game functionality
        self.generate_template_javascript_files(output_dir)
        
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
        template = self.env.get_template('homepage_template.html')
        
        # Prepare data structure for the template
        template_data = {
            'site_name': content['site_name'],
            'site_tagline': 'Social Casino Games',
            'canonical_url': '/',
            'favicon_path': 'images/favicon.ico',
            'primary_font': design_system['typography']['heading_font'],
            'hero': {
                'title': content['pages']['homepage']['hero']['headline'],
                'description': content['pages']['homepage']['hero']['subheadline'],
                'background_image': 'images/hero.jpg',
                'overlay_opacity': 0.6,
                'cta_text': content['pages']['homepage']['cta']['button'],
                'cta_url': '/games.html',
                'cta_icon': 'fas fa-play'
            },
            'content_sections': [
                {
                    'subtitle': 'Most popular games on our platform',
                    'items': [self.format_game_for_template(game) for game in games[:6]]
                },
                {
                    'subtitle': 'Latest additions to our game collection', 
                    'items': [self.format_game_for_template(game) for game in games[6:12] if len(games) > 6]
                }
            ],
            'about': {
                'content': content['pages']['homepage']['about']['content'].split('\n')
            },
            'about_url': '/about.html',
            'contact_url': '/contact.html',
            'terms_url': '/terms.html',
            'privacy_url': '/privacy.html',
            'cookies_url': '/cookies.html',
            'responsible_url': '/responsible.html',
            'footer': {
                'disclaimer': {
                    'title': 'Disclaimer',
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return template.render(**template_data)
    
    def format_game_for_template(self, game):
        """Format game data for template usage"""
        return {
            'title': game.get('name', 'Unknown Game'),
            'image': game.get('local_thumbnail', game.get('thumbnail', 'images/placeholder-game.jpg')),
            'url': f"/games/{game.get('slug', 'unknown')}.html",
            'slug': game.get('slug', 'unknown'),
            'provider': game.get('provider', 'Unknown'),
            'cta_text': 'Play Now'
        }
    
    def render_games_page(self, content, design_system, games):
        """Render games listing page"""
        template = self.env.get_template('games_template.html')
        
        template_data = {
            'site_name': content['site_name'],
            'canonical_url': '/games.html',
            'favicon_path': 'images/favicon.ico',
            'primary_font': design_system['typography']['heading_font'],
            'total_games': len(games),
            'all_games': [self.format_game_for_template(game) for game in games],
            'path_prefix': '',
            'about_url': '/about.html',
            'contact_url': '/contact.html',
            'terms_url': '/terms.html',
            'privacy_url': '/privacy.html',
            'cookies_url': '/cookies.html',
            'responsible_url': '/responsible.html',
            'footer': {
                'disclaimer': {
                    'title': 'Disclaimer',
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return template.render(**template_data)
    
    def render_game_detail_page(self, content, design_system, game, all_games):
        """Render individual game detail page"""
        # Get similar games (same category, exclude current)
        similar_games = [g for g in all_games if g['category'] == game['category'] and g['id'] != game['id']][:4]
        
        template = self.env.get_template('game_template.html')
        
        template_data = {
            'site_name': content['site_name'],
            'canonical_url': f'/games/{game.get("slug", "unknown")}.html',
            'favicon_path': '../images/favicon.ico',
            'primary_font': design_system['typography']['heading_font'],
            'game': {
                'title': game.get('name', 'Unknown Game'),
                'iframe_url': game.get('demo_url', 'about:blank')
            },
            'about_url': '/about.html',
            'contact_url': '/contact.html',
            'terms_url': '/terms.html',
            'privacy_url': '/privacy.html',
            'cookies_url': '/cookies.html',
            'responsible_url': '/responsible.html',
            'footer': {
                'disclaimer': {
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return template.render(**template_data)
    
    def render_about_page(self, content, design_system):
        """Render about page"""
        template = self.env.get_template('about_template.html')
        
        template_data = {
            'site_name': content['site_name'],
            'canonical_url': '/about.html',
            'favicon_path': 'images/favicon.ico',
            'primary_font': design_system['typography']['heading_font'],
            'about_sections': content['pages']['about']['sections'],
            'about_url': '/about.html',
            'contact_url': '/contact.html',
            'terms_url': '/terms.html',
            'privacy_url': '/privacy.html',
            'cookies_url': '/cookies.html',
            'responsible_url': '/responsible.html',
            'footer': {
                'disclaimer': {
                    'title': 'Disclaimer',
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return template.render(**template_data)
    
    def render_legal_page(self, content, design_system, page_type):
        """Render legal pages"""
        template = self.env.get_template('legal_template.html')
        
        legal_titles = {
            'terms': 'Terms & Conditions',
            'privacy': 'Privacy Policy',
            'responsible': 'Responsible Gaming'
        }
        
        template_data = {
            'site_name': content['site_name'],
            'canonical_url': f'/{page_type}.html',
            'favicon_path': 'images/favicon.ico',
            'primary_font': design_system['typography']['heading_font'],
            'page_title': legal_titles.get(page_type, 'Legal Information'),
            'page_subtitle': f'Please read our {legal_titles.get(page_type, "legal information")} carefully.',
            'page_type': page_type,
            'content': content['pages']['legal'][page_type]['content'],
            'last_updated': '2024-01-01',
            'about_url': '/about.html',
            'contact_url': '/contact.html',
            'terms_url': '/terms.html',
            'privacy_url': '/privacy.html',
            'cookies_url': '/cookies.html',
            'responsible_url': '/responsible.html',
            'footer': {
                'disclaimer': {
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return template.render(**template_data)
    
    def render_contact_page(self, content, design_system):
        """Render contact page"""
        template = self.env.get_template('contact_template.html')
        
        template_data = {
            'site_name': content['site_name'],
            'canonical_url': '/contact.html',
            'favicon_path': 'images/favicon.ico',
            'primary_font': design_system['typography']['heading_font'],
            'about_url': '/about.html',
            'contact_url': '/contact.html',
            'terms_url': '/terms.html',
            'privacy_url': '/privacy.html',
            'cookies_url': '/cookies.html',
            'responsible_url': '/responsible.html',
            'footer': {
                'disclaimer': {
                    'title': 'Disclaimer',
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return template.render(**template_data)
    
    def generate_main_css(self, design_system):
        """Generate main CSS file that matches the template structure"""
        return f"""/* Main CSS for Casino Website Template */
:root {{
    --primary-color: {design_system['colors']['primary']};
    --secondary-color: {design_system['colors']['secondary']};
    --accent-color: {design_system['colors']['accent']};
    --background-color: {design_system['colors']['background']};
    --surface-color: {design_system['colors']['surface']};
    --text-color: {design_system['colors']['text_primary']};
    --text-secondary: {design_system['colors']['text_secondary']};
    --success-color: {design_system['colors']['success']};
    --warning-color: {design_system['colors']['warning']};
    --error-color: {design_system['colors']['error']};
    
    --heading-font: '{design_system['typography']['heading_font']}', sans-serif;
    --body-font: '{design_system['typography']['body_font']}', sans-serif;
    
    --gradient-1: {design_system['gradients'][0]};
    --gradient-2: {design_system['gradients'][1] if len(design_system['gradients']) > 1 else design_system['gradients'][0]};
    
    --sidebar-width: 280px;
    --sidebar-collapsed-width: 60px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--body-font);
    background: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
    overflow-x: hidden;
}}

/* Sidebar Styles */
.sidebar {{
    position: fixed;
    top: 0;
    left: 0;
    width: var(--sidebar-width);
    height: 100vh;
    background: var(--primary-color);
    z-index: 1000;
    transition: transform 0.3s ease;
    overflow-y: auto;
}}

.sidebar-header {{
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}}

.logo {{
    font-family: var(--heading-font);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent-color);
}}

.sidebar-nav {{
    padding: 1rem 0;
}}

.nav-item {{
    display: flex;
    align-items: center;
    padding: 1rem 1.5rem;
    color: var(--text-color);
    text-decoration: none;
    transition: all 0.3s ease;
    border-left: 3px solid transparent;
}}

.nav-item:hover,
.nav-item.active {{
    background: rgba(255,255,255,0.1);
    border-left-color: var(--accent-color);
}}

.nav-item i {{
    margin-right: 0.75rem;
    width: 20px;
}}

.sidebar-toggle {{
    position: absolute;
    top: 50%;
    right: -15px;
    transform: translateY(-50%);
    background: var(--accent-color);
    color: var(--primary-color);
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
}}

/* Mobile Sidebar */
.mobile-sidebar-toggle {{
    display: none;
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 1001;
    background: var(--primary-color);
    color: var(--accent-color);
    border: none;
    width: 50px;
    height: 50px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1.2rem;
}}

.sidebar-overlay {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 999;
}}

/* Main Content */
.main-wrapper {{
    margin-left: var(--sidebar-width);
    min-height: 100vh;
    transition: margin-left 0.3s ease;
}}

/* Hero Section */
.hero {{
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    background-attachment: fixed;
}}

.hero-content {{
    max-width: 800px;
    padding: 2rem;
    z-index: 2;
}}

.hero h1 {{
    font-family: var(--heading-font);
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    margin-bottom: 1rem;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}}

.hero p {{
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: rgba(255,255,255,0.9);
}}

/* Buttons */
.btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    border: none;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
}}

.btn-primary {{
    background: var(--gradient-1);
    color: white;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}}

.btn-large {{
    padding: 1.2rem 2.5rem;
    font-size: 1.1rem;
}}

/* Content Sections */
.content-section {{
    padding: 4rem 2rem;
}}

.section-header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.section-title {{
    font-family: var(--heading-font);
    font-size: 2.5rem;
    color: var(--accent-color);
    margin-bottom: 1rem;
}}

.section-subtitle {{
    font-size: 1.1rem;
    color: var(--text-secondary);
}}

/* Cards and Sliders */
.cards-container {{
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
}}

.cards-slider {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    overflow: hidden;
}}

.card {{
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    background: var(--surface-color);
    transition: transform 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
}}

.card-thumbnail {{
    width: 100%;
    height: 200px;
    object-fit: cover;
}}

.card-overlay {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.8));
    padding: 2rem 1rem 1rem;
    transform: translateY(100%);
    transition: transform 0.3s ease;
}}

.card:hover .card-overlay {{
    transform: translateY(0);
}}

.card-title {{
    color: white;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.card-cta {{
    background: var(--accent-color);
    color: var(--primary-color);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    display: inline-block;
}}

/* Games Page Styles */
.games-header {{
    background: var(--gradient-1);
    padding: 4rem 2rem 2rem;
    text-align: center;
    color: white;
}}

.games-header h1 {{
    font-family: var(--heading-font);
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.games-count {{
    background: rgba(255,255,255,0.2);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    display: inline-block;
    margin-top: 1rem;
}}

.games-section {{
    padding: 4rem 2rem;
}}

.games-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}}

.game-card {{
    background: var(--surface-color);
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.3s ease;
    position: relative;
}}

.game-card:hover {{
    transform: scale(1.02);
}}

.game-thumbnail {{
    width: 100%;
    height: 200px;
    object-fit: cover;
}}

.game-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.9));
    display: flex;
    align-items: flex-end;
    padding: 1rem;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.game-card:hover .game-overlay {{
    opacity: 1;
}}

.game-info {{
    color: white;
}}

.game-title {{
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.game-cta {{
    background: var(--accent-color);
    color: var(--primary-color);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    display: inline-block;
}}

/* Game Page Styles */
.game-header {{
    background: var(--gradient-1);
    padding: 2rem;
    color: white;
}}

.breadcrumb {{
    margin-bottom: 1rem;
    font-size: 0.9rem;
}}

.breadcrumb a {{
    color: rgba(255,255,255,0.8);
    text-decoration: none;
}}

.breadcrumb-separator {{
    margin: 0 0.5rem;
}}

.game-title {{
    font-family: var(--heading-font);
    font-size: 2.5rem;
}}

.game-container {{
    padding: 2rem;
}}

.game-wrapper {{
    max-width: 1200px;
    margin: 0 auto;
}}

.game-iframe-container {{
    position: relative;
    width: 100%;
    height: 600px;
    background: var(--surface-color);
    border-radius: 12px;
    overflow: hidden;
}}

.game-iframe {{
    width: 100%;
    height: 100%;
    border: none;
}}

.game-loading {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--surface-color);
    z-index: 10;
}}

.game-loading-spinner {{
    width: 50px;
    height: 50px;
    border: 3px solid rgba(255,255,255,0.3);
    border-top: 3px solid var(--accent-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}}

@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

.fullscreen-btn {{
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: rgba(0,0,0,0.7);
    color: white;
    border: none;
    padding: 0.5rem;
    border-radius: 6px;
    cursor: pointer;
    z-index: 20;
}}

/* Page Header */
.page-header {{
    background: var(--gradient-1);
    padding: 4rem 2rem 2rem;
    text-align: center;
    color: white;
}}

.page-header h1 {{
    font-family: var(--heading-font);
    font-size: 3rem;
    margin-bottom: 1rem;
}}

/* About Section */
.about-section {{
    padding: 4rem 2rem;
    background: var(--surface-color);
}}

.about-content {{
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}}

.about-block {{
    margin-bottom: 3rem;
}}

.about-block h2 {{
    font-family: var(--heading-font);
    color: var(--accent-color);
    margin-bottom: 1rem;
}}

/* Content Wrapper */
.content-wrapper {{
    max-width: 800px;
    margin: 0 auto;
    padding: 0 2rem;
}}

/* Footer */
.footer {{
    background: var(--primary-color);
    color: var(--text-color);
    padding: 3rem 2rem 1rem;
    margin-top: auto;
}}

.footer-content {{
    max-width: 1200px;
    margin: 0 auto;
}}

.footer-links {{
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}}

.footer-link {{
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.3s ease;
}}

.footer-link:hover,
.footer-link.active {{
    color: var(--accent-color);
}}

.footer-bottom {{
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    color: var(--text-secondary);
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .sidebar {{
        transform: translateX(-100%);
    }}
    
    .sidebar.active {{
        transform: translateX(0);
    }}
    
    .sidebar-overlay.active {{
        display: block;
    }}
    
    .mobile-sidebar-toggle {{
        display: block;
    }}
    
    .main-wrapper {{
        margin-left: 0;
    }}
    
    .hero h1 {{
        font-size: 2rem;
    }}
    
    .section-title {{
        font-size: 2rem;
    }}
    
    .cards-slider {{
        grid-template-columns: 1fr;
    }}
    
    .footer-links {{
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }}
}}

/* Slider Navigation */
.slider-nav {{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0,0,0,0.7);
    color: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    z-index: 10;
    display: none;
}}

.slider-prev {{
    left: -20px;
}}

.slider-next {{
    right: -20px;
}}

.slider-dots {{
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 2rem;
}}

.dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255,255,255,0.3);
    cursor: pointer;
    transition: background 0.3s ease;
}}

.dot.active {{
    background: var(--accent-color);
}}"""
    
    def generate_template_javascript_files(self, output_dir):
        """Generate JavaScript files for the template functionality"""
        
        # Main JavaScript for sidebar and general functionality
        main_js = '''// Main JavaScript for Casino Website Template

// Sidebar functionality
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainWrapper = document.getElementById('mainWrapper');
    
    sidebar.classList.toggle('collapsed');
    if (sidebar.classList.contains('collapsed')) {
        mainWrapper.style.marginLeft = 'var(--sidebar-collapsed-width)';
    } else {
        mainWrapper.style.marginLeft = 'var(--sidebar-width)';
    }
}

function toggleMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    sidebar.classList.add('active');
    overlay.classList.add('active');
}

function closeMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
}

// Image error handling
function handleImageError(img) {
    img.style.display = 'none';
    const placeholder = document.createElement('div');
    placeholder.className = 'image-placeholder';
    placeholder.style.cssText = `
        width: 100%;
        height: 200px;
        background: linear-gradient(45deg, #333, #555);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.9rem;
    `;
    placeholder.textContent = 'Game Image';
    img.parentNode.insertBefore(placeholder, img);
}

function handleImageLoad(img) {
    img.style.opacity = '1';
}

// Game tracking
function trackGameClick(gameTitle, gameUrl, gameProvider) {
    console.log('Game clicked:', { gameTitle, gameUrl, gameProvider });
    // Add analytics tracking here if needed
}

// Game page functionality
function hideLoading() {
    const loading = document.getElementById('gameLoading');
    if (loading) {
        loading.style.display = 'none';
    }
}

function showError() {
    const loading = document.getElementById('gameLoading');
    if (loading) {
        loading.innerHTML = '<p>Error loading game. Please try again later.</p>';
    }
}

function toggleFullscreen() {
    const container = document.querySelector('.game-iframe-container');
    const btn = document.querySelector('.fullscreen-btn i');
    
    if (!document.fullscreenElement) {
        container.requestFullscreen().then(() => {
            btn.className = 'fas fa-compress';
        });
    } else {
        document.exitFullscreen().then(() => {
            btn.className = 'fas fa-expand';
        });
    }
}

// Slider functionality
function slideCards(sectionId, direction) {
    const slider = document.getElementById(sectionId + 'Slider');
    const cards = slider.children;
    const cardWidth = cards[0].offsetWidth + 32; // 32px for gap
    const currentScroll = slider.scrollLeft;
    const newScroll = currentScroll + (direction * cardWidth * 2);
    
    slider.scrollTo({
        left: newScroll,
        behavior: 'smooth'
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set active navigation item
    const currentPage = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href === currentPage || (currentPage === '/' && href === '/')) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Close mobile sidebar when clicking on nav items
    navItems.forEach(item => {
        item.addEventListener('click', closeMobileSidebar);
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeMobileSidebar();
        }
    });
    
    // Initialize slider dots if present
    initializeSliderDots();
});

function initializeSliderDots() {
    const sliders = document.querySelectorAll('.cards-slider');
    
    sliders.forEach((slider, index) => {
        const dotsContainer = document.getElementById(`section${index}Dots`);
        if (!dotsContainer) return;
        
        const cardCount = slider.children.length;
        const dotsCount = Math.ceil(cardCount / 2); // 2 cards per view
        
        for (let i = 0; i < dotsCount; i++) {
            const dot = document.createElement('div');
            dot.className = 'dot';
            if (i === 0) dot.classList.add('active');
            
            dot.addEventListener('click', () => {
                const cardWidth = slider.children[0].offsetWidth + 32;
                slider.scrollTo({
                    left: i * cardWidth * 2,
                    behavior: 'smooth'
                });
                
                dotsContainer.querySelectorAll('.dot').forEach(d => d.classList.remove('active'));
                dot.classList.add('active');
            });
            
            dotsContainer.appendChild(dot);
        }
    });
}'''
        
        with open(f"{output_dir}/js/main.js", 'w', encoding='utf-8') as f:
            f.write(main_js)
    
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
