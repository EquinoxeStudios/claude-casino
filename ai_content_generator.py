import asyncio
import random
from openai import OpenAI
from config import OPENAI_API_KEY, GOOGLE_FONTS
from utils import print_colored, generate_random_string
from colorama import Fore

class AIContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    async def generate_theme_concepts(self, domain_name):
        """Generate 3 unique theme concepts based on domain name"""
        prompt = f"""
        Based on the domain name "{domain_name}", generate 3 unique casino theme concepts.
        Each theme should be creative, engaging, and suitable for a social casino website.
        
        Return a JSON array with this exact structure:
        [
            {{
                "name": "Theme Name",
                "description": "Brief description of the theme and its visual style",
                "keywords": ["keyword1", "keyword2", "keyword3"],
                "mood": "exciting/mysterious/luxurious/etc",
                "color_inspiration": "primary color concept"
            }}
        ]
        
        Make each theme distinctly different from the others.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.8
            )
            
            import json
            themes = json.loads(response.choices[0].message.content)
            return themes
            
        except Exception as e:
            print_colored(f"Error generating themes: {e}", Fore.RED)
            # Fallback themes
            return [
                {
                    "name": "Neon Vegas",
                    "description": "Electric neon lights and modern casino vibes",
                    "keywords": ["neon", "electric", "modern"],
                    "mood": "exciting",
                    "color_inspiration": "electric blue and purple"
                },
                {
                    "name": "Golden Palace",
                    "description": "Luxurious golden theme with royal elegance",
                    "keywords": ["gold", "luxury", "royal"],
                    "mood": "luxurious",
                    "color_inspiration": "gold and deep red"
                },
                {
                    "name": "Mystic Forest",
                    "description": "Enchanted forest with magical casino elements",
                    "keywords": ["forest", "magic", "nature"],
                    "mood": "mysterious",
                    "color_inspiration": "emerald green and earth tones"
                }
            ]
    
    async def generate_design_system(self, theme):
        """Generate complete design system based on chosen theme"""
        prompt = f"""
        Create a complete design system for a casino website with the theme "{theme['name']}".
        Theme description: {theme['description']}
        Color inspiration: {theme['color_inspiration']}
        
        Return a JSON object with this exact structure:
        {{
            "colors": {{
                "primary": "#hexcolor",
                "secondary": "#hexcolor",
                "accent": "#hexcolor",
                "background": "#hexcolor",
                "surface": "#hexcolor",
                "text_primary": "#hexcolor",
                "text_secondary": "#hexcolor",
                "success": "#hexcolor",
                "warning": "#hexcolor",
                "error": "#hexcolor"
            }},
            "typography": {{
                "heading_font": "Google Font Name",
                "body_font": "Google Font Name",
                "heading_weight": "400/500/600/700",
                "body_weight": "300/400/500"
            }},
            "gradients": [
                "linear-gradient(direction, color1, color2)",
                "linear-gradient(direction, color1, color2)"
            ]
        }}
        
        Use only Google Fonts from this list: {', '.join(GOOGLE_FONTS)}
        Make sure all colors work well together and fit the theme.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            import json
            design_system = json.loads(response.choices[0].message.content)
            return design_system
            
        except Exception as e:
            print_colored(f"Error generating design system: {e}", Fore.RED)
            # Fallback design system
            return {
                "colors": {
                    "primary": "#1a1a2e",
                    "secondary": "#16213e",
                    "accent": "#ffd700",
                    "background": "#0f0f23",
                    "surface": "#1e1e3f",
                    "text_primary": "#ffffff",
                    "text_secondary": "#b0b0b0",
                    "success": "#2ed573",
                    "warning": "#ffa726",
                    "error": "#e94560"
                },
                "typography": {
                    "heading_font": "Montserrat",
                    "body_font": "Open Sans",
                    "heading_weight": "600",
                    "body_weight": "400"
                },
                "gradients": [
                    "linear-gradient(135deg, #1a1a2e, #16213e)",
                    "linear-gradient(45deg, #ffd700, #ffed4a)"
                ]
            }
    
    async def generate_images(self, theme):
        """Generate hero image and favicon using DALL-E"""
        hero_prompt = f"""
        Create a stunning casino hero image for the theme "{theme['name']}".
        Description: {theme['description']}
        Style: High-quality, professional, casino-themed, {theme['mood']}, suitable for website header.
        Resolution should be wide format (1920x800 aspect ratio).
        No text or logos in the image.
        """
        
        favicon_prompt = f"""
        Create a simple, iconic favicon design for a casino website with the theme "{theme['name']}".
        Style: Minimalist, recognizable at small sizes, {theme['mood']}, casino-themed.
        Should work well as a 32x32 pixel icon.
        No text, just symbols or shapes.
        """
        
        try:
            # Generate hero image
            hero_response = self.client.images.generate(
                model="dall-e-3",
                prompt=hero_prompt,
                size="1792x1024",
                quality="standard",
                n=1
            )
            
            # Generate favicon
            favicon_response = self.client.images.generate(
                model="dall-e-3",
                prompt=favicon_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            return {
                "hero_url": hero_response.data[0].url,
                "favicon_url": favicon_response.data[0].url
            }
            
        except Exception as e:
            print_colored(f"Error generating images: {e}", Fore.RED)
            return {
                "hero_url": "https://via.placeholder.com/1792x1024/1a1a2e/ffd700?text=Casino+Hero",
                "favicon_url": "https://via.placeholder.com/32x32/1a1a2e/ffd700?text=🎰"
            }
    
    async def generate_all_content(self, domain_name, theme, games):
        """Generate all website content"""
        site_name = domain_name.replace('.com', '').replace('.', ' ').title()
        
        content = {
            "site_name": site_name,
            "theme": theme,
            "pages": {}
        }
        
        # Generate homepage content
        content["pages"]["homepage"] = await self.generate_homepage_content(site_name, theme, games[:6])
        
        # Generate about page content
        content["pages"]["about"] = await self.generate_about_content(site_name, theme)
        
        # Generate legal pages content
        content["pages"]["legal"] = await self.generate_legal_content(site_name)
        
        return content
    
    async def generate_homepage_content(self, site_name, theme, featured_games):
        """Generate homepage content"""
        prompt = f"""
        Create homepage content for a social casino website called "{site_name}".
        Theme: {theme['name']} - {theme['description']}
        
        Generate engaging, professional content that includes:
        1. Hero headline and subheadline
        2. About section text (2-3 paragraphs)
        3. Features list (4-5 key features)
        4. Call-to-action text
        
        Return as JSON with this structure:
        {{
            "hero": {{
                "headline": "Main catchy headline",
                "subheadline": "Supporting text"
            }},
            "about": {{
                "title": "About section title",
                "content": "About text paragraphs"
            }},
            "features": [
                {{
                    "title": "Feature name",
                    "description": "Feature description"
                }}
            ],
            "cta": {{
                "text": "Call to action text",
                "button": "Button text"
            }}
        }}
        
        Make it exciting but responsible (social casino, no real money).
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.7
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print_colored(f"Error generating homepage content: {e}", Fore.RED)
            return {
                "hero": {
                    "headline": f"Welcome to {site_name}",
                    "subheadline": "Experience the thrill of casino games in a fun, social environment"
                },
                "about": {
                    "title": "About Our Casino",
                    "content": "Discover an amazing collection of casino games designed for entertainment. Play your favorite slots, table games, and more in a safe, social environment."
                },
                "features": [
                    {"title": "100+ Games", "description": "Huge selection of slots and casino games"},
                    {"title": "Daily Bonuses", "description": "Free credits every day to keep playing"},
                    {"title": "Social Features", "description": "Connect with friends and compete"},
                    {"title": "Mobile Friendly", "description": "Play anywhere on any device"}
                ],
                "cta": {
                    "text": "Ready to start playing?",
                    "button": "Play Now"
                }
            }
    
    async def generate_about_content(self, site_name, theme):
        """Generate about page content"""
        prompt = f"""
        Create an about page for the social casino website "{site_name}" with theme "{theme['name']}".
        
        Include:
        1. Company story/mission
        2. What makes us special
        3. Our commitment to responsible gaming
        4. Contact information section
        
        Return as JSON:
        {{
            "title": "About Us",
            "sections": [
                {{
                    "title": "Section title",
                    "content": "Section content"
                }}
            ]
        }}
        
        Keep it professional but engaging. Emphasize entertainment value.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print_colored(f"Error generating about content: {e}", Fore.RED)
            return {
                "title": "About Us",
                "sections": [
                    {
                        "title": "Our Story",
                        "content": f"{site_name} was created to bring the excitement of casino gaming to everyone in a fun, safe environment. We believe in providing entertainment that brings people together."
                    },
                    {
                        "title": "Our Mission",
                        "content": "We're committed to providing the best social casino experience with high-quality games, fair play, and responsible gaming practices."
                    },
                    {
                        "title": "Contact Us",
                        "content": f"Questions? Reach out to us at support@{site_name.lower().replace(' ', '')}.com"
                    }
                ]
            }
    
    async def generate_legal_content(self, site_name):
        """Generate legal pages content"""
        return {
            "terms": {
                "title": "Terms & Conditions",
                "content": f"These terms govern your use of {site_name}. By using our services, you agree to these terms..."
            },
            "privacy": {
                "title": "Privacy Policy", 
                "content": f"{site_name} is committed to protecting your privacy. This policy explains how we collect and use your information..."
            },
            "responsible": {
                "title": "Responsible Gaming",
                "content": "We promote responsible gaming practices. Our games are for entertainment only and do not offer real money gambling..."
            }
        }