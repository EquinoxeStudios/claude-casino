import os
import re
import random
import string
from pathlib import Path
from utils import print_colored, generate_random_string
from colorama import Fore

class UniqueGenerator:
    def __init__(self):
        self.class_mapping = {}
        self.id_mapping = {}
        self.function_mapping = {}
        self.variable_mapping = {}
        
    def apply_uniqueness(self, output_dir):
        """Apply anti-fingerprinting measures to the generated website"""
        print_colored("🔒 Applying anti-fingerprinting measures...", Fore.YELLOW)
        
        # Generate unique mappings
        self.generate_unique_mappings()
        
        # Process HTML files
        self.process_html_files(output_dir)
        
        # Process CSS files
        self.process_css_files(output_dir)
        
        # Process JS files
        self.process_js_files(output_dir)
        
        # Add random comments and metadata
        self.add_random_elements(output_dir)
        
        # Vary CSS delivery method
        self.vary_css_delivery(output_dir)
        
        # Generate unique build files
        self.generate_build_files(output_dir)
        
        print_colored("✅ Anti-fingerprinting applied successfully", Fore.GREEN)
    
    def generate_unique_mappings(self):
        """Generate unique mappings for classes, IDs, and functions"""
        
        # Common CSS classes to randomize - must match those used in templates and CSS
        common_classes = [
            'sidebar', 'sidebar-header', 'sidebar-nav', 'sidebar-toggle', 'sidebar-overlay',
            'mobile-sidebar-toggle', 'main-wrapper', 'hero', 'hero-content', 'hero-buttons',
            'content-section', 'section-header', 'section-title', 'section-subtitle',
            'cards-container', 'cards-slider', 'card', 'card-thumbnail', 'card-overlay',
            'card-info', 'card-title', 'card-cta', 'slider-nav', 'slider-prev', 'slider-next',
            'slider-dots', 'dot', 'about-section', 'about-content', 'footer', 'footer-content',
            'footer-links', 'footer-link', 'footer-bottom', 'nav-item', 'logo', 'btn',
            'btn-primary', 'btn-large', 'games-header', 'games-count', 'games-section',
            'games-grid', 'game-card', 'game-thumbnail', 'game-overlay', 'game-info',
            'game-title', 'game-cta', 'page-header', 'about-block', 'content-wrapper'
        ]
        
        # Common IDs to randomize
        common_ids = [
            'sidebar', 'mainWrapper', 'mobileSidebarToggle', 'sidebarOverlay',
            'section0Slider', 'section1Slider', 'section0Dots', 'section1Dots',
            'gameLoading'
        ]
        
        # Common JavaScript functions to randomize
        common_functions = [
            'toggleSidebar', 'toggleMobileSidebar', 'closeMobileSidebar', 'slideCards',
            'handleImageError', 'handleImageLoad', 'trackGameClick', 'hideLoading',
            'showError', 'toggleFullscreen', 'initializeSliderDots'
        ]
        
        # Generate unique class names
        for cls in common_classes:
            self.class_mapping[cls] = f"c{generate_random_string(8)}"
        
        # Generate unique IDs
        for id_name in common_ids:
            self.id_mapping[id_name] = f"i{generate_random_string(8)}"
        
        # Generate unique function names
        for func in common_functions:
            self.function_mapping[func] = f"f{generate_random_string(8)}"
    
    def process_html_files(self, output_dir):
        """Process HTML files to randomize classes and IDs"""
        html_files = list(Path(output_dir).rglob("*.html")) + list(Path(output_dir).rglob("*.php"))
        
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace class names with proper spacing
                for original, unique in self.class_mapping.items():
                    # Replace whole class names with word boundaries
                    def replace_class_name(m):
                        full_class_attr = m.group(1)
                        # Split into individual classes, replace the target class, rejoin
                        classes = full_class_attr.split()
                        updated_classes = []
                        for cls in classes:
                            if cls == original:
                                updated_classes.append(unique)
                            else:
                                updated_classes.append(cls)
                        return f'class="{" ".join(updated_classes)}"'
                    
                    # Match the entire class attribute content
                    content = re.sub(rf'\bclass="([^"]*\b{re.escape(original)}\b[^"]*)"', 
                                   replace_class_name, content)
                
                # Replace IDs
                for original, unique in self.id_mapping.items():
                    content = re.sub(rf'id="{re.escape(original)}"', f'id="{unique}"', content)
                    content = re.sub(rf'href="#{re.escape(original)}"', f'href="#{unique}"', content)
                
                # Replace JavaScript function names in HTML attributes (onclick, etc.)
                for original, unique in self.function_mapping.items():
                    content = re.sub(rf'\b{re.escape(original)}\s*\(', f'{unique}(', content)
                
                # Process inline CSS within <style> tags
                content = self.process_inline_css(content)
                
                # Process inline JavaScript within <script> tags
                content = self.process_inline_js(content)
                
                # Add random comments
                content = self.add_random_html_comments(content)
                
                # Add invisible unicode characters
                content = self.add_invisible_characters(content)
                
                # Vary DOM structure slightly
                content = self.vary_dom_structure(content)
                
                # Add dynamic inline style variations
                content = self.add_dynamic_inline_styles(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print_colored(f"❌ Error processing {file_path}: {e}", Fore.RED)
    
    def process_css_files(self, output_dir):
        """Process CSS files to randomize selectors"""
        css_files = list(Path(output_dir).rglob("*.css"))
        
        for file_path in css_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace class selectors
                for original, unique in self.class_mapping.items():
                    # Match class selectors: .classname (with word boundary or special chars)
                    content = re.sub(rf'\.{re.escape(original)}(?=[\s\{{:,>+~#\.]|$)', f'.{unique}', content)
                
                # Replace ID selectors
                for original, unique in self.id_mapping.items():
                    # Match ID selectors: #idname (with word boundary or special chars)
                    content = re.sub(rf'#{re.escape(original)}(?=[\s\{{:,>+~#\.]|$)', f'#{unique}', content)
                
                # Add random CSS comments
                content = self.add_random_css_comments(content)
                
                # Randomize CSS property order
                content = self.randomize_css_properties(content)
                
                # Add font variations
                content = self.add_font_variations(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print_colored(f"❌ Error processing {file_path}: {e}", Fore.RED)
    
    def process_inline_css(self, content):
        """Process inline CSS within <style> tags to randomize selectors"""
        def process_style_block(match):
            css_content = match.group(1)
            
            # Replace class selectors
            for original, unique in self.class_mapping.items():
                # Match class selectors: .classname (with word boundary or special chars)
                css_content = re.sub(rf'\.{re.escape(original)}(?=[\s\{{:,>+~#\.]|$)', f'.{unique}', css_content)
            
            # Replace ID selectors
            for original, unique in self.id_mapping.items():
                # Match ID selectors: #idname (with word boundary or special chars)
                css_content = re.sub(rf'#{re.escape(original)}(?=[\s\{{:,>+~#\.]|$)', f'#{unique}', css_content)
            
            return f'<style>{css_content}</style>'
        
        # Process all <style> blocks
        content = re.sub(r'<style[^>]*>(.*?)</style>', process_style_block, content, flags=re.DOTALL)
        
        return content
    
    def process_inline_js(self, content):
        """Process inline JavaScript within <script> tags to randomize function names and IDs"""
        def process_script_block(match):
            # Check if this is an external script (has src attribute)
            full_tag = match.group(0)
            if 'src=' in full_tag:
                return full_tag  # Don't process external scripts
            
            js_content = match.group(1)
            
            # Replace function names in JavaScript
            for original, unique in self.function_mapping.items():
                # Function declarations: function functionName()
                js_content = re.sub(rf'\bfunction\s+{re.escape(original)}\b', f'function {unique}', js_content)
                # Function expressions: var functionName = function
                js_content = re.sub(rf'\b{re.escape(original)}\s*=\s*function', f'{unique} = function', js_content)
                # Function calls: functionName(
                js_content = re.sub(rf'\b{re.escape(original)}\s*\(', f'{unique}(', js_content)
            
            # Replace ID references in JavaScript
            for original, unique in self.id_mapping.items():
                # getElementById calls
                js_content = re.sub(rf'getElementById\s*\(\s*[\'\"]{re.escape(original)}[\'\"]\s*\)', 
                                  f'getElementById(\'{unique}\')', js_content)
                # querySelector calls with IDs
                js_content = re.sub(rf'querySelector\s*\(\s*[\'\"]\#{re.escape(original)}[\'\"]\s*\)', 
                                  f'querySelector(\'#{unique}\')', js_content)
                # querySelectorAll calls with IDs
                js_content = re.sub(rf'querySelectorAll\s*\(\s*[\'\"]\#{re.escape(original)}[\'\"]\s*\)', 
                                  f'querySelectorAll(\'#{unique}\')', js_content)
            
            # Replace class references in JavaScript
            for original, unique in self.class_mapping.items():
                # querySelector calls with classes
                js_content = re.sub(rf'querySelector\s*\(\s*[\'\""]\.{re.escape(original)}[\'\"]\s*\)', 
                                  f'querySelector(\'.{unique}\')', js_content)
                # querySelectorAll calls with classes
                js_content = re.sub(rf'querySelectorAll\s*\(\s*[\'\""]\.{re.escape(original)}[\'\"]\s*\)', 
                                  f'querySelectorAll(\'.{unique}\')', js_content)
                # getElementsByClassName calls
                js_content = re.sub(rf'getElementsByClassName\s*\(\s*[\'\"]{re.escape(original)}[\'\"]\s*\)', 
                                  f'getElementsByClassName(\'{unique}\')', js_content)
                # classList operations
                js_content = re.sub(rf'classList\.(add|remove|toggle|contains)\s*\(\s*[\'\"]{re.escape(original)}[\'\"]\s*\)', 
                                  rf'classList.\1(\'{unique}\')', js_content)
            
            return f'<script>{js_content}</script>'
        
        # Process all <script> blocks (but not external scripts)
        content = re.sub(r'<script([^>]*)>(.*?)</script>', process_script_block, content, flags=re.DOTALL)
        
        return content
    
    def process_js_files(self, output_dir):
        """Process JavaScript files to randomize function names"""
        js_files = list(Path(output_dir).rglob("*.js"))
        
        for file_path in js_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace function names in JavaScript
                for original, unique in self.function_mapping.items():
                    # Function declarations: function functionName()
                    content = re.sub(rf'\bfunction\s+{re.escape(original)}\b', f'function {unique}', content)
                    # Function expressions: var functionName = function
                    content = re.sub(rf'\b{re.escape(original)}\s*=\s*function', f'{unique} = function', content)
                    # Function calls: functionName(
                    content = re.sub(rf'\b{re.escape(original)}\s*\(', f'{unique}(', content)
                
                # Add random JavaScript comments
                content = self.add_random_js_comments(content)
                
                # Add random variable declarations
                content = self.add_random_variables(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print_colored(f"❌ Error processing {file_path}: {e}", Fore.RED)
    
    def add_random_html_comments(self, content):
        """Add random HTML comments throughout the content in safe locations"""
        comments = [
            "<!-- Generated content -->",
            "<!-- Dynamic section -->", 
            "<!-- Custom implementation -->",
            "<!-- Responsive design -->",
            "<!-- Optimized for mobile -->",
            "<!-- SEO friendly -->",
            "<!-- Accessibility compliant -->",
            "<!-- Modern standards -->"
        ]
        
        # Find safe locations to insert comments (avoid inside tags)
        lines = content.split('\n')
        safe_lines = []
        
        for i, line in enumerate(lines):
            safe_lines.append(line)
            
            # Only add comments after complete lines that are safe locations
            if (i % random.randint(15, 30) == 0 and 
                line.strip() and 
                (line.strip().endswith('</div>') or 
                 line.strip().endswith('</section>') or
                 line.strip().endswith('</article>') or
                 line.strip().endswith('</header>') or
                 line.strip().endswith('</footer>') or
                 line.strip().endswith('</nav>'))):
                
                # Add comment on next line with proper indentation
                indent = len(line) - len(line.lstrip())
                safe_lines.append(' ' * indent + random.choice(comments))
        
        return '\n'.join(safe_lines)
    
    def add_random_css_comments(self, content):
        """Add random CSS comments"""
        comments = [
            "/* Custom styling */",
            "/* Responsive breakpoint */",
            "/* Animation effects */",
            "/* Color scheme */",
            "/* Typography settings */",
            "/* Layout structure */",
            "/* Performance optimized */",
            "/* Cross-browser compatible */"
        ]
        
        # Add comments at random positions
        lines = content.split('\n')
        for i in range(0, len(lines), random.randint(15, 30)):
            if i < len(lines):
                lines.insert(i, f"{random.choice(comments)}")
        
        return '\n'.join(lines)
    
    def add_random_js_comments(self, content):
        """Add random JavaScript comments"""
        comments = [
            "// Enhanced functionality",
            "// Event handling",
            "// DOM manipulation",
            "// User interaction",
            "// Performance optimization",
            "// Cross-platform support",
            "// Modern JavaScript",
            "// Async operations"
        ]
        
        # Add comments at random positions
        lines = content.split('\n')
        for i in range(0, len(lines), random.randint(8, 20)):
            if i < len(lines):
                lines.insert(i, f"    {random.choice(comments)}")
        
        return '\n'.join(lines)
    
    def add_invisible_characters(self, content):
        """Add invisible Unicode characters to content (optional feature)"""
        # Disabled by default to avoid text rendering issues
        # Uncomment the code below if you want to enable invisible characters
        
        # invisible_chars = ['\u200B', '\u200C', '\u200D', '\u2060']  # Zero-width chars
        # lines = content.split('\n')
        # for i in range(len(lines)):
        #     if random.random() < 0.02:  # Very low chance
        #         char = random.choice(invisible_chars)
        #         # Only add to specific safe locations
        #         if '</title>' in lines[i] or '</h1>' in lines[i]:
        #             lines[i] = lines[i].replace('>', f'{char}>')
        # return '\n'.join(lines)
        
        # Return content unchanged (invisible chars disabled)
        return content
    
    def vary_dom_structure(self, content):
        """Advanced DOM structure variation for anti-fingerprinting"""
        
        # 1. Add random empty containers with varying depth
        if random.random() < 0.3:
            depth = random.randint(1, 3)
            nested_divs = ''.join(['<div class="layout-helper">'] * depth)
            nested_closing = ''.join(['</div>'] * depth)
            content = content.replace('<body>', f'<body>\n{nested_divs}{nested_closing}')
        
        # 2. Randomly use semantic vs generic tags (safer approach)
        # Only replace if we can ensure matching closing tags
        semantic_patterns = [
            ('content-section', 'article'),
            ('sidebar', 'aside'), 
            ('nav', 'nav'),
            ('header', 'header'),
            ('footer', 'footer')
        ]
        
        for class_pattern, tag_name in semantic_patterns:
            if random.random() < 0.3:  # 30% chance to use semantic tags
                # Only replace self-contained divs to avoid mismatched tags
                pattern = rf'<div class="([^"]*{class_pattern}[^"]*)"([^>]*)>(.*?)</div>'
                replacement = rf'<{tag_name} class="\1"\2>\3</{tag_name}>'
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # 3. Add random data attributes with varying formats
        data_attrs = [
            f'data-id="{generate_random_string(8)}"',
            f'data-component="{generate_random_string(6)}"',
            f'data-render="{random.randint(1000, 9999)}"',
            f'data-version="{random.randint(1, 99)}.{random.randint(0, 9)}"'
        ]
        
        content = re.sub(r'<div class="([^"]*)"', 
                        lambda m: f'<div class="{m.group(1)}" {random.choice(data_attrs)}', 
                        content)
        
        # 4. Add random wrapper elements
        if random.random() < 0.2:
            wrapper_tag = random.choice(['section', 'div', 'article'])
            content = content.replace('<main class="main-wrapper"', 
                                    f'<{wrapper_tag} class="container-wrap"><main class="main-wrapper"')
            content = content.replace('</main>', f'</main></{wrapper_tag}>')
        
        return content
    
    def randomize_css_properties(self, content):
        """Randomize order of CSS properties within rules"""
        def randomize_rule(match):
            selector = match.group(1)
            properties = match.group(2).strip()
            
            if not properties:
                return match.group(0)
            
            # Split properties and randomize order
            prop_lines = [line.strip() for line in properties.split(';') if line.strip()]
            random.shuffle(prop_lines)
            
            newline = '\n'
            prop_separator = f';{newline}    '
            return f"{selector} {{{newline}    {prop_separator.join(prop_lines)};{newline}}}"
        
        # Match CSS rules and randomize properties
        pattern = r'([^{]+)\s*{\s*([^}]+)\s*}'
        content = re.sub(pattern, randomize_rule, content)
        
        return content
    
    def add_font_variations(self, content):
        """Add font stack variations for anti-fingerprinting"""
        
        # Alternative web-safe font stacks
        font_variations = {
            'Arial': [
                'Arial, Helvetica, sans-serif',
                'Arial, "Helvetica Neue", sans-serif', 
                '"Segoe UI", Arial, sans-serif'
            ],
            'Helvetica': [
                'Helvetica, Arial, sans-serif',
                '"Helvetica Neue", Helvetica, sans-serif',
                'system-ui, Helvetica, sans-serif'
            ],
            'sans-serif': [
                'system-ui, -apple-system, sans-serif',
                '"Segoe UI", Roboto, sans-serif',
                'BlinkMacSystemFont, "Segoe UI", sans-serif'
            ]
        }
        
        # Apply font variations randomly
        for original_font, variations in font_variations.items():
            if original_font in content:
                replacement = random.choice(variations)
                content = content.replace(f'font-family: {original_font}', f'font-family: {replacement}')
                content = content.replace(f"font-family: '{original_font}'", f"font-family: {replacement}")
                content = content.replace(f'font-family: "{original_font}"', f"font-family: {replacement}")
        
        # Add subtle font-weight variations
        weight_variations = {
            'font-weight: 400': f'font-weight: {random.choice([400, 450, 500])}',
            'font-weight: 600': f'font-weight: {random.choice([600, 650, 700])}',
            'font-weight: 700': f'font-weight: {random.choice([700, 750, 800])}'
        }
        
        for original, variation in weight_variations.items():
            if random.random() < 0.3:  # 30% chance to apply variation
                content = content.replace(original, variation)
        
        return content
    
    def add_random_variables(self, content):
        """Add random unused variables to JavaScript"""
        random_vars = []
        for _ in range(random.randint(3, 8)):
            var_name = f"_{generate_random_string(6)}"
            var_value = random.choice([
                f'"{generate_random_string(10)}"',
                str(random.randint(1000, 9999)),
                'null',
                'undefined',
                '[]',
                '{}'
            ])
            random_vars.append(f"var {var_name} = {var_value};")
        
        # Add variables at the beginning of the file
        var_block = "\n".join(random_vars) + "\n\n"
        content = var_block + content
        
        return content
    
    def add_dynamic_inline_styles(self, content):
        """Add subtle inline style variations for anti-fingerprinting"""
        
        # Define micro-variations for common CSS properties
        padding_variations = [
            f"{random.randint(10, 15)}.{random.randint(1, 9)}px",
            f"{random.randint(8, 12)}px",
            f"0.{random.randint(6, 14)}rem"
        ]
        
        margin_variations = [
            f"{random.randint(5, 10)}.{random.randint(2, 8)}px",
            f"{random.randint(4, 8)}px auto",
            f"0 {random.randint(8, 16)}px"
        ]
        
        border_radius_variations = [
            f"{random.randint(6, 12)}px",
            f"{random.randint(4, 8)}.{random.randint(1, 5)}px",
            f"{random.randint(10, 20)}%"
        ]
        
        # Add inline styles to random elements
        style_additions = [
            f'style="padding: {random.choice(padding_variations)};"',
            f'style="margin: {random.choice(margin_variations)};"',
            f'style="border-radius: {random.choice(border_radius_variations)};"',
            f'style="opacity: 0.{random.randint(95, 99)};"',
            f'style="letter-spacing: {random.choice([0.1, 0.2, 0.3, -0.1])}px;"'
        ]
        
        # Apply random inline styles to card elements (only if no existing style)
        if random.random() < 0.3:
            content = re.sub(r'(<div class="[^"]*card[^"]*"(?![^>]*style=))', 
                           lambda m: f'{m.group(1)} {random.choice(style_additions)}', 
                           content, count=random.randint(1, 3))
        
        # Apply to button elements (only if no existing style)
        if random.random() < 0.4:
            content = re.sub(r'(<[^>]*class="[^"]*btn[^"]*"(?![^>]*style=))', 
                           lambda m: f'{m.group(1)} {random.choice(style_additions)}', 
                           content, count=random.randint(1, 2))
        
        return content
    
    def add_random_elements(self, output_dir):
        """Add random elements like meta tags, hidden divs, and other obfuscation"""
        html_files = list(Path(output_dir).rglob("*.html")) + list(Path(output_dir).rglob("*.php"))
        
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add random meta tags with variations
                random_meta = []
                meta_names = ['generator', 'author', 'copyright', 'rating', 'distribution', 'robots', 'theme-color']
                
                # Generate varied meta content
                for name in random.sample(meta_names, random.randint(3, 5)):
                    if name == 'robots':
                        value = random.choice(['index,follow', 'index,nofollow', 'noindex,follow'])
                    elif name == 'theme-color':
                        value = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                    else:
                        value = generate_random_string(random.randint(8, 16))
                    random_meta.append(f'<meta name="{name}" content="{value}">')
                
                # Vary title format if present
                title_variations = [
                    lambda site: f"{site} - Social Casino Games",
                    lambda site: f"Free Casino Games at {site}",
                    lambda site: f"{site} | Play Free Slots Online",
                    lambda site: f"Online Casino Games - {site}",
                    lambda site: f"{site}: Free Social Gaming"
                ]
                
                if '<title>' in content:
                    # Extract site name from existing title
                    title_match = re.search(r'<title>([^<]+)</title>', content)
                    if title_match:
                        current_title = title_match.group(1)
                        site_name = current_title.split(' - ')[0].split(' | ')[0].split(': ')[0]
                        new_title = random.choice(title_variations)(site_name)
                        content = re.sub(r'<title>[^<]+</title>', f'<title>{new_title}</title>', content)
                
                # Add varied meta description
                desc_templates = [
                    "Play free social casino games online. Entertainment only, no real money gambling.",
                    "Enjoy the best free casino games for entertainment. No deposits required.",
                    "Free social gaming experience with casino-style games. Play for fun!",
                    "Entertainment-focused casino games. No real money, just pure fun.",
                    "Social casino gaming platform. Free to play, entertainment only."
                ]
                random_meta.append(f'<meta name="description" content="{random.choice(desc_templates)}">')
                
                # Insert meta tags before closing head tag
                if '</head>' in content:
                    meta_block = '\n    ' + '\n    '.join(random_meta) + '\n'
                    content = content.replace('</head>', meta_block + '</head>')
                
                # Add random hidden divs
                hidden_divs = []
                for _ in range(random.randint(1, 3)):
                    div_id = generate_random_string(8)
                    hidden_divs.append(f'<div id="{div_id}" style="display:none;"></div>')
                
                # Insert hidden divs after body tag
                if '<body>' in content:
                    hidden_block = '\n' + '\n'.join(hidden_divs) + '\n'
                    content = content.replace('<body>', '<body>' + hidden_block)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print_colored(f"❌ Error adding random elements to {file_path}: {e}", Fore.RED)
    
    def vary_css_delivery(self, output_dir):
        """Vary CSS delivery method for anti-fingerprinting"""
        html_files = list(Path(output_dir).rglob("*.html")) + list(Path(output_dir).rglob("*.php"))
        
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 30% chance to inline critical CSS
                if random.random() < 0.3:
                    css_file = Path(output_dir) / "css" / "style.css"
                    if css_file.exists():
                        with open(css_file, 'r', encoding='utf-8') as css_f:
                            css_content = css_f.read()
                        
                        # Extract and inline critical CSS (first 50 rules)
                        critical_css = self.extract_critical_css(css_content)
                        
                        # Add inline style block
                        style_block = f'\n<style>\n{critical_css}\n</style>\n'
                        content = content.replace('</head>', style_block + '</head>')
                        
                        # Modify external stylesheet link to load non-critical CSS
                        content = content.replace(
                            '<link rel="stylesheet" href="css/style.css">',
                            '<link rel="stylesheet" href="css/style.css" media="print" onload="this.media=\'all\'; this.onload=null;">'
                        )
                
                # 20% chance to add CSS custom properties variation
                if random.random() < 0.2:
                    custom_props = self.generate_css_custom_properties()
                    style_block = f'\n<style>\n:root {{\n{custom_props}\n}}\n</style>\n'
                    content = content.replace('</head>', style_block + '</head>')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print_colored(f"❌ Error varying CSS delivery for {file_path}: {e}", Fore.RED)
    
    def extract_critical_css(self, css_content):
        """Extract critical CSS rules (basic selectors)"""
        lines = css_content.split('\n')
        critical_lines = []
        brace_count = 0
        rule_count = 0
        
        for line in lines:
            critical_lines.append(line)
            if '{' in line:
                brace_count += line.count('{')
            if '}' in line:
                brace_count -= line.count('}')
                if brace_count == 0:
                    rule_count += 1
                    if rule_count >= 50:  # Limit to first 50 rules
                        break
        
        return '\n'.join(critical_lines)
    
    def generate_css_custom_properties(self):
        """Generate unique CSS custom properties"""
        return f"""
    --unique-spacing: {random.randint(2, 8)}px;
    --unique-radius: {random.randint(4, 12)}px;
    --unique-opacity: 0.{random.randint(85, 95)};
    --unique-shadow: 0 {random.randint(2, 6)}px {random.randint(10, 20)}px rgba(0,0,0,0.{random.randint(1, 3)});
    --unique-transition: {random.choice(['0.2s', '0.3s', '0.4s'])} ease;
        """.strip()
    
    def generate_build_files(self, output_dir):
        """Generate unique build and meta files"""
        
        # Generate unique build ID
        build_id = generate_random_string(16)
        build_timestamp = str(random.randint(1600000000, 1700000000))
        
        # Create build.json
        build_info = {
            "build_id": build_id,
            "timestamp": build_timestamp,
            "version": f"{random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 99)}",
            "env": "production",
            "hash": generate_random_string(32)
        }
        
        with open(f"{output_dir}/build.json", 'w') as f:
            import json
            json.dump(build_info, f, indent=2)
        
        # Create .htaccess with unique rules
        htaccess_content = f"""# Build ID: {build_id}
RewriteEngine On

# Security headers
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"

# Cache control
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
</IfModule>

# Compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Custom error pages
ErrorDocument 404 /404.html
ErrorDocument 500 /500.html

# Random comment: {generate_random_string(20)}
"""
        
        with open(f"{output_dir}/.htaccess", 'w') as f:
            f.write(htaccess_content)
        
        # Create robots.txt with unique identifiers
        robots_content = f"""# Build: {build_id}
User-agent: *
Disallow: /admin/
Disallow: /private/
Disallow: /temp/
Allow: /

# Crawl-delay: {random.randint(1, 5)}
Sitemap: /sitemap.xml

# Generated: {build_timestamp}
"""
        
        with open(f"{output_dir}/robots.txt", 'w') as f:
            f.write(robots_content)
        
        # Create version.txt
        version_content = f"""Build ID: {build_id}
Version: {build_info['version']}
Timestamp: {build_timestamp}
Hash: {build_info['hash']}
Environment: production
Generator: CasinoGen v1.0
"""
        
        with open(f"{output_dir}/version.txt", 'w') as f:
            f.write(version_content)
        
        print_colored("✅ Build files generated with unique identifiers", Fore.GREEN)