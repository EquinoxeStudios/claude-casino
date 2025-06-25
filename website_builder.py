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
    
    def _build_iframe_url(self, base_url):
        """Build iframe URL with API token if it's a SlotsLaunch URL"""
        if not base_url or base_url == 'about:blank':
            return base_url
            
        # Check if it's a SlotsLaunch iframe URL
        if 'slotslaunch.com/iframe/' in base_url:
            from config import SLOTSLAUNCH_API_TOKEN
            
            # Only add token if it's configured and not a placeholder
            if SLOTSLAUNCH_API_TOKEN and SLOTSLAUNCH_API_TOKEN != 'your_slotslaunch_token_here':
                # Add token parameter
                separator = '&' if '?' in base_url else '?'
                return f"{base_url}{separator}token={SLOTSLAUNCH_API_TOKEN}"
        
        return base_url
    
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
                'iframe_url': self._build_iframe_url(game.get('demo_url', 'about:blank'))
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
        """Generate enhanced CSS with modern visual effects while preserving all functionality"""
        return f"""/* Enhanced Premium Casino Website CSS */
:root {{
    /* Core Colors */
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
    
    /* Typography */
    --heading-font: '{design_system['typography']['heading_font']}', sans-serif;
    --body-font: '{design_system['typography']['body_font']}', sans-serif;
    
    /* Enhanced Gradients */
    --gradient-1: {design_system['gradients'][0]};
    --gradient-2: {design_system['gradients'][1] if len(design_system['gradients']) > 1 else design_system['gradients'][0]};
    --gradient-premium: linear-gradient(135deg, var(--primary-color) 0%, var(--accent-color) 50%, var(--secondary-color) 100%);
    --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    --gradient-shadow: linear-gradient(135deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.1) 100%);
    
    /* Layout */
    --sidebar-width: 280px;
    --sidebar-collapsed-width: 60px;
    
    /* Enhanced Design System */
    --blur-intensity: 20px;
    --border-radius-sm: 8px;
    --border-radius-md: 12px;
    --border-radius-lg: 20px;
    --border-radius-xl: 24px;
    
    /* Shadows */
    --shadow-sm: 0 2px 8px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.15);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.2);
    --shadow-xl: 0 16px 64px rgba(0,0,0,0.25);
    --shadow-glow: 0 0 20px rgba(var(--accent-color-rgb), 0.3);
    
    /* Transitions */
    --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Z-indices */
    --z-dropdown: 1000;
    --z-sticky: 1020;
    --z-fixed: 1030;
    --z-modal-backdrop: 1040;
    --z-modal: 1050;
    --z-popover: 1060;
    --z-tooltip: 1070;
}}

/* Reset & Base Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

*::before,
*::after {{
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
    scroll-padding-top: 2rem;
}}

body {{
    font-family: var(--body-font);
    background: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
    overflow-x: hidden;
    min-height: 100vh;
    position: relative;
}}

/* Enhanced Background with animated particles */
body::before {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.05) 0%, transparent 50%);
    z-index: -1;
    animation: backgroundShift 20s ease-in-out infinite;
}}

@keyframes backgroundShift {{
    0%, 100% {{ 
        transform: translateY(0) rotate(0deg);
        opacity: 0.3;
    }}
    50% {{ 
        transform: translateY(-10px) rotate(2deg);
        opacity: 0.5;
    }}
}}

/* Enhanced Typography */
h1, h2, h3, h4, h5, h6 {{
    font-family: var(--heading-font);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
    background: var(--gradient-premium);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: textShine 3s ease-in-out infinite;
}}

@keyframes textShine {{
    0%, 100% {{ filter: brightness(1); }}
    50% {{ filter: brightness(1.2); }}
}}

/* Smooth scrollbar styling */
::-webkit-scrollbar {{
    width: 8px;
}}

::-webkit-scrollbar-track {{
    background: var(--surface-color);
}}

::-webkit-scrollbar-thumb {{
    background: var(--gradient-1);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--accent-color);
}}

/* Enhanced Sidebar with Glassmorphism */
.sidebar {{
    position: fixed;
    top: 0;
    left: 0;
    width: var(--sidebar-width);
    height: 100vh;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(var(--blur-intensity));
    -webkit-backdrop-filter: blur(var(--blur-intensity));
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    z-index: var(--z-fixed);
    transition: transform var(--transition-normal);
    overflow-y: auto;
    box-shadow: var(--shadow-xl);
}}

.sidebar::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--gradient-glass);
    z-index: -1;
}}

.sidebar-header {{
    padding: 2rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    position: relative;
}}

.logo {{
    font-family: var(--heading-font);
    font-size: 1.8rem;
    font-weight: 900;
    background: var(--gradient-premium);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    position: relative;
}}

.logo::after {{
    content: '';
    position: absolute;
    bottom: -0.5rem;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 2px;
    background: var(--gradient-1);
    border-radius: 2px;
}}

.sidebar-nav {{
    padding: 1rem 0;
}}

.nav-item {{
    display: flex;
    align-items: center;
    padding: 1.25rem 1.5rem;
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: all var(--transition-normal);
    border-left: 3px solid transparent;
    margin: 0.25rem 0.75rem;
    border-radius: var(--border-radius-md);
    position: relative;
    overflow: hidden;
}}

.nav-item::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: var(--gradient-1);
    transition: left var(--transition-normal);
    z-index: -1;
}}

.nav-item:hover::before,
.nav-item.active::before {{
    left: 0;
}}

.nav-item:hover,
.nav-item.active {{
    color: white;
    transform: translateX(8px);
    box-shadow: var(--shadow-md);
    border-left-color: var(--accent-color);
}}

.nav-item i {{
    margin-right: 0.75rem;
    width: 20px;
    font-size: 1.1rem;
    transition: transform var(--transition-fast);
}}

.nav-item:hover i {{
    transform: scale(1.1);
}}

.sidebar-toggle {{
    position: absolute;
    top: 50%;
    right: -18px;
    transform: translateY(-50%);
    background: var(--gradient-1);
    color: white;
    border: none;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    cursor: pointer;
    transition: all var(--transition-normal);
    box-shadow: var(--shadow-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}}

.sidebar-toggle:hover {{
    transform: translateY(-50%) scale(1.1);
    box-shadow: var(--shadow-xl);
}}

/* Enhanced Mobile Sidebar */
.mobile-sidebar-toggle {{
    display: none;
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: calc(var(--z-fixed) + 1);
    background: var(--gradient-1);
    color: white;
    border: none;
    width: 56px;
    height: 56px;
    border-radius: var(--border-radius-md);
    cursor: pointer;
    font-size: 1.3rem;
    box-shadow: var(--shadow-lg);
    transition: all var(--transition-normal);
    backdrop-filter: blur(var(--blur-intensity));
}}

.mobile-sidebar-toggle:hover {{
    transform: scale(1.05);
    box-shadow: var(--shadow-xl);
}}

.sidebar-overlay {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(4px);
    z-index: calc(var(--z-fixed) - 1);
    transition: all var(--transition-normal);
}}

/* Enhanced Main Content */
.main-wrapper {{
    margin-left: var(--sidebar-width);
    min-height: 100vh;
    transition: margin-left var(--transition-normal);
    position: relative;
    background: transparent;
}}

/* Enhanced Hero Section */
.hero {{
    min-height: 70vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    background-attachment: fixed;
    overflow: hidden;
}}

.hero::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 2px,
        rgba(255,255,255,0.03) 2px,
        rgba(255,255,255,0.03) 4px
    );
    animation: heroPattern 20s linear infinite;
    z-index: 1;
}}

@keyframes heroPattern {{
    0% {{ transform: translateX(0) translateY(0); }}
    100% {{ transform: translateX(50px) translateY(50px); }}
}}

.hero-content {{
    max-width: 900px;
    padding: 3rem 2rem;
    z-index: 3;
    position: relative;
}}

.hero-content::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 120%;
    height: 120%;
    background: var(--gradient-glass);
    border-radius: var(--border-radius-xl);
    backdrop-filter: blur(10px);
    z-index: -1;
    border: 1px solid rgba(255,255,255,0.1);
}}

.hero h1 {{
    font-family: var(--heading-font);
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 900;
    margin-bottom: 1.5rem;
    color: white;
    text-shadow: 
        0 0 20px rgba(255,255,255,0.5),
        0 0 40px rgba(255,255,255,0.3),
        2px 2px 8px rgba(0,0,0,0.8);
    animation: heroTitleGlow 3s ease-in-out infinite;
    line-height: 1.1;
}}

@keyframes heroTitleGlow {{
    0%, 100% {{ 
        text-shadow: 
            0 0 20px rgba(255,255,255,0.5),
            0 0 40px rgba(255,255,255,0.3),
            2px 2px 8px rgba(0,0,0,0.8);
    }}
    50% {{ 
        text-shadow: 
            0 0 30px rgba(255,255,255,0.8),
            0 0 60px rgba(255,255,255,0.5),
            2px 2px 8px rgba(0,0,0,0.8);
    }}
}}

.hero p {{
    font-size: 1.3rem;
    margin-bottom: 2.5rem;
    color: rgba(255,255,255,0.95);
    text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
    line-height: 1.6;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}}

/* Enhanced Buttons with Modern Effects */
.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    border: none;
    border-radius: var(--border-radius-md);
    text-decoration: none;
    font-weight: 600;
    font-family: var(--heading-font);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
    transition: all var(--transition-normal);
    cursor: pointer;
    box-shadow: var(--shadow-md);
    z-index: 1;
}}

.btn::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left var(--transition-slow);
    z-index: -1;
}}

.btn:hover::before {{
    left: 100%;
}}

.btn-primary {{
    background: var(--gradient-1);
    color: white;
    border: 2px solid transparent;
    box-shadow: var(--shadow-lg), var(--shadow-glow);
}}

.btn-primary:hover {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: var(--shadow-xl), 0 0 30px rgba(120, 119, 198, 0.5);
    filter: brightness(110%);
}}

.btn-primary:active {{
    transform: translateY(-1px) scale(0.98);
    transition: all var(--transition-fast);
}}

.btn-secondary {{
    background: transparent;
    color: var(--accent-color);
    border: 2px solid var(--accent-color);
    backdrop-filter: blur(10px);
}}

.btn-secondary:hover {{
    background: var(--accent-color);
    color: var(--primary-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}}

.btn-large {{
    padding: 1.5rem 3rem;
    font-size: 1.2rem;
    border-radius: var(--border-radius-lg);
    font-weight: 800;
}}

.btn-icon {{
    transition: transform var(--transition-fast);
}}

.btn:hover .btn-icon {{
    transform: scale(1.2) rotate(5deg);
}}

/* Pulse animation for CTAs */
.btn-pulse {{
    animation: btnPulse 2s infinite;
}}

@keyframes btnPulse {{
    0% {{ box-shadow: var(--shadow-lg), 0 0 0 0 rgba(120, 119, 198, 0.7); }}
    70% {{ box-shadow: var(--shadow-lg), 0 0 0 10px rgba(120, 119, 198, 0); }}
    100% {{ box-shadow: var(--shadow-lg), 0 0 0 0 rgba(120, 119, 198, 0); }}
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

/* Enhanced Cards with Glassmorphism */
.cards-container {{
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
}}

.cards-slider {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    overflow: hidden;
    padding: 1rem 0;
}}

.card {{
    position: relative;
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(var(--blur-intensity));
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all var(--transition-normal);
    cursor: pointer;
    transform-style: preserve-3d;
}}

.card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--gradient-glass);
    opacity: 0;
    transition: opacity var(--transition-normal);
    z-index: 1;
    border-radius: var(--border-radius-lg);
}}

.card:hover {{
    transform: translateY(-10px) rotateX(5deg);
    box-shadow: var(--shadow-xl), 0 20px 40px rgba(0,0,0,0.3);
    border-color: rgba(255, 255, 255, 0.2);
}}

.card:hover::before {{
    opacity: 1;
}}

.card-thumbnail {{
    width: 100%;
    height: 220px;
    object-fit: cover;
    transition: transform var(--transition-normal);
    position: relative;
    z-index: 2;
}}

.card:hover .card-thumbnail {{
    transform: scale(1.05);
}}

.card-overlay {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.9));
    backdrop-filter: blur(10px);
    padding: 2rem 1.5rem 1.5rem;
    transform: translateY(100%);
    transition: all var(--transition-normal);
    z-index: 3;
    border-radius: 0 0 var(--border-radius-lg) var(--border-radius-lg);
}}

.card:hover .card-overlay {{
    transform: translateY(0);
}}

.card-info {{
    position: relative;
    z-index: 4;
}}

.card-title {{
    color: white;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    font-family: var(--heading-font);
}}

.card-cta {{
    background: var(--gradient-1);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: var(--border-radius-md);
    text-decoration: none;
    font-weight: 600;
    font-family: var(--heading-font);
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all var(--transition-normal);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.9rem;
    position: relative;
    overflow: hidden;
}}

.card-cta::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left var(--transition-normal);
}}

.card-cta:hover::before {{
    left: 100%;
}}

.card-cta:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    filter: brightness(110%);
}}

/* Card loading animation */
.card-loading {{
    position: relative;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    background-size: 200% 100%;
    animation: cardShimmer 2s infinite;
}}

@keyframes cardShimmer {{
    0% {{ background-position: -200% 0; }}
    100% {{ background-position: 200% 0; }}
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

/* Enhanced Loading Animations */
.game-loading-spinner {{
    width: 60px;
    height: 60px;
    position: relative;
    margin-bottom: 1.5rem;
}}

.game-loading-spinner::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: 4px solid rgba(255,255,255,0.2);
    border-top: 4px solid var(--accent-color);
    border-radius: 50%;
    animation: spinPrimary 1.2s linear infinite;
}}

.game-loading-spinner::after {{
    content: '';
    position: absolute;
    top: 8px;
    left: 8px;
    width: 44px;
    height: 44px;
    border: 3px solid rgba(255,255,255,0.1);
    border-bottom: 3px solid var(--secondary-color);
    border-radius: 50%;
    animation: spinSecondary 1s linear infinite reverse;
}}

@keyframes spinPrimary {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

@keyframes spinSecondary {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

/* Pulse loading for content */
.loading-pulse {{
    animation: contentPulse 1.5s ease-in-out infinite;
}}

@keyframes contentPulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.6; }}
}}

/* Skeleton loading for cards */
.skeleton-card {{
    background: var(--surface-color);
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    position: relative;
}}

.skeleton-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,0.1),
        transparent
    );
    animation: skeletonWave 2s infinite;
}}

@keyframes skeletonWave {{
    0% {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}

/* Floating elements animation */
.floating-element {{
    animation: floating 3s ease-in-out infinite;
}}

@keyframes floating {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
}}

/* Fade in animation for page load */
.fade-in {{
    animation: fadeIn 0.6s ease-out;
}}

@keyframes fadeIn {{
    from {{ 
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{ 
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Scale in animation for cards */
.scale-in {{
    animation: scaleIn 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

@keyframes scaleIn {{
    from {{ 
        opacity: 0;
        transform: scale(0.8);
    }}
    to {{ 
        opacity: 1;
        transform: scale(1);
    }}
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
