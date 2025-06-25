import asyncio
import requests
from utils import create_directory, save_json, get_file_extension, print_colored
from colorama import Fore
from template_generator import DynamicTemplateGenerator

class WebsiteBuilder:
    def __init__(self):
        # Initialize dynamic template generator for unique templates
        self.template_generator = DynamicTemplateGenerator()
    
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
        """Generate CSS and JavaScript files - now handled by dynamic templates"""
        # Note: CSS and JS are now embedded in dynamically generated templates
        # This method remains for compatibility but may create additional assets if needed
        
        # Generate any additional JavaScript files if needed
        self.generate_additional_js_files(output_dir)
        
        print_colored("✅ Dynamic template assets generated", Fore.GREEN)
    
    def generate_additional_js_files(self, output_dir):
        """Generate any additional JavaScript files if needed"""
        # For now, all JS is embedded in templates
        # This method can be used for external JS libraries or additional functionality
        pass
    
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
        """Render homepage HTML using dynamic template generator"""
        # Prepare data structure for the dynamic template
        template_data = {
            'site_name': content['site_name'],
            'site_tagline': 'Social Casino Games',
            'canonical_url': '/',
            'favicon_path': 'images/favicon.ico',
            'meta_description': f"Play exciting casino games at {content['site_name']}. Enjoy slots, table games and more!",
            'design_system': design_system,
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
                    'title': 'Featured Games',
                    'subtitle': 'Most popular games on our platform',
                    'items': [self.format_game_for_template(game) for game in games[:6]]
                },
                {
                    'title': 'New Arrivals',
                    'subtitle': 'Latest additions to our game collection', 
                    'items': [self.format_game_for_template(game) for game in games[6:12] if len(games) > 6]
                }
            ],
            'about': {
                'content': content['pages']['homepage']['about']['content'].split('\n')
            },
            'footer': {
                'disclaimer': {
                    'title': 'Disclaimer',
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return self.template_generator.generate_homepage_template(template_data)
    
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
        """Render games listing page using dynamic template generator"""
        template_data = {
            'site_name': content['site_name'],
            'canonical_url': '/games.html',
            'favicon_path': 'images/favicon.ico',
            'meta_description': f"Browse all casino games at {content['site_name']}. Find your favorite slots and table games.",
            'design_system': design_system,
            'total_games': len(games),
            'all_games': [self.format_game_for_template(game) for game in games],
            'path_prefix': '',
            'footer': {
                'disclaimer': {
                    'title': 'Disclaimer',
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return self.template_generator.generate_games_template(template_data)
    
    def render_game_detail_page(self, content, design_system, game, all_games):
        """Render individual game detail page using dynamic template generator"""
        # Get similar games (same category, exclude current)
        similar_games = [g for g in all_games if g['category'] == game['category'] and g['id'] != game['id']][:4]
        
        template_data = {
            'site_name': content['site_name'],
            'canonical_url': f'/games/{game.get("slug", "unknown")}.html',
            'favicon_path': '../images/favicon.ico',
            'meta_description': f"Play {game.get('name', 'this game')} at {content['site_name']}. {game.get('description', 'Exciting casino game experience!')}",
            'design_system': design_system,
            'game': {
                'title': game.get('name', 'Unknown Game'),
                'iframe_url': self._build_iframe_url(game.get('demo_url', 'about:blank')),
                'description': game.get('description', ''),
                'provider': game.get('provider', 'Unknown'),
                'category': game.get('category', 'slots')
            },
            'similar_games': [self.format_game_for_template(g) for g in similar_games],
            'footer': {
                'disclaimer': {
                    'title': 'Disclaimer',
                    'text': 'This is a social casino for entertainment purposes only. No real money gambling.'
                },
                'copyright_year': '2024',
                'domain_name': content['site_name'].lower().replace(' ', '')
            }
        }
        
        return self.template_generator.generate_game_detail_template(template_data)
    
    def render_about_page(self, content, design_system):
        """Render about page using simple dynamic generation"""
        site_name = content['site_name']
        about_content = content['pages']['about']['content']
        
        # Simple dynamic about page template
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - {site_name}</title>
    <link rel="icon" type="image/png" href="images/favicon.ico">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #0f0f1e; color: #ffffff; margin: 0; padding: 2rem; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 3rem; }}
        .content {{ line-height: 1.6; }}
        .back-link {{ color: #7c77c6; text-decoration: none; margin-bottom: 2rem; display: inline-block; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> Back to Home</a>
        <div class="header">
            <h1>About {site_name}</h1>
        </div>
        <div class="content">
            <p>{about_content}</p>
        </div>
    </div>
</body>
</html>"""
    
    def render_legal_page(self, content, design_system, page_type):
        """Render legal pages using simple dynamic generation"""
        legal_titles = {
            'terms': 'Terms & Conditions',
            'privacy': 'Privacy Policy',
            'responsible': 'Responsible Gaming'
        }
        
        page_title = legal_titles.get(page_type, 'Legal Information')
        legal_content = content['pages']['legal'][page_type]['content']
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} - {content['site_name']}</title>
    <link rel="icon" type="image/png" href="images/favicon.ico">
    <style>
        body {{ font-family: Arial, sans-serif; background: #0f0f1e; color: #ffffff; margin: 0; padding: 2rem; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .back-link {{ color: #7c77c6; text-decoration: none; margin-bottom: 2rem; display: inline-block; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">← Back to Home</a>
        <h1>{page_title}</h1>
        <div>{legal_content}</div>
        <p><small>Last updated: January 1, 2024</small></p>
    </div>
</body>
</html>"""
    
    def render_contact_page(self, content, design_system):
        """Render contact page using simple dynamic generation"""
        site_name = content['site_name']
        contact_info = content['pages']['contact']
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us - {site_name}</title>
    <link rel="icon" type="image/png" href="images/favicon.ico">
    <style>
        body {{ font-family: Arial, sans-serif; background: #0f0f1e; color: #ffffff; margin: 0; padding: 2rem; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .back-link {{ color: #7c77c6; text-decoration: none; margin-bottom: 2rem; display: inline-block; }}
        .contact-info {{ margin: 2rem 0; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">← Back to Home</a>
        <h1>Contact Us</h1>
        <div class="contact-info">
            <p>{contact_info.get('content', 'Get in touch with us for any questions or support.')}</p>
            <p><strong>Email:</strong> {contact_info.get('email', 'support@casino.com')}</p>
        </div>
    </div>
</body>
</html>"""
    
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