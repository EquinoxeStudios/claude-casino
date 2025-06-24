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
        
        # Generate unique build files
        self.generate_build_files(output_dir)
        
        print_colored("✅ Anti-fingerprinting applied successfully", Fore.GREEN)
    
    def generate_unique_mappings(self):
        """Generate unique mappings for classes, IDs, and functions"""
        
        # Common CSS classes to randomize
        common_classes = [
            'container', 'header', 'footer', 'nav', 'menu', 'content', 'sidebar',
            'main', 'section', 'article', 'card', 'button', 'btn', 'link',
            'game-card', 'game-grid', 'hero', 'features', 'about', 'contact'
        ]
        
        # Common IDs to randomize
        common_ids = [
            'header', 'footer', 'nav', 'menu', 'content', 'main', 'sidebar',
            'hero', 'games', 'about', 'contact', 'search', 'filter'
        ]
        
        # Common JavaScript functions to randomize
        common_functions = [
            'init', 'setup', 'handleClick', 'showGame', 'filterGames',
            'toggleMenu', 'scrollToTop', 'loadGames', 'searchGames'
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
                
                # Replace class names
                for original, unique in self.class_mapping.items():
                    content = re.sub(rf'class="([^"]*\b)?{re.escape(original)}(\b[^"]*)?', 
                                   lambda m: f'class="{m.group(1) or ""}{unique}{m.group(2) or ""}"', content)
                
                # Replace IDs
                for original, unique in self.id_mapping.items():
                    content = re.sub(rf'id="{re.escape(original)}"', f'id="{unique}"', content)
                    content = re.sub(rf'href="#{re.escape(original)}"', f'href="#{unique}"', content)
                
                # Add random comments
                content = self.add_random_html_comments(content)
                
                # Add invisible unicode characters
                content = self.add_invisible_characters(content)
                
                # Vary DOM structure slightly
                content = self.vary_dom_structure(content)
                
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
                    content = re.sub(rf'\.{re.escape(original)}(\b)', f'.{unique}\\1', content)
                
                # Replace ID selectors
                for original, unique in self.id_mapping.items():
                    content = re.sub(rf'#{re.escape(original)}(\b)', f'#{unique}\\1', content)
                
                # Add random CSS comments
                content = self.add_random_css_comments(content)
                
                # Randomize CSS property order
                content = self.randomize_css_properties(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print_colored(f"❌ Error processing {file_path}: {e}", Fore.RED)
    
    def process_js_files(self, output_dir):
        """Process JavaScript files to randomize function names"""
        js_files = list(Path(output_dir).rglob("*.js"))
        
        for file_path in js_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace function names
                for original, unique in self.function_mapping.items():
                    content = re.sub(rf'function\s+{re.escape(original)}(\b)', f'function {unique}\\1', content)
                    content = re.sub(rf'{re.escape(original)}\s*=\s*function', f'{unique} = function', content)
                    content = re.sub(rf'{re.escape(original)}\s*\(', f'{unique}(', content)
                
                # Add random JavaScript comments
                content = self.add_random_js_comments(content)
                
                # Add random variable declarations
                content = self.add_random_variables(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print_colored(f"❌ Error processing {file_path}: {e}", Fore.RED)
    
    def add_random_html_comments(self, content):
        """Add random HTML comments throughout the content"""
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
        
        # Add random comments at various positions
        lines = content.split('\n')
        for i in range(0, len(lines), random.randint(10, 25)):
            if i < len(lines):
                lines.insert(i, f"    {random.choice(comments)}")
        
        return '\n'.join(lines)
    
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
        """Add invisible Unicode characters to content"""
        invisible_chars = ['\\u200B', '\\u200C', '\\u200D', '\\u2060']
        
        # Add invisible characters at random positions in text content
        lines = content.split('\n')
        for i in range(len(lines)):
            if random.random() < 0.1:  # 10% chance per line
                char = random.choice(invisible_chars)
                lines[i] = lines[i] + char
        
        return '\n'.join(lines)
    
    def vary_dom_structure(self, content):
        """Slightly vary DOM structure"""
        # Add random empty divs
        if random.random() < 0.3:
            content = content.replace('<body>', '<body>\\n<div class="layout-helper"></div>')
        
        # Add random data attributes
        content = re.sub(r'<div class="([^"]*)"', 
                        lambda m: f'<div class="{m.group(1)}" data-v="{generate_random_string(6)}"', 
                        content)
        
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
            
            return f"{selector} {{\\n    {';\\n    '.join(prop_lines)};\\n}}"
        
        # Match CSS rules and randomize properties
        pattern = r'([^{]+)\\s*{\\s*([^}]+)\\s*}'
        content = re.sub(pattern, randomize_rule, content)
        
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
        var_block = "\\n".join(random_vars) + "\\n\\n"
        content = var_block + content
        
        return content
    
    def add_random_elements(self, output_dir):
        """Add random elements like meta tags, hidden divs, and other obfuscation"""
        html_files = list(Path(output_dir).rglob("*.html")) + list(Path(output_dir).rglob("*.php"))
        
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add random meta tags
                random_meta = []
                meta_names = ['generator', 'author', 'copyright', 'rating', 'distribution']
                for name in random.sample(meta_names, random.randint(2, 4)):
                    value = generate_random_string(random.randint(8, 16))
                    random_meta.append(f'<meta name="{name}" content="{value}">')
                
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