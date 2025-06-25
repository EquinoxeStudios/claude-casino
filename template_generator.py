#!/usr/bin/env python3
"""
Dynamic HTML Template Generator for Casino Websites
Generates unique HTML templates on each run for anti-fingerprinting
"""

import random
import string
from enum import Enum
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

class Framework(Enum):
    VANILLA_CSS = ("vanilla", 0.30)
    TAILWIND = ("tailwind", 0.25)
    BOOTSTRAP = ("bootstrap", 0.20)
    BULMA = ("bulma", 0.15)
    MODERN_CSS = ("modern", 0.10)

class NavigationPattern(Enum):
    SIDEBAR = "sidebar"
    TOP_NAV = "top_nav"
    HAMBURGER = "hamburger"
    BOTTOM_NAV = "bottom_nav"
    FLOATING_ACTION = "floating_action"
    TAB_BAR = "tab_bar"

class LayoutStructure(Enum):
    GRID_12 = "grid-12"
    GRID_16 = "grid-16"
    CSS_GRID = "css-grid"
    FLEXBOX = "flexbox"

@dataclass
class TemplateConfig:
    framework: Framework
    navigation: NavigationPattern
    layout: LayoutStructure
    hero_style: str
    card_style: str
    color_scheme: str
    animation_type: str
    responsive_approach: str

class DynamicTemplateGenerator:
    def __init__(self):
        self.config = self._generate_random_config()
        self.class_prefix = self._generate_class_prefix()
        self.id_prefix = self._generate_id_prefix()
        
    def _generate_random_config(self) -> TemplateConfig:
        """Generate random configuration for template structure"""
        # Weighted random framework selection
        frameworks = list(Framework)
        weights = [f.value[1] for f in frameworks]
        framework = random.choices(frameworks, weights=weights)[0]
        
        return TemplateConfig(
            framework=framework,
            navigation=random.choice(list(NavigationPattern)),
            layout=random.choice(list(LayoutStructure)),
            hero_style=random.choice([
                "fullscreen_overlay", "split_hero", "video_background", 
                "gradient_animated", "particles", "carousel", "minimalist"
            ]),
            card_style=random.choice([
                "hover_overlay", "flip_card", "slide_up", "glassmorphism",
                "neumorphism", "gradient_border", "zoom_hover"
            ]),
            color_scheme=random.choice([
                "dark_gradient", "neon_cyber", "warm_casino", "cool_blue",
                "purple_gold", "red_black", "green_emerald"
            ]),
            animation_type=random.choice([
                "css_animations", "intersection_observer", "micro_interactions",
                "page_transitions", "loading_states"
            ]),
            responsive_approach=random.choice(["mobile_first", "desktop_first", "container_queries"])
        )
    
    def _generate_class_prefix(self) -> str:
        """Generate random class prefix for uniqueness"""
        return ''.join(random.choices(string.ascii_lowercase, k=3))
    
    def _generate_id_prefix(self) -> str:
        """Generate random ID prefix for uniqueness"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    
    def generate_homepage_template(self, content_data: Dict[str, Any]) -> str:
        """Generate unique homepage template"""
        meta_tags = self._generate_meta_tags(content_data)
        head_section = self._generate_head_section(content_data)
        navigation = self._generate_navigation(content_data)
        hero_section = self._generate_hero_section(content_data)
        content_sections = self._generate_content_sections(content_data)
        footer = self._generate_footer(content_data)
        scripts = self._generate_scripts()
        
        # Standard DOCTYPE for compatibility
        doctype = "<!DOCTYPE html>"
        
        # Random html attributes
        html_attrs = self._generate_html_attributes()
        
        template = f"""{doctype}
<html{html_attrs} lang="en">
<head>
{meta_tags}
{head_section}
</head>
<body{self._generate_body_attributes()}>
    <!-- Randomized comment: {self._generate_random_comment()} -->
    {navigation}
    
    <main class="main-wrapper" id="main-content" role="main" aria-label="Main content">
        <div class="accessibility-info sr-only">
            <h1>Casino Website Content</h1>
            <p>This page contains casino games and entertainment content. Use Tab to navigate through interactive elements.</p>
        </div>
        {hero_section}
        {content_sections}
    </main>
    
    {footer}
    {scripts}
    <!-- Build ID: {self._generate_build_id()} -->
</body>
</html>"""
        
        return template
    
    def generate_games_template(self, content_data: Dict[str, Any]) -> str:
        """Generate unique games listing template"""
        meta_tags = self._generate_meta_tags(content_data, page_type="games")
        head_section = self._generate_head_section(content_data)
        navigation = self._generate_navigation(content_data)
        games_header = self._generate_games_header(content_data)
        games_grid = self._generate_games_grid(content_data)
        footer = self._generate_footer(content_data)
        scripts = self._generate_scripts()
        
        template = f"""<!DOCTYPE html>
<html{self._generate_html_attributes()}>
<head>
{meta_tags}
{head_section}
</head>
<body{self._generate_body_attributes()}>
    {navigation}
    
    <main class="main-wrapper" id="mainWrapper">
        {games_header}
        {games_grid}
    </main>
    
    {footer}
    {scripts}
</body>
</html>"""
        
        return template
    
    def generate_game_detail_template(self, content_data: Dict[str, Any]) -> str:
        """Generate unique individual game template"""
        meta_tags = self._generate_meta_tags(content_data, page_type="game")
        head_section = self._generate_head_section(content_data)
        navigation = self._generate_navigation(content_data)
        breadcrumb = self._generate_breadcrumb(content_data)
        game_container = self._generate_game_container(content_data)
        related_games = self._generate_related_games(content_data)
        footer = self._generate_footer(content_data)
        scripts = self._generate_scripts()
        
        template = f"""<!DOCTYPE html>
<html{self._generate_html_attributes()}>
<head>
{meta_tags}
{head_section}
</head>
<body{self._generate_body_attributes()}>
    {navigation}
    
    <main class="main-wrapper" id="mainWrapper">
        {breadcrumb}
        {game_container}
        {related_games}
    </main>
    
    {footer}
    {scripts}
</body>
</html>"""
        
        return template
    
    def _generate_meta_tags(self, content_data: Dict[str, Any], page_type: str = "homepage") -> str:
        """Generate randomized meta tags"""
        base_meta = [
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'<title>{content_data.get("site_name", "Casino")} - {content_data.get("site_tagline", "Games")}</title>',
            f'<meta name="description" content="{content_data.get("meta_description", "Play exciting casino games")}">',
            '<meta name="robots" content="index, follow">',
            f'<link rel="canonical" href="{content_data.get("canonical_url", "/")}">',
        ]
        
        # Add random gaming-specific meta tags
        gaming_meta = [
            '<meta name="rating" content="general">',
            '<meta name="distribution" content="global">',
            '<meta name="revisit-after" content="7 days">',
            '<meta name="author" content="Casino Generator">',
            '<meta name="generator" content="Dynamic Casino Builder">',
        ]
        
        # Random social media meta tags
        social_meta = [
            f'<meta property="og:title" content="{content_data.get("site_name", "Casino")}">',
            f'<meta property="og:description" content="{content_data.get("meta_description", "Play games")}">',
            '<meta property="og:type" content="website">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]
        
        # Randomize order and selection
        all_meta = base_meta + random.sample(gaming_meta, random.randint(2, 4)) + social_meta
        random.shuffle(all_meta)
        
        return "    " + "\n    ".join(all_meta)
    
    def _generate_head_section(self, content_data: Dict[str, Any]) -> str:
        """Generate head section with framework CSS and custom styles"""
        framework_css = self._get_framework_css()
        font_imports = self._generate_font_imports(content_data)
        custom_css = self._generate_custom_css(content_data)
        
        # Random preload/prefetch hints
        resource_hints = self._generate_resource_hints()
        
        return f"""    {resource_hints}
    {font_imports}
    {framework_css}
    <style>
{custom_css}
    </style>"""
    
    def _get_framework_css(self) -> str:
        """Get CSS framework CDN links based on selected framework"""
        if self.config.framework == Framework.TAILWIND:
            # Tailwind CSS with custom configuration
            colors = self._get_theme_colors()
            return f'''    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'primary': '{colors["primary"]}',
                        'secondary': '{colors["secondary"]}',
                        'accent': '{colors["accent"]}',
                        'background': '{colors["background"]}',
                        'surface': '{colors["surface"]}'
                    }},
                    fontFamily: {{
                        'heading': ['Poppins', 'system-ui', 'sans-serif'],
                        'body': ['Inter', 'system-ui', 'sans-serif']
                    }},
                    animation: {{
                        'float': 'float 6s ease-in-out infinite',
                        'glow': 'glow 2s ease-in-out infinite alternate',
                        'slideIn': 'slideIn 0.3s ease-out'
                    }}
                }}
            }}
        }}
    </script>'''
        elif self.config.framework == Framework.BOOTSTRAP:
            # Bootstrap 5 with custom CSS variables
            return '''    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" defer></script>'''
        elif self.config.framework == Framework.BULMA:
            # Bulma CSS framework
            return '''    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">'''
        elif self.config.framework == Framework.MODERN_CSS:
            # Modern CSS with container queries and advanced features
            return '''    <!-- Modern CSS with container queries and advanced features -->'''
        else:
            # Vanilla CSS with custom grid system
            return '''    <!-- Vanilla CSS with custom design system -->'''
    
    def _generate_font_imports(self, content_data: Dict[str, Any]) -> str:
        """Generate font imports with random variation"""
        fonts = [
            "Poppins:wght@300;400;600;700;900",
            "Inter:wght@300;400;500;600;700",
            "Montserrat:wght@300;400;600;700;800",
            "Roboto:wght@300;400;500;700;900",
            "Open+Sans:wght@300;400;600;700;800"
        ]
        
        primary_font = random.choice(fonts)
        
        return f"""    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family={primary_font}&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">"""
    
    def _generate_custom_css(self, content_data: Dict[str, Any]) -> str:
        """Generate custom CSS based on configuration"""
        css_variables = self._generate_css_variables(content_data)
        base_styles = self._generate_base_styles()
        navigation_styles = self._generate_navigation_styles()
        component_styles = self._generate_component_styles()
        animation_styles = self._generate_animation_styles()
        responsive_styles = self._generate_responsive_styles()
        
        return f"""        /* CSS Variables */
        :root {{
{css_variables}
        }}
        
        /* Base Styles */
{base_styles}
        
        /* Navigation Styles */
{navigation_styles}
        
        /* Component Styles */
{component_styles}
        
        /* Animation Styles */
{animation_styles}
        
        /* Responsive Styles */
{responsive_styles}"""
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """Get theme colors based on color scheme"""
        color_schemes = {
            "dark_gradient": {
                "primary": "#1a1a2e",
                "secondary": "#16213e", 
                "accent": "#7c77c6",
                "background": "#0f0f1e",
                "surface": "#1e1e2e"
            },
            "neon_cyber": {
                "primary": "#00ffff",
                "secondary": "#ff00ff",
                "accent": "#ffff00", 
                "background": "#0a0a0a",
                "surface": "#1a1a1a"
            },
            "warm_casino": {
                "primary": "#d4af37",
                "secondary": "#8b0000",
                "accent": "#ff6b35",
                "background": "#1a0e0e",
                "surface": "#2a1a1a"
            },
            "cool_blue": {
                "primary": "#4a90e2",
                "secondary": "#357abd",
                "accent": "#5dade2",
                "background": "#0e1a2a",
                "surface": "#1a2a3a"
            },
            "purple_gold": {
                "primary": "#6a4c93",
                "secondary": "#9b5de5",
                "accent": "#f1c40f",
                "background": "#1a0e2a",
                "surface": "#2a1a3a"
            },
            "red_black": {
                "primary": "#e74c3c",
                "secondary": "#c0392b",
                "accent": "#f39c12",
                "background": "#0e0e0e",
                "surface": "#1e1e1e"
            },
            "green_emerald": {
                "primary": "#00b894",
                "secondary": "#00a085",
                "accent": "#fdcb6e",
                "background": "#0e1a0e", 
                "surface": "#1a2a1a"
            }
        }
        
        return color_schemes.get(self.config.color_scheme, color_schemes["dark_gradient"])
    
    def _generate_css_variables(self, content_data: Dict[str, Any]) -> str:
        """Generate CSS custom properties"""
        design_system = content_data.get('design_system', {})
        colors = design_system.get('colors', {})
        
        # Random color variations
        primary_variations = self._generate_color_variations(colors.get('primary', '#1a1a2e'))
        accent_variations = self._generate_color_variations(colors.get('accent', '#7c77c6'))
        
        variables = [
            f"            --primary-color: {colors.get('primary', '#1a1a2e')};",
            f"            --accent-color: {colors.get('accent', '#7c77c6')};",
            f"            --background-color: {colors.get('background', '#0f0f1e')};",
            f"            --surface-color: {colors.get('surface', '#1e1e2e')};",
            f"            --text-color: {colors.get('text', '#ffffff')};",
            f"            --text-secondary: {colors.get('text_secondary', 'rgba(255,255,255,0.7)')};",
            "            --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);",
            "            --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);",
            "            --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);",
            "            --border-radius-sm: 8px;",
            "            --border-radius-md: 12px;",
            "            --border-radius-lg: 20px;",
            "            --shadow-sm: 0 2px 8px rgba(0,0,0,0.1);",
            "            --shadow-md: 0 4px 16px rgba(0,0,0,0.15);",
            "            --shadow-lg: 0 8px 32px rgba(0,0,0,0.2);",
            f"            --z-fixed: {random.randint(1000, 1100)};",
            f"            --z-modal: {random.randint(1200, 1300)};",
        ]
        
        return "\n".join(variables)
    
    def _generate_navigation(self, content_data: Dict[str, Any]) -> str:
        """Generate navigation based on selected pattern"""
        site_name = content_data.get('site_name', 'Casino')
        nav_items = [
            ('Home', '/', 'fas fa-home'),
            ('Games', '/games.html', 'fas fa-gamepad'),
            ('About', '/about.html', 'fas fa-info-circle'),
            ('Contact', '/contact.html', 'fas fa-envelope'),
        ]
        
        if self.config.navigation == NavigationPattern.SIDEBAR:
            return self._generate_sidebar_navigation(site_name, nav_items)
        elif self.config.navigation == NavigationPattern.TOP_NAV:
            return self._generate_top_navigation(site_name, nav_items)
        elif self.config.navigation == NavigationPattern.HAMBURGER:
            return self._generate_hamburger_navigation(site_name, nav_items)
        elif self.config.navigation == NavigationPattern.BOTTOM_NAV:
            return self._generate_bottom_navigation(site_name, nav_items)
        elif self.config.navigation == NavigationPattern.FLOATING_ACTION:
            return self._generate_floating_navigation(site_name, nav_items)
        else:  # TAB_BAR
            return self._generate_tab_navigation(site_name, nav_items)
    
    def _generate_sidebar_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate accessible sidebar navigation with anti-fingerprinting compatible class names"""
        # Skip link for accessibility
        skip_link = """    <a href="#main-content" class="skip-link" tabindex="1">Skip to main content</a>"""
        
        nav_html = f"""{skip_link}
    <!-- Navigation: Anti-fingerprinting compatible -->
    <nav class="sidebar" id="sidebar" role="navigation" aria-label="Main navigation">
        <div class="sidebar-header">
            <div class="logo" role="banner">
                <h1>{site_name}</h1>
            </div>
        </div>
        <div class="sidebar-nav" role="menubar">"""
        
        for i, (name, url, icon) in enumerate(nav_items):
            active_class = " active" if name == "Home" else ""
            is_current = 'aria-current="page"' if name == "Home" else ''
            nav_html += f"""
            <a href="{url}" 
               class="nav-item{active_class}" 
               role="menuitem" 
               tabindex="{i+2}"
               {is_current}
               aria-describedby="nav-{name.lower()}-desc">
                <i class="{icon}" aria-hidden="true"></i> 
                <span>{name}</span>
                <span id="nav-{name.lower()}-desc" class="sr-only">Navigate to {name} page</span>
            </a>"""
        
        nav_html += f"""
        </div>
        <button class="sidebar-toggle" 
                onclick="toggleSidebar()" 
                aria-label="Toggle sidebar navigation" 
                aria-expanded="true"
                aria-controls="sidebar">
            <i class="fas fa-chevron-left" aria-hidden="true"></i>
        </button>
    </nav>
    
    <button class="mobile-sidebar-toggle" 
            onclick="toggleMobileSidebar()" 
            id="mobileSidebarToggle" 
            aria-label="Open mobile navigation menu"
            aria-expanded="false"
            aria-controls="sidebar">
        <i class="fas fa-bars" aria-hidden="true"></i>
    </button>
    
    <div class="sidebar-overlay" 
         id="sidebarOverlay" 
         onclick="closeMobileSidebar()" 
         aria-hidden="true"></div>"""
        
        return nav_html
    
    def _generate_hero_section(self, content_data: Dict[str, Any]) -> str:
        """Generate hero section based on style configuration"""
        hero_data = content_data.get('hero', {})
        
        if self.config.hero_style == "fullscreen_overlay":
            return self._generate_fullscreen_hero(hero_data)
        elif self.config.hero_style == "split_hero":
            return self._generate_split_hero(hero_data)
        elif self.config.hero_style == "video_background":
            return self._generate_video_hero(hero_data)
        elif self.config.hero_style == "gradient_animated":
            return self._generate_gradient_hero(hero_data)
        elif self.config.hero_style == "particles":
            return self._generate_particles_hero(hero_data)
        elif self.config.hero_style == "carousel":
            return self._generate_carousel_hero(hero_data)
        else:  # minimalist
            return self._generate_minimalist_hero(hero_data)
    
    def _generate_fullscreen_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate fullscreen overlay hero with anti-fingerprinting compatible classes"""
        return f"""        <section class="hero hero-fullscreen" style="background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.4)), url('{hero_data.get('background_image', 'images/hero.jpg')}'); background-size: cover; background-position: center;">
            <div class="hero-content">
                <h1 class="hero-title">{hero_data.get('title', 'Welcome to Casino')}</h1>
                <p class="hero-description">{hero_data.get('description', 'Experience the best casino games')}</p>
                <div class="hero-buttons">
                    <a href="{hero_data.get('cta_url', '/games.html')}" class="btn btn-primary btn-large">
                        <i class="{hero_data.get('cta_icon', 'fas fa-play')}"></i> {hero_data.get('cta_text', 'Play Now')}
                    </a>
                </div>
            </div>
        </section>"""
    
    def _generate_split_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate split hero section"""
        return f"""        <section class="hero hero-split">
            <div class="hero-grid">
                <div class="hero-content">
                    <h1 class="hero-title">{hero_data.get('title', 'Welcome to Casino')}</h1>
                    <p class="hero-description">{hero_data.get('description', 'Experience the best casino games')}</p>
                    <div class="hero-buttons">
                        <a href="{hero_data.get('cta_url', '/games.html')}" class="btn btn-primary btn-large">
                            <i class="{hero_data.get('cta_icon', 'fas fa-play')}"></i> {hero_data.get('cta_text', 'Play Now')}
                        </a>
                        <a href="/about.html" class="btn btn-outline">Learn More</a>
                    </div>
                </div>
                <div class="hero-image">
                    <img src="{hero_data.get('image', 'images/hero-split.jpg')}" alt="Casino Games" loading="lazy">
                </div>
            </div>
        </section>"""
    
    def _generate_video_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate video background hero"""
        return f"""        <section class="hero hero-video">
            <video class="hero-video" autoplay muted loop>
                <source src="{hero_data.get('video', 'videos/hero.mp4')}" type="video/mp4">
                <img src="{hero_data.get('fallback_image', 'images/hero.jpg')}" alt="Casino">
            </video>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <h1 class="hero-title">{hero_data.get('title', 'Ultimate Casino Experience')}</h1>
                <p class="hero-description">{hero_data.get('description', 'Immerse yourself in premium gaming')}</p>
                <div class="hero-buttons">
                    <a href="{hero_data.get('cta_url', '/games.html')}" class="btn btn-primary btn-large">
                        <i class="{hero_data.get('cta_icon', 'fas fa-play')}"></i> {hero_data.get('cta_text', 'Start Playing')}
                    </a>
                </div>
            </div>
        </section>"""
    
    def _generate_gradient_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate animated gradient hero"""
        gradient_colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
        return f"""        <section class="hero hero-gradient">
            <div class="gradient-bg"></div>
            <div class="hero-content">
                <h1 class="hero-title gradient-text">{hero_data.get('title', 'Next Level Gaming')}</h1>
                <p class="hero-description">{hero_data.get('description', 'Experience casino games like never before')}</p>
                <div class="hero-buttons">
                    <a href="{hero_data.get('cta_url', '/games.html')}" class="btn btn-gradient btn-large">
                        <i class="{hero_data.get('cta_icon', 'fas fa-rocket')}"></i> {hero_data.get('cta_text', 'Launch Games')}
                    </a>
                </div>
            </div>
        </section>"""
    
    def _generate_particles_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate particle effect hero"""
        return f"""        <section class="hero hero-particles">
            <div id="particles-js"></div>
            <div class="hero-content">
                <h1 class="hero-title">{hero_data.get('title', 'Cosmic Casino')}</h1>
                <p class="hero-description">{hero_data.get('description', 'Gaming in a galaxy far, far away')}</p>
                <div class="hero-buttons">
                    <a href="{hero_data.get('cta_url', '/games.html')}" class="btn btn-primary btn-large pulse">
                        <i class="{hero_data.get('cta_icon', 'fas fa-star')}"></i> {hero_data.get('cta_text', 'Enter Universe')}
                    </a>
                </div>
            </div>
        </section>"""
    
    def _generate_carousel_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate carousel hero section"""
        slides = hero_data.get('slides', [{'title': 'Welcome', 'description': 'Play amazing games', 'image': 'images/hero1.jpg'}])
        carousel_html = f"""        <section class="hero hero-carousel">
            <div class="carousel-container">"""
        
        for i, slide in enumerate(slides[:3]):  # Limit to 3 slides
            active_class = "active" if i == 0 else ""
            carousel_html += f"""
                <div class="carousel-slide {active_class}" style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.3)), url('{slide.get('image', 'images/hero.jpg')}'); background-size: cover;">
                    <div class="hero-content">
                        <h1 class="hero-title">{slide.get('title', 'Casino Games')}</h1>
                        <p class="hero-description">{slide.get('description', 'Play and win big')}</p>
                        <div class="hero-buttons">
                            <a href="{slide.get('cta_url', '/games.html')}" class="btn btn-primary btn-large">
                                <i class="{slide.get('cta_icon', 'fas fa-play')}"></i> {slide.get('cta_text', 'Play Now')}
                            </a>
                        </div>
                    </div>
                </div>"""
        
        carousel_html += f"""
            </div>
            <div class="carousel-nav">
                <button class="carousel-prev" onclick="changeSlide(-1)">❮</button>
                <button class="carousel-next" onclick="changeSlide(1)">❯</button>
            </div>
            <div class="carousel-dots">
                {' '.join([f'<span class="dot {"active" if i == 0 else ""}" onclick="currentSlide({i+1})"></span>' for i in range(len(slides[:3]))])}
            </div>
        </section>"""
        
        return carousel_html
    
    def _generate_minimalist_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate minimalist hero section"""
        return f"""        <section class="hero hero-minimalist">
            <div class="hero-content">
                <h1 class="hero-title minimal">{hero_data.get('title', 'Pure Gaming')}</h1>
                <p class="hero-description minimal">{hero_data.get('description', 'Simple. Clean. Fun.')}</p>
                <div class="hero-buttons minimal">
                    <a href="{hero_data.get('cta_url', '/games.html')}" class="btn btn-minimal">
                        {hero_data.get('cta_text', 'Play')}
                    </a>
                </div>
            </div>
        </section>"""
    
    def _generate_content_sections(self, content_data: Dict[str, Any]) -> str:
        """Generate content sections with anti-fingerprinting compatible classes"""
        content_sections = content_data.get('content_sections', [])
        
        sections_html = []
        for i, section in enumerate(content_sections):
            items = section.get('items', [])
            cards_html = ''.join(f"\n                    {self._generate_game_card(item)}" for item in items)
            
            section_html = f"""        
        <section class="content-section">
            <div class="section-header">
                <h2 class="section-title">{section.get('title', f'Section {i+1}')}</h2>
                <p class="section-subtitle">{section.get('subtitle', '')}</p>
            </div>
            <div class="cards-container">
                <div class="cards-slider" id="section{i}Slider">{cards_html}
                </div>
            </div>
        </section>"""
            
            sections_html.append(section_html)
        
        return ''.join(sections_html)
    
    def _generate_game_card(self, item: Dict[str, Any]) -> str:
        """Generate game card based on style configuration"""
        if self.config.card_style == "hover_overlay":
            return self._generate_hover_overlay_card(item)
        elif self.config.card_style == "flip_card":
            return self._generate_flip_card(item)
        elif self.config.card_style == "slide_up":
            return self._generate_slide_up_card(item)
        elif self.config.card_style == "glassmorphism":
            return self._generate_glassmorphism_card(item)
        elif self.config.card_style == "neumorphism":
            return self._generate_neumorphism_card(item)
        elif self.config.card_style == "gradient_border":
            return self._generate_gradient_border_card(item)
        else:  # zoom_hover
            return self._generate_zoom_hover_card(item)
    
    def _generate_hover_overlay_card(self, item: Dict[str, Any]) -> str:
        """Generate hover overlay style card with anti-fingerprinting compatible classes"""
        return f"""                    <div class="card card-hover-overlay" data-game-slug="{item.get('slug', 'unknown')}">
                        <img src="{item.get('image', 'images/placeholder.jpg')}" 
                             alt="{item.get('title', 'Game')}" 
                             class="card-thumbnail" 
                             loading="lazy"
                             onerror="handleImageError(this)"
                             onload="handleImageLoad(this)">
                        <div class="card-overlay">
                            <div class="card-info">
                                <h3 class="card-title">{item.get('title', 'Game')}</h3>
                                <a href="{item.get('url', '#')}" 
                                   class="card-cta" 
                                   data-game-title="{item.get('title', 'Game')}"
                                   data-game-provider="{item.get('provider', 'Unknown')}"
                                   onclick="trackGameClick('{item.get('title', 'Game')}', '{item.get('url', '#')}', '{item.get('provider', 'Unknown')}')">
                                   <i class="fas fa-play"></i>
                                   {item.get('cta_text', 'Play Now')}
                                </a>
                            </div>
                        </div>
                    </div>"""
    
    def _generate_flip_card(self, item: Dict[str, Any]) -> str:
        """Generate flip card with anti-fingerprinting compatible classes"""
        return f"""                    <div class="card card-flip" data-game-slug="{item.get('slug', 'unknown')}">
                        <div class="card-inner">
                            <div class="card-front">
                                <img src="{item.get('image', 'images/placeholder.jpg')}" 
                                     alt="{item.get('title', 'Game')}" 
                                     class="card-thumbnail"
                                     loading="lazy"
                                     onerror="handleImageError(this)"
                                     onload="handleImageLoad(this)">
                            </div>
                            <div class="card-back">
                                <div class="card-info">
                                    <h3 class="card-title">{item.get('title', 'Game')}</h3>
                                    <p class="card-description">{item.get('description', 'Amazing casino game')}</p>
                                    <a href="{item.get('url', '#')}" class="card-cta">
                                        <i class="fas fa-play"></i> {item.get('cta_text', 'Play Now')}
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>"""
    
    def _generate_slide_up_card(self, item: Dict[str, Any]) -> str:
        """Generate slide up card with anti-fingerprinting compatible classes"""
        return f"""                    <div class="card card-slide-up" data-game-slug="{item.get('slug', 'unknown')}">
                        <img src="{item.get('image', 'images/placeholder.jpg')}" 
                             alt="{item.get('title', 'Game')}" 
                             class="card-thumbnail"
                             loading="lazy"
                             onerror="handleImageError(this)"
                             onload="handleImageLoad(this)">
                        <div class="card-info slide-panel">
                            <h3 class="card-title">{item.get('title', 'Game')}</h3>
                            <p class="card-provider">{item.get('provider', 'Provider')}</p>
                            <a href="{item.get('url', '#')}" class="card-cta">
                                <i class="fas fa-gamepad"></i> {item.get('cta_text', 'Play')}
                            </a>
                        </div>
                    </div>"""
    
    def _generate_glassmorphism_card(self, item: Dict[str, Any]) -> str:
        """Generate glassmorphism card with anti-fingerprinting compatible classes"""
        return f"""                    <div class="card card-glass" data-game-slug="{item.get('slug', 'unknown')}">
                        <div class="glass-bg"></div>
                        <img src="{item.get('image', 'images/placeholder.jpg')}" 
                             alt="{item.get('title', 'Game')}" 
                             class="card-thumbnail"
                             loading="lazy"
                             onerror="handleImageError(this)"
                             onload="handleImageLoad(this)">
                        <div class="card-content">
                            <h3 class="card-title glass-text">{item.get('title', 'Game')}</h3>
                            <div class="card-actions">
                                <a href="{item.get('url', '#')}" class="card-cta glass-btn">
                                    <i class="fas fa-play"></i>
                                </a>
                            </div>
                        </div>
                    </div>"""
    
    def _generate_neumorphism_card(self, item: Dict[str, Any]) -> str:
        """Generate neumorphism card with anti-fingerprinting compatible classes"""
        return f"""                    <div class="card card-neomorphism" data-game-slug="{item.get('slug', 'unknown')}">
                        <div class="neomorphism-inner">
                            <img src="{item.get('image', 'images/placeholder.jpg')}" 
                                 alt="{item.get('title', 'Game')}" 
                                 class="card-thumbnail neomorphism-image"
                                 loading="lazy"
                                 onerror="handleImageError(this)"
                                 onload="handleImageLoad(this)">
                            <div class="card-info">
                                <h3 class="card-title neomorphism-title">{item.get('title', 'Game')}</h3>
                                <a href="{item.get('url', '#')}" class="card-cta neomorphism-btn">
                                    {item.get('cta_text', 'Play')}
                                </a>
                            </div>
                        </div>
                    </div>"""
    
    def _generate_gradient_border_card(self, item: Dict[str, Any]) -> str:
        """Generate gradient border card with anti-fingerprinting compatible classes"""
        return f"""                    <div class="card card-gradient-border" data-game-slug="{item.get('slug', 'unknown')}">
                        <div class="gradient-border"></div>
                        <div class="card-content">
                            <img src="{item.get('image', 'images/placeholder.jpg')}" 
                                 alt="{item.get('title', 'Game')}" 
                                 class="card-thumbnail"
                                 loading="lazy"
                                 onerror="handleImageError(this)"
                                 onload="handleImageLoad(this)">
                            <div class="card-overlay gradient-overlay">
                                <h3 class="card-title">{item.get('title', 'Game')}</h3>
                                <a href="{item.get('url', '#')}" class="card-cta gradient-cta">
                                    <i class="fas fa-star"></i> {item.get('cta_text', 'Play Now')}
                                </a>
                            </div>
                        </div>
                    </div>"""
    
    def _generate_zoom_hover_card(self, item: Dict[str, Any]) -> str:
        """Generate zoom hover card with anti-fingerprinting compatible classes"""
        return f"""                    <div class="card card-zoom" data-game-slug="{item.get('slug', 'unknown')}">
                        <div class="card-image-container">
                            <img src="{item.get('image', 'images/placeholder.jpg')}" 
                                 alt="{item.get('title', 'Game')}" 
                                 class="card-thumbnail zoom-image"
                                 loading="lazy"
                                 onerror="handleImageError(this)"
                                 onload="handleImageLoad(this)">
                            <div class="zoom-overlay">
                                <a href="{item.get('url', '#')}" class="zoom-cta">
                                    <i class="fas fa-search-plus"></i>
                                </a>
                            </div>
                        </div>
                        <div class="card-info">
                            <h3 class="card-title">{item.get('title', 'Game')}</h3>
                            <p class="card-meta">{item.get('provider', 'Provider')} • {item.get('category', 'Casino')}</p>
                        </div>
                    </div>"""
    
    def _generate_scripts(self) -> str:
        """Generate JavaScript with anti-fingerprinting compatible function names"""
        return f"""    <script>
        // Navigation functionality - standard function names for anti-fingerprinting
        function toggleSidebar() {{
            const sidebar = document.getElementById('sidebar');
            const mainWrapper = document.getElementById('mainWrapper');
            
            sidebar.classList.toggle('collapsed');
            if (sidebar.classList.contains('collapsed')) {{
                mainWrapper.style.marginLeft = '60px';
            }} else {{
                mainWrapper.style.marginLeft = '280px';
            }}
        }}

        function toggleMobileSidebar() {{
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebarOverlay');
            
            sidebar.classList.add('active');
            overlay.classList.add('active');
        }}

        function closeMobileSidebar() {{
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebarOverlay');
            
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        }}

        // Image error handling
        function handleImageError(img) {{
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
        }}

        function handleImageLoad(img) {{
            img.style.opacity = '1';
        }}

        // Game tracking
        function trackGameClick(gameTitle, gameUrl, gameProvider) {{
            console.log('Game clicked:', {{ gameTitle, gameUrl, gameProvider }});
        }}

        // Game page functionality
        function hideLoading() {{
            const loading = document.getElementById('gameLoading');
            if (loading) {{
                loading.style.display = 'none';
            }}
        }}

        function showError() {{
            const loading = document.getElementById('gameLoading');
            if (loading) {{
                loading.innerHTML = '<p>Error loading game. Please try again later.</p>';
            }}
        }}

        function toggleFullscreen() {{
            const container = document.querySelector('.game-iframe-container');
            const btn = document.querySelector('.fullscreen-btn i');
            
            if (!document.fullscreenElement) {{
                container.requestFullscreen().then(() => {{
                    btn.className = 'fas fa-compress';
                }});
            }} else {{
                document.exitFullscreen().then(() => {{
                    btn.className = 'fas fa-expand';
                }});
            }}
        }}

        // Additional navigation functions for different navigation patterns
        function toggleHamburgerMenu() {{
            const menu = document.querySelector('.nav-menu');
            const toggle = document.querySelector('.hamburger-toggle');
            
            if (menu && toggle) {{
                menu.classList.toggle('active');
                const isExpanded = menu.classList.contains('active');
                toggle.setAttribute('aria-expanded', isExpanded);
                
                // Change icon
                const icon = toggle.querySelector('i');
                if (icon) {{
                    icon.className = isExpanded ? 'fas fa-times' : 'fas fa-bars';
                }}
            }}
        }}

        function toggleFabMenu() {{
            const fabMenu = document.querySelector('.fab-menu');
            const fabMain = document.querySelector('.fab-main');
            
            if (fabMenu && fabMain) {{
                fabMenu.classList.toggle('active');
                const isExpanded = fabMenu.classList.contains('active');
                fabMain.setAttribute('aria-expanded', isExpanded);
                
                // Rotate main button
                const icon = fabMain.querySelector('i');
                if (icon) {{
                    icon.style.transform = isExpanded ? 'rotate(45deg)' : 'rotate(0deg)';
                }}
            }}
        }}

        function changeSlide(direction) {{
            const slides = document.querySelectorAll('.carousel-slide');
            const dots = document.querySelectorAll('.dot');
            let activeIndex = Array.from(slides).findIndex(slide => slide.classList.contains('active'));
            
            slides[activeIndex].classList.remove('active');
            dots[activeIndex].classList.remove('active');
            
            activeIndex += direction;
            if (activeIndex >= slides.length) activeIndex = 0;
            if (activeIndex < 0) activeIndex = slides.length - 1;
            
            slides[activeIndex].classList.add('active');
            dots[activeIndex].classList.add('active');
        }}

        function currentSlide(index) {{
            const slides = document.querySelectorAll('.carousel-slide');
            const dots = document.querySelectorAll('.dot');
            
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            slides[index - 1].classList.add('active');
            dots[index - 1].classList.add('active');
        }}

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Set active navigation item
            const currentPage = window.location.pathname;
            const navItems = document.querySelectorAll('.nav-item');
            
            navItems.forEach(item => {{
                const href = item.getAttribute('href');
                if (href === currentPage || (currentPage === '/' && href === '/')) {{
                    item.classList.add('active');
                }} else {{
                    item.classList.remove('active');
                }}
            }});
            
            // Close mobile sidebar when clicking on nav items
            navItems.forEach(item => {{
                item.addEventListener('click', closeMobileSidebar);
            }});
            
            // Handle window resize
            window.addEventListener('resize', function() {{
                if (window.innerWidth > 768) {{
                    closeMobileSidebar();
                }}
            }});
        }});
    </script>"""
    
    # Helper methods for generating various components and styles
    def _generate_html_attributes(self) -> str:
        """Generate random HTML tag attributes"""
        lang_codes = ["en", "en-US", "en-GB"]
        attrs = [f' lang="{random.choice(lang_codes)}"']
        
        if random.choice([True, False]):
            attrs.append(f' data-theme="{random.choice(["dark", "casino", "neon"])}"')
        
        return "".join(attrs)
    
    def _generate_body_attributes(self) -> str:
        """Generate random body tag attributes"""
        attrs = []
        
        if random.choice([True, False]):
            attrs.append(f' data-framework="{self.config.framework.value[0]}"')
        
        if random.choice([True, False]):
            attrs.append(f' data-layout="{self.config.layout.value}"')
            
        return "".join(attrs)
    
    def _generate_random_comment(self) -> str:
        """Generate random comment for uniqueness"""
        comments = [
            "Generated template variation",
            "Dynamic casino template",
            "Unique structure build",
            "Casino generator output",
            "Template fingerprint variant"
        ]
        return f"{random.choice(comments)} - {random.randint(1000, 9999)}"
    
    def _generate_build_id(self) -> str:
        """Generate random build ID"""
        return f"build-{random.randint(100000, 999999)}"
    
    def _generate_resource_hints(self) -> str:
        """Generate random preload/prefetch hints"""
        hints = []
        
        if random.choice([True, False]):
            hints.append('<link rel="preload" href="/css/style.css" as="style">')
        
        if random.choice([True, False]):
            hints.append('<link rel="prefetch" href="/images/hero.jpg">')
            
        return "\n    ".join(hints)
    
    def _generate_color_variations(self, base_color: str) -> List[str]:
        """Generate color variations from base color"""
        # This would implement color manipulation logic
        return [base_color, base_color, base_color]  # Simplified for now
    
    # Additional helper methods would continue here for:
    # - _generate_base_styles()
    # - _generate_navigation_styles() 
    # - _generate_component_styles()
    # - _generate_animation_styles()
    # - _generate_responsive_styles()
    # - Other template generation methods
    
    def _generate_layout_system(self) -> str:
        """Generate layout system based on configuration"""
        if self.config.layout == LayoutStructure.GRID_12:
            return """        .grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: var(--grid-gap, 1.5rem);
        }
        
        .col-1 { grid-column: span 1; }
        .col-2 { grid-column: span 2; }
        .col-3 { grid-column: span 3; }
        .col-4 { grid-column: span 4; }
        .col-6 { grid-column: span 6; }
        .col-8 { grid-column: span 8; }
        .col-9 { grid-column: span 9; }
        .col-12 { grid-column: span 12; }"""
        elif self.config.layout == LayoutStructure.GRID_16:
            return """        .grid {
            display: grid;
            grid-template-columns: repeat(16, 1fr);
            gap: var(--grid-gap, 1rem);
        }
        
        .col-1 { grid-column: span 1; }
        .col-2 { grid-column: span 2; }
        .col-4 { grid-column: span 4; }
        .col-8 { grid-column: span 8; }
        .col-12 { grid-column: span 12; }
        .col-16 { grid-column: span 16; }"""
        elif self.config.layout == LayoutStructure.CSS_GRID:
            return """        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: var(--grid-gap, 2rem);
        }
        
        .grid-auto {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
        }
        
        .grid-dense {
            grid-auto-flow: dense;
        }"""
        elif self.config.layout == LayoutStructure.FLEXBOX:
            return """        .flex {
            display: flex;
            flex-wrap: wrap;
            gap: var(--flex-gap, 1.5rem);
        }
        
        .flex-1 { flex: 1; }
        .flex-2 { flex: 2; }
        .flex-3 { flex: 3; }
        .flex-none { flex: none; }
        
        .justify-center { justify-content: center; }
        .justify-between { justify-content: space-between; }
        .items-center { align-items: center; }"""
        else:
            return """        .layout {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }"""
    
    def _generate_base_styles(self) -> str:
        """Generate base CSS styles with layout system and anti-fingerprinting compatible classes"""
        layout_styles = self._generate_layout_system()
        
        return f"""        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
            overflow-x: hidden;
        }}
        
        .main-wrapper {{
            margin-left: 280px;
            min-height: 100vh;
            transition: margin-left var(--transition-normal);
        }}
        
        /* Layout System */
{layout_styles}
        
        /* Container Widths */
        .container {{
            max-width: {random.choice(['1200px', '1400px', '1600px'])};
            margin: 0 auto;
            padding: 0 {random.choice(['1rem', '1.5rem', '2rem'])};
        }}
        
        /* Section Patterns */
        .section {{
            padding: {random.choice(['4rem 0', '5rem 0', '6rem 0'])};
            position: relative;
        }}
        
        .section:nth-child(even) {{
            background: rgba(255, 255, 255, {random.choice(['0.02', '0.03', '0.05'])});
        }}
        
        /* Accessibility Styles */
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}
        
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--accent-color);
            color: white;
            padding: 8px;
            text-decoration: none;
            z-index: 9999;
            border-radius: 4px;
            transition: top 0.3s;
        }}
        
        .skip-link:focus {{
            top: 6px;
        }}
        
        /* Focus indicators */
        a:focus,
        button:focus,
        input:focus,
        select:focus,
        textarea:focus {{
            outline: 2px solid var(--accent-color);
            outline-offset: 2px;
        }}
        
        /* High contrast mode support */
        @media (prefers-contrast: high) {{
            .card {{
                border: 2px solid currentColor;
            }}
            
            .btn {{
                border: 2px solid currentColor;
            }}
        }}
        
        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}"""
    
    def _generate_navigation_styles(self) -> str:
        """Generate navigation styles based on pattern"""
        if self.config.navigation == NavigationPattern.SIDEBAR:
            return f"""        .sidebar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 280px;
            height: 100vh;
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            z-index: var(--z-fixed);
            transition: transform var(--transition-normal);
        }}
        
        .sidebar-header {{
            padding: 2rem 1.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .logo {{
            font-size: 1.8rem;
            font-weight: 900;
            color: var(--accent-color);
            text-align: center;
        }}
        
        .nav-item {{
            display: flex;
            align-items: center;
            padding: 1.25rem 1.5rem;
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: all var(--transition-normal);
            margin: 0.25rem 0.75rem;
            border-radius: var(--border-radius-md);
        }}
        
        .nav-item:hover,
        .nav-item.active {{
            color: white;
            background: var(--accent-color);
            transform: translateX(8px);
        }}
        
        .nav-item i {{
            margin-right: 0.75rem;
            width: 20px;
        }}
        
        .mobile-sidebar-toggle {{
            display: none;
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: calc(var(--z-fixed) + 1);
            background: var(--accent-color);
            color: white;
            border: none;
            width: 56px;
            height: 56px;
            border-radius: var(--border-radius-md);
            cursor: pointer;
            transition: all var(--transition-fast);
        }}
        
        .mobile-sidebar-toggle:hover {{
            background: color-mix(in srgb, var(--accent-color) 80%, white 20%);
            transform: scale(1.05);
        }}
        
        .sidebar-overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: calc(var(--z-fixed) - 1);
            backdrop-filter: blur(2px);
        }}
        
        .sidebar-overlay.active {{
            display: block;
        }}

        @media (max-width: 768px) {{
            .sidebar {{
                transform: translateX(-100%);
            }}
            
            .sidebar.active {{
                transform: translateX(0);
            }}
            
            .main-wrapper {{
                margin-left: 0;
            }}
            
            .mobile-sidebar-toggle {{
                display: block;
            }}
        }}"""
        elif self.config.navigation == NavigationPattern.TOP_NAV:
            return f"""        .top-nav {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            z-index: var(--z-fixed);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .nav-brand {{
            font-size: 1.5rem;
            font-weight: 900;
            color: var(--accent-color);
        }}
        
        .nav-menu {{
            display: flex;
            align-items: center;
            gap: 2rem;
        }}
        
        .nav-item {{
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: var(--border-radius-sm);
            transition: all var(--transition-normal);
        }}
        
        .nav-item:hover,
        .nav-item.active {{
            color: white;
            background: var(--accent-color);
        }}
        
        .main-wrapper {{
            margin-top: 80px;
            margin-left: 0;
        }}
        
        @media (max-width: 768px) {{
            .nav-menu {{
                display: none;
            }}
        }}"""
        elif self.config.navigation == NavigationPattern.HAMBURGER:
            return f"""        .hamburger-nav {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            z-index: var(--z-fixed);
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .nav-brand {{
            font-size: 1.5rem;
            font-weight: 900;
            color: var(--accent-color);
        }}
        
        .hamburger-toggle {{
            background: transparent;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
        }}
        
        .nav-menu {{
            position: fixed;
            top: 0;
            right: -100%;
            width: 280px;
            height: 100vh;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            padding: 6rem 2rem 2rem;
            transition: right var(--transition-normal);
        }}
        
        .nav-menu.active {{
            right: 0;
        }}
        
        .nav-item {{
            display: block;
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: var(--border-radius-md);
            transition: all var(--transition-normal);
        }}
        
        .nav-item:hover,
        .nav-item.active {{
            color: white;
            background: var(--accent-color);
        }}
        
        .main-wrapper {{
            margin-top: 80px;
            margin-left: 0;
        }}"""
        elif self.config.navigation == NavigationPattern.BOTTOM_NAV:
            return f"""        .bottom-nav {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            z-index: var(--z-fixed);
            padding: 1rem;
            display: flex;
            justify-content: space-around;
            align-items: center;
        }}
        
        .nav-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            color: rgba(255, 255, 255, 0.6);
            text-decoration: none;
            padding: 0.5rem;
            border-radius: var(--border-radius-sm);
            transition: all var(--transition-normal);
            font-size: 0.75rem;
        }}
        
        .nav-item i {{
            font-size: 1.2rem;
            margin-bottom: 0.25rem;
        }}
        
        .nav-item:hover,
        .nav-item.active {{
            color: var(--accent-color);
        }}
        
        .main-wrapper {{
            margin-bottom: 80px;
            margin-left: 0;
        }}"""
        elif self.config.navigation == NavigationPattern.FLOATING_ACTION:
            return f"""        .floating-nav {{
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: var(--z-fixed);
        }}
        
        .fab-main {{
            width: 60px;
            height: 60px;
            background: var(--accent-color);
            border-radius: 50%;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            transition: all var(--transition-normal);
        }}
        
        .fab-main:hover {{
            transform: scale(1.1);
        }}
        
        .fab-menu {{
            position: absolute;
            bottom: 70px;
            right: 0;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            opacity: 0;
            visibility: hidden;
            transition: all var(--transition-normal);
        }}
        
        .fab-menu.active {{
            opacity: 1;
            visibility: visible;
        }}
        
        .fab-item {{
            width: 50px;
            height: 50px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 50%;
            border: none;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all var(--transition-normal);
        }}
        
        .fab-item:hover {{
            background: var(--accent-color);
            transform: scale(1.1);
        }}
        
        .main-wrapper {{
            margin-left: 0;
        }}"""
        elif self.config.navigation == NavigationPattern.TAB_BAR:
            return f"""        .tab-nav {{
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 0 0 2rem 2rem;
            z-index: var(--z-fixed);
            padding: 1rem 2rem;
            display: flex;
            gap: 1rem;
        }}
        
        .tab-item {{
            background: transparent;
            border: 2px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.7);
            padding: 0.75rem 1.5rem;
            border-radius: 2rem;
            cursor: pointer;
            transition: all var(--transition-normal);
            text-decoration: none;
            font-size: 0.9rem;
        }}
        
        .tab-item:hover,
        .tab-item.active {{
            background: var(--accent-color);
            border-color: var(--accent-color);
            color: white;
            transform: translateY(-2px);
        }}
        
        .main-wrapper {{
            margin-top: 100px;
            margin-left: 0;
        }}"""
        else:
            return "        /* Default navigation styles */"
    
    def _generate_component_styles(self) -> str:
        """Generate component styles based on configuration"""
        framework_specific_styles = self._get_framework_specific_styles()
        
        return f"""        .hero {{
            min-height: 70vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
        }}
        
        .hero-content {{
            max-width: 900px;
            padding: 3rem 2rem;
            z-index: 3;
            position: relative;
        }}
        
        .hero-title {{
            font-size: clamp(3rem, 6vw, 5rem);
            font-weight: 900;
            margin-bottom: 1.5rem;
            color: white;
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
        }}
        
        .hero-description {{
            font-size: 1.3rem;
            margin-bottom: 2.5rem;
            color: rgba(255,255,255,0.95);
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem 2rem;
            border: none;
            border-radius: var(--border-radius-md);
            text-decoration: none;
            font-weight: 600;
            transition: all var(--transition-normal);
            cursor: pointer;
        }}
        
        .btn-primary {{
            background: var(--accent-color);
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}
        
        .btn-large {{
            padding: 1.2rem 2.5rem;
            font-size: 1.1rem;
        }}
        
        /* Games Grid Styles */
        .games-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            padding: 2rem;
        }}
        
        .cards-slider {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            padding: 1rem 0;
        }}
        
        .content-section {{
            padding: 4rem 2rem;
        }}
        
        .section-header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        
        .section-title {{
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
            margin-bottom: 1rem;
        }}
        
        .section-subtitle {{
            font-size: 1.2rem;
            color: rgba(255,255,255,0.8);
        }}
        
        .games-header {{
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        }}
        
        .games-header h1 {{
            font-size: 3rem;
            font-weight: 900;
            color: white;
            margin-bottom: 1rem;
        }}
        
        .games-header p {{
            font-size: 1.3rem;
            color: rgba(255,255,255,0.9);
            margin-bottom: 2rem;
        }}
        
        .games-count {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            border-radius: var(--border-radius-lg);
            color: white;
            font-weight: 600;
            display: inline-block;
        }}
        
        .card {{
            position: relative;
            border-radius: var(--border-radius-lg);
            overflow: hidden;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all var(--transition-normal);
            cursor: pointer;
        }}
        
        .card:hover {{
            transform: translateY(-10px);
            box-shadow: var(--shadow-lg);
        }}
        
        .card-thumbnail {{
            width: 100%;
            height: 220px;
            object-fit: cover;
            transition: opacity 0.3s ease;
            opacity: 0;
        }}
        
        .card-thumbnail[style*="opacity: 1"] {{
            opacity: 1;
        }}
        
        .image-placeholder {{
            width: 100%;
            height: 220px;
            background: linear-gradient(45deg, #333, #555);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.9rem;
        }}
        
        .card-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.9));
            padding: 2rem 1.5rem 1.5rem;
            transform: translateY(100%);
            transition: transform var(--transition-normal);
        }}
        
        .card:hover .card-overlay {{
            transform: translateY(0);
        }}
        
        .card-title {{
            color: white;
            font-weight: 700;
            margin-bottom: 0.75rem;
            font-size: 1.1rem;
        }}
        
        .card-cta {{
            background: var(--accent-color);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: var(--border-radius-md);
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all var(--transition-fast);
        }}
        
        .card-cta:hover {{
            background: color-mix(in srgb, var(--accent-color) 80%, white 20%);
            transform: scale(1.05);
        }}
        
        /* Footer Styles */
        .footer {{
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(20px);
            border-top: 1px solid rgba(255,255,255,0.1);
            padding: 3rem 2rem 2rem;
            margin-top: 4rem;
        }}
        
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}
        
        .footer-link {{
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            transition: color var(--transition-fast);
        }}
        
        .footer-link:hover {{
            color: var(--accent-color);
        }}
        
        .footer-bottom {{
            color: rgba(255,255,255,0.6);
            font-size: 0.9rem;
        }}
        
        .footer-bottom p {{
            margin: 0.5rem 0;
        }}
        
{framework_specific_styles}"""
    
    def _generate_animation_styles(self) -> str:
        """Generate animation styles"""
        return f"""        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes scaleIn {{
            from {{ opacity: 0; transform: scale(0.8); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
        
        .{self.class_prefix}-fade-in {{
            animation: fadeIn 0.6s ease-out;
        }}
        
        .{self.class_prefix}-scale-in {{
            animation: scaleIn 0.4s ease-out;
        }}"""
    
    def _generate_responsive_styles(self) -> str:
        """Generate responsive styles"""
        return f"""        /* Game Detail Styles */
        .{self.class_prefix}-game-container {{
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .{self.class_prefix}-game-title {{
            font-size: 2.5rem;
            font-weight: 900;
            color: white;
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .{self.class_prefix}-game-iframe-container {{
            position: relative;
            background: rgba(255,255,255,0.05);
            border-radius: var(--border-radius-lg);
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .{self.class_prefix}-game-iframe {{
            width: 100%;
            height: 600px;
            border: none;
            display: block;
        }}
        
        .{self.class_prefix}-game-loading {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--background-color);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            z-index: 10;
        }}
        
        .{self.class_prefix}-game-loading-spinner {{
            width: 40px;
            height: 40px;
            border: 3px solid rgba(255,255,255,0.2);
            border-top: 3px solid var(--accent-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .{self.class_prefix}-fullscreen-btn {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(0,0,0,0.7);
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: var(--border-radius-md);
            cursor: pointer;
            z-index: 20;
            transition: all var(--transition-fast);
        }}
        
        .{self.class_prefix}-fullscreen-btn:hover {{
            background: var(--accent-color);
            transform: scale(1.1);
        }}
        
        .{self.class_prefix}-breadcrumb {{
            padding: 1rem 2rem;
            margin-bottom: 2rem;
            color: rgba(255,255,255,0.8);
        }}
        
        .{self.class_prefix}-breadcrumb a {{
            color: var(--accent-color);
            text-decoration: none;
        }}
        
        .{self.class_prefix}-breadcrumb-separator {{
            margin: 0 0.5rem;
            color: rgba(255,255,255,0.5);
        }}
        
        .{self.class_prefix}-related-games {{
            margin-top: 4rem;
            padding: 2rem;
        }}
        
        .{self.class_prefix}-related-games h2 {{
            color: white;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 2rem;
            text-align: center;
        }}

        @media (max-width: 768px) {{
            .{self.class_prefix}-hero-title {{
                font-size: 2rem;
            }}
            
            .{self.class_prefix}-cards-slider {{
                grid-template-columns: 1fr;
            }}
            
            .{self.class_prefix}-games-grid {{
                grid-template-columns: 1fr;
                gap: 1rem;
                padding: 1rem;
            }}
            
            .{self.class_prefix}-mobile-sidebar-toggle {{
                display: block;
            }}
            
            .{self.class_prefix}-game-iframe {{
                height: 400px;
            }}
            
            .{self.class_prefix}-game-title {{
                font-size: 2rem;
            }}
            
            .{self.class_prefix}-game-container {{
                padding: 1rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            .{self.class_prefix}-hero {{
                min-height: 50vh;
                padding: 2rem 1rem;
            }}
            
            .{self.class_prefix}-btn-large {{
                padding: 1rem 2rem;
                font-size: 1rem;
            }}
            
            .{self.class_prefix}-games-grid {{
                padding: 0.5rem;
            }}
            
            .{self.class_prefix}-game-iframe {{
                height: 300px;
            }}
        }}"""
    
    def _generate_footer(self, content_data: Dict[str, Any]) -> str:
        """Generate footer section with anti-fingerprinting compatible classes"""
        footer_data = content_data.get('footer', {})
        
        return f"""    <footer class="footer">
        <div class="footer-content">
            <div class="footer-links">
                <a href="/terms.html" class="footer-link">Terms & Conditions</a>
                <a href="/privacy.html" class="footer-link">Privacy Policy</a>
                <a href="/responsible.html" class="footer-link">Responsible Gaming</a>
            </div>
            <div class="footer-bottom">
                <p><strong>Disclaimer:</strong> This is a social casino for entertainment purposes only.</p>
                <p>&copy; 2024 {content_data.get('site_name', 'Casino')}. All rights reserved.</p>
            </div>
        </div>
    </footer>"""
    
    # Placeholder methods for additional components
    def _generate_games_header(self, content_data: Dict[str, Any]) -> str:
        """Generate games page header with anti-fingerprinting compatible classes"""
        return f"""        <section class="games-header">
            <h1>All Games</h1>
            <p>Explore our complete collection of exciting games</p>
            <div class="games-count">{content_data.get('total_games', 0)} Games Available</div>
        </section>"""
    
    def _generate_games_grid(self, content_data: Dict[str, Any]) -> str:
        """Generate games grid section with anti-fingerprinting compatible classes"""
        all_games = content_data.get('all_games', [])
        game_cards = ''.join(self._generate_game_card(game) for game in all_games)
        
        return f"""        <section class="games-section">
            <div class="games-grid">
{game_cards}
            </div>
        </section>"""
    
    def _generate_breadcrumb(self, content_data: Dict[str, Any]) -> str:
        """Generate breadcrumb navigation with anti-fingerprinting compatible classes"""
        return f"""        <nav class="breadcrumb">
            <a href="/">Home</a> 
            <span class="breadcrumb-separator">/</span> 
            <a href="/games.html">Games</a>
            <span class="breadcrumb-separator">/</span> 
            <span>{content_data.get('game', {}).get('title', 'Game')}</span>
        </nav>"""
    
    def _generate_game_container(self, content_data: Dict[str, Any]) -> str:
        """Generate game detail container with anti-fingerprinting compatible classes"""
        game_data = content_data.get('game', {})
        
        return f"""        <section class="game-container">
            <div class="game-wrapper">
                <h1 class="game-title">{game_data.get('title', 'Game')}</h1>
                <div class="game-iframe-container">
                    <div class="game-loading" id="gameLoading">
                        <div class="game-loading-spinner"></div>
                        <p>Loading game...</p>
                    </div>
                    <iframe 
                        id="gameIframe"
                        class="game-iframe"
                        src="{game_data.get('iframe_url', 'about:blank')}" 
                        title="{game_data.get('title', 'Game')}"
                        width="100%" 
                        height="600"
                        frameborder="0"
                        allowfullscreen
                        onload="hideLoading()"
                        onerror="showError()">
                    </iframe>
                    <button class="fullscreen-btn" onclick="toggleFullscreen()" aria-label="Toggle fullscreen">
                        <i class="fas fa-expand"></i>
                    </button>
                </div>
            </div>
        </section>"""
    
    def _generate_related_games(self, content_data: Dict[str, Any]) -> str:
        """Generate related games section with anti-fingerprinting compatible classes"""
        return f"""        <section class="related-games">
            <h2>Similar Games</h2>
            <div class="games-grid">
                <!-- Related games would be populated here -->
            </div>
        </section>"""
    
    # Additional placeholder methods for other card styles and hero styles
    
    def _generate_top_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate top navigation HTML"""
        skip_link = """    <a href="#main-content" class="skip-link" tabindex="1">Skip to main content</a>"""
        
        nav_html = f"""{skip_link}
    <nav class="top-nav" role="navigation" aria-label="Main navigation">
        <div class="nav-brand">
            <h1>{site_name}</h1>
        </div>
        <div class="nav-menu" role="menubar">"""
        
        for i, (name, url, icon) in enumerate(nav_items):
            active_class = " active" if name == "Home" else ""
            is_current = 'aria-current="page"' if name == "Home" else ''
            nav_html += f"""
            <a href="{url}" 
               class="nav-item{active_class}" 
               role="menuitem" 
               {is_current}>
                <i class="{icon}" aria-hidden="true"></i> {name}
            </a>"""
        
        nav_html += """
        </div>
    </nav>"""
        return nav_html
    
    def _generate_hamburger_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate hamburger navigation HTML"""
        skip_link = """    <a href="#main-content" class="skip-link" tabindex="1">Skip to main content</a>"""
        
        nav_html = f"""{skip_link}
    <nav class="hamburger-nav" role="navigation" aria-label="Main navigation">
        <div class="nav-brand">
            <h1>{site_name}</h1>
        </div>
        <button class="hamburger-toggle" 
                onclick="toggleHamburgerMenu()" 
                aria-label="Toggle navigation menu"
                aria-expanded="false">
            <i class="fas fa-bars" aria-hidden="true"></i>
        </button>
    </nav>
    <div class="nav-menu" role="menubar">"""
        
        for i, (name, url, icon) in enumerate(nav_items):
            active_class = " active" if name == "Home" else ""
            is_current = 'aria-current="page"' if name == "Home" else ''
            nav_html += f"""
        <a href="{url}" 
           class="nav-item{active_class}" 
           role="menuitem" 
           {is_current}>
            <i class="{icon}" aria-hidden="true"></i> {name}
        </a>"""
        
        nav_html += """
    </div>"""
        return nav_html
    
    def _generate_bottom_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate bottom navigation HTML"""
        skip_link = """    <a href="#main-content" class="skip-link" tabindex="1">Skip to main content</a>"""
        
        nav_html = f"""{skip_link}
    <nav class="bottom-nav" role="navigation" aria-label="Main navigation">"""
        
        for i, (name, url, icon) in enumerate(nav_items):
            active_class = " active" if name == "Home" else ""
            is_current = 'aria-current="page"' if name == "Home" else ''
            nav_html += f"""
        <a href="{url}" 
           class="nav-item{active_class}" 
           role="menuitem" 
           {is_current}>
            <i class="{icon}" aria-hidden="true"></i>
            <span>{name}</span>
        </a>"""
        
        nav_html += """
    </nav>"""
        return nav_html
    
    def _generate_floating_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate floating action navigation HTML"""
        skip_link = """    <a href="#main-content" class="skip-link" tabindex="1">Skip to main content</a>"""
        
        nav_html = f"""{skip_link}
    <nav class="floating-nav" role="navigation" aria-label="Main navigation">
        <button class="fab-main" 
                onclick="toggleFabMenu()" 
                aria-label="Toggle navigation menu"
                aria-expanded="false">
            <i class="fas fa-bars" aria-hidden="true"></i>
        </button>
        <div class="fab-menu" role="menubar">"""
        
        for i, (name, url, icon) in enumerate(nav_items):
            nav_html += f"""
            <a href="{url}" 
               class="fab-item" 
               role="menuitem" 
               aria-label="{name}">
                <i class="{icon}" aria-hidden="true"></i>
            </a>"""
        
        nav_html += """
        </div>
    </nav>"""
        return nav_html
    
    def _generate_tab_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate tab bar navigation HTML"""
        skip_link = """    <a href="#main-content" class="skip-link" tabindex="1">Skip to main content</a>"""
        
        nav_html = f"""{skip_link}
    <nav class="tab-nav" role="navigation" aria-label="Main navigation">"""
        
        for i, (name, url, icon) in enumerate(nav_items):
            active_class = " active" if name == "Home" else ""
            is_current = 'aria-current="page"' if name == "Home" else ''
            nav_html += f"""
        <a href="{url}" 
           class="tab-item{active_class}" 
           role="menuitem" 
           {is_current}>
            {name}
        </a>"""
        
        nav_html += """
    </nav>"""
        return nav_html
    
    def _get_framework_specific_styles(self) -> str:
        """Generate framework-specific override styles with anti-fingerprinting compatible classes"""
        if self.config.framework == Framework.TAILWIND:
            return f"""        /* Tailwind CSS specific overrides */
        .main-wrapper {{
            @apply ml-0 lg:ml-72;
        }}
        
        .sidebar {{
            @apply fixed top-0 left-0 w-72 h-screen bg-black bg-opacity-90 backdrop-blur-xl border-r border-white border-opacity-10 z-50 transition-transform duration-300;
        }}
        
        .games-grid {{
            @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 p-8;
        }}
        
        .hero {{
            @apply min-h-screen flex items-center justify-center text-center relative;
        }}
        
        .btn {{
            @apply inline-flex items-center gap-2 px-8 py-4 border-0 rounded-xl no-underline font-semibold transition-all duration-300 cursor-pointer;
        }}
        
        .btn-primary {{
            @apply bg-casino-accent text-white;
        }}
        
        .btn-primary:hover {{
            @apply -translate-y-1 shadow-2xl;
        }}
        
        .card {{
            @apply relative rounded-2xl overflow-hidden bg-white bg-opacity-5 backdrop-blur-xl border border-white border-opacity-10 transition-all duration-300 cursor-pointer;
        }}
        
        .card:hover {{
            @apply -translate-y-3 shadow-2xl;
        }}"""
        
        elif self.config.framework == Framework.BOOTSTRAP:
            return f"""        /* Bootstrap specific overrides */
        .games-grid {{
            display: grid !important;
        }}
        
        @media (min-width: 576px) {{
            .games-grid {{
                grid-template-columns: repeat(2, 1fr) !important;
            }}
        }}
        
        @media (min-width: 768px) {{
            .games-grid {{
                grid-template-columns: repeat(3, 1fr) !important;
            }}
        }}
        
        @media (min-width: 1200px) {{
            .games-grid {{
                grid-template-columns: repeat(4, 1fr) !important;
            }}
        }}"""
        
        elif self.config.framework == Framework.BULMA:
            return f"""        /* Bulma specific overrides */
        .games-grid {{
            display: grid !important;
        }}
        
        @media screen and (min-width: 769px) {{
            .games-grid {{
                grid-template-columns: repeat(3, 1fr) !important;
            }}
        }}
        
        @media screen and (min-width: 1024px) {{
            .games-grid {{
                grid-template-columns: repeat(4, 1fr) !important;
            }}
        }}"""
        
        else:
            return "        /* Vanilla CSS - no framework overrides needed */"