import os
import json
import math
import random
import string
from pathlib import Path
from colorama import Fore, Style

def create_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def print_colored(text, color=Fore.WHITE):
    """Print colored text"""
    print(f"{color}{text}{Style.RESET_ALL}")

def get_user_input(prompt):
    """Get user input with colored prompt"""
    return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}")

def generate_random_string(length=8):
    """Generate random string of specified length"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def save_json(data, filepath):
    """Save data as JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath):
    """Load data from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def sanitize_filename(filename):
    """Sanitize filename for safe file creation"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def slugify(text):
    """Convert text to URL-friendly slug"""
    import re
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def get_file_extension(deployment_type):
    """Get file extension based on deployment type"""
    return ".php" if deployment_type == "traffic_armor" else ".html"

def create_breadcrumb_nav(current_page, game_name=None):
    """Create breadcrumb navigation"""
    breadcrumbs = []
    
    if current_page == "home":
        breadcrumbs = [{"text": "Home", "url": "#", "active": True}]
    elif current_page == "games":
        breadcrumbs = [
            {"text": "Home", "url": "index.html", "active": False},
            {"text": "Games", "url": "#", "active": True}
        ]
    elif current_page == "game" and game_name:
        breadcrumbs = [
            {"text": "Home", "url": "index.html", "active": False},
            {"text": "Games", "url": "games.html", "active": False},
            {"text": game_name, "url": "#", "active": True}
        ]
    
    return breadcrumbs