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
<html{html_attrs}>
<head>
{meta_tags}
{head_section}
</head>
<body{self._generate_body_attributes()}>
    <!-- Randomized comment: {self._generate_random_comment()} -->
    {navigation}
    
    <main class="main-wrapper" id="mainWrapper">
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
            return '''    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'casino-primary': '#1a1a2e',
                        'casino-accent': '#7c77c6',
                        'casino-background': '#0f0f1e',
                        'casino-surface': '#1e1e2e'
                    },
                    fontFamily: {
                        'casino': ['Inter', 'system-ui', 'sans-serif']
                    }
                }
            }
        }
    </script>'''
        elif self.config.framework == Framework.BOOTSTRAP:
            return '    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">'
        elif self.config.framework == Framework.BULMA:
            return '    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">'
        else:
            return '    <!-- Vanilla CSS Framework -->'
    
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
        """Generate sidebar navigation with anti-fingerprinting compatible class names"""
        nav_html = f"""    <!-- Navigation: Anti-fingerprinting compatible -->
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="logo">{site_name}</div>
        </div>
        <div class="sidebar-nav">"""
        
        for name, url, icon in nav_items:
            active_class = " active" if name == "Home" else ""
            nav_html += f"""
            <a href="{url}" class="nav-item{active_class}">
                <i class="{icon}"></i> <span>{name}</span>
            </a>"""
        
        nav_html += f"""
        </div>
        <button class="sidebar-toggle" onclick="toggleSidebar()" aria-label="Toggle sidebar">
            <i class="fas fa-chevron-left"></i>
        </button>
    </nav>
    
    <button class="mobile-sidebar-toggle" onclick="toggleMobileSidebar()" id="mobileSidebarToggle" aria-label="Open menu">
        <i class="fas fa-bars"></i>
    </button>
    
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="closeMobileSidebar()"></div>"""
        
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
    
    def _generate_content_sections(self, content_data: Dict[str, Any]) -> str:
        """Generate content sections with anti-fingerprinting compatible classes"""
        sections = ""
        content_sections = content_data.get('content_sections', [])
        
        for i, section in enumerate(content_sections):
            section_html = f"""        
        <section class="content-section">
            <div class="section-header">
                <h2 class="section-title">{section.get('title', f'Section {i+1}')}</h2>
                <p class="section-subtitle">{section.get('subtitle', '')}</p>
            </div>
            <div class="cards-container">
                <div class="cards-slider" id="section{i}Slider">"""
            
            for item in section.get('items', []):
                card_html = self._generate_game_card(item)
                section_html += f"""
                    {card_html}"""
            
            section_html += f"""
                </div>
            </div>
        </section>"""
            
            sections += section_html
        
        return sections
    
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
    
    def _generate_base_styles(self) -> str:
        """Generate base CSS styles with anti-fingerprinting compatible classes"""
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
        else:
            return "        /* Alternative navigation styles would go here */"
    
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
        games_html = f"""        <section class="games-section">
            <div class="games-grid">"""
        
        for game in content_data.get('all_games', []):
            games_html += self._generate_game_card(game)
        
        games_html += """            </div>
        </section>"""
        
        return games_html
    
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
    def _generate_flip_card(self, item: Dict[str, Any]) -> str:
        """Generate flip card style"""
        return self._generate_hover_overlay_card(item)  # Simplified for now
    
    def _generate_slide_up_card(self, item: Dict[str, Any]) -> str:
        """Generate slide up card style"""
        return self._generate_hover_overlay_card(item)  # Simplified for now
    
    def _generate_glassmorphism_card(self, item: Dict[str, Any]) -> str:
        """Generate glassmorphism card style"""
        return self._generate_hover_overlay_card(item)  # Simplified for now
    
    def _generate_neumorphism_card(self, item: Dict[str, Any]) -> str:
        """Generate neumorphism card style"""
        return self._generate_hover_overlay_card(item)  # Simplified for now
    
    def _generate_gradient_border_card(self, item: Dict[str, Any]) -> str:
        """Generate gradient border card style"""
        return self._generate_hover_overlay_card(item)  # Simplified for now
    
    def _generate_zoom_hover_card(self, item: Dict[str, Any]) -> str:
        """Generate zoom hover card style"""
        return self._generate_hover_overlay_card(item)  # Simplified for now
    
    def _generate_split_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate split hero style"""
        return self._generate_fullscreen_hero(hero_data)  # Simplified for now
    
    def _generate_video_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate video background hero"""
        return self._generate_fullscreen_hero(hero_data)  # Simplified for now
    
    def _generate_gradient_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate animated gradient hero"""
        return self._generate_fullscreen_hero(hero_data)  # Simplified for now
    
    def _generate_particles_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate particles.js hero"""
        return self._generate_fullscreen_hero(hero_data)  # Simplified for now
    
    def _generate_carousel_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate carousel hero"""
        return self._generate_fullscreen_hero(hero_data)  # Simplified for now
    
    def _generate_minimalist_hero(self, hero_data: Dict[str, Any]) -> str:
        """Generate minimalist hero"""
        return self._generate_fullscreen_hero(hero_data)  # Simplified for now
    
    def _generate_top_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate top navigation"""
        return self._generate_sidebar_navigation(site_name, nav_items)  # Simplified for now
    
    def _generate_hamburger_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate hamburger navigation"""
        return self._generate_sidebar_navigation(site_name, nav_items)  # Simplified for now
    
    def _generate_bottom_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate bottom navigation"""
        return self._generate_sidebar_navigation(site_name, nav_items)  # Simplified for now
    
    def _generate_floating_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate floating action navigation"""
        return self._generate_sidebar_navigation(site_name, nav_items)  # Simplified for now
    
    def _generate_tab_navigation(self, site_name: str, nav_items: List[Tuple[str, str, str]]) -> str:
        """Generate tab bar navigation"""
        return self._generate_sidebar_navigation(site_name, nav_items)  # Simplified for now
    
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