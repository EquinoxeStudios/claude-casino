#!/usr/bin/env python3
"""
Complete Dynamic Casino Website Generator
Generates fully-functional social casino websites with AI-powered content and real games.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from colorama import init, Fore, Style

from ai_content_generator import AIContentGenerator
from game_manager import GameManager
from website_builder import WebsiteBuilder
from unique_generator import UniqueGenerator
from utils import create_directory, get_user_input, print_colored

init(autoreset=True)

# Set UTF-8 encoding for Windows
if sys.platform.startswith('win'):
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

class CasinoWebsiteGenerator:
    def __init__(self):
        self.ai_generator = AIContentGenerator()
        self.game_manager = GameManager()
        self.website_builder = WebsiteBuilder()
        self.unique_generator = UniqueGenerator()
        
    def display_banner(self):
        """Display application banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                  CASINO WEBSITE GENERATOR v1.0                      ║
║             Generate Complete Social Casino Websites                ║
║                    Powered by AI & Real Games                       ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        print_colored(banner, Fore.CYAN)
    
    async def generate_website(self, domain_name, deployment_type="noip"):
        """Main website generation workflow"""
        try:
            print_colored(f"\n🎰 Starting website generation for: {domain_name}", Fore.GREEN)
            
            # Step 1: Generate theme concepts
            print_colored("🎨 Generating theme concepts...", Fore.YELLOW)
            themes = await self.ai_generator.generate_theme_concepts(domain_name)
            
            # Step 2: Let user choose theme
            chosen_theme = self.select_theme(themes)
            print_colored(f"✅ Selected theme: {chosen_theme['name']}", Fore.GREEN)
            
            # Step 3: Generate design system
            print_colored("🎨 Creating design system...", Fore.YELLOW)
            design_system = await self.ai_generator.generate_design_system(chosen_theme)
            
            # Step 4: Generate images
            print_colored("🖼️ Generating hero image and favicon...", Fore.YELLOW)
            images = await self.ai_generator.generate_images(chosen_theme)
            
            # Step 5: Fetch and process games
            print_colored("🎮 Fetching casino games...", Fore.YELLOW)
            games = await self.game_manager.fetch_games(domain_name)
            
            # Step 6: Generate all content
            print_colored("📝 Generating website content...", Fore.YELLOW)
            content = await self.ai_generator.generate_all_content(domain_name, chosen_theme, games)
            
            # Step 7: Build website
            print_colored("🏗️ Building website...", Fore.YELLOW)
            output_dir = f"output/{domain_name.replace('.', '_')}"
            await self.website_builder.build_website(
                output_dir, content, design_system, images, games, deployment_type
            )
            
            # Step 8: Apply uniqueness features
            print_colored("🔒 Applying anti-fingerprinting...", Fore.YELLOW)
            self.unique_generator.apply_uniqueness(output_dir)
            
            print_colored(f"\n✅ Website generated successfully!", Fore.GREEN)
            print_colored(f"📁 Output directory: {output_dir}", Fore.CYAN)
            
        except Exception as e:
            print_colored(f"❌ Error generating website: {str(e)}", Fore.RED)
            raise
    
    def select_theme(self, themes):
        """Let user select from generated themes"""
        print_colored("\n🎨 Choose a theme:", Fore.CYAN)
        for i, theme in enumerate(themes, 1):
            print(f"{i}. {theme['name']}")
            print(f"   {theme['description']}")
            print()
        
        while True:
            try:
                choice = int(input("Enter theme number (1-3): "))
                if 1 <= choice <= len(themes):
                    return themes[choice - 1]
                else:
                    print_colored("Invalid choice. Please enter 1, 2, or 3.", Fore.RED)
            except ValueError:
                print_colored("Please enter a valid number.", Fore.RED)

async def main():
    generator = CasinoWebsiteGenerator()
    generator.display_banner()
    
    # Get domain name from user
    domain_name = get_user_input("Enter domain name (e.g., mycasino.com): ")
    
    # Get deployment type
    print("\nSelect deployment type:")
    print("1. Standard (.html extensions)")
    print("2. Traffic Armor (folder structure with index.php)")
    
    deployment_choice = get_user_input("Enter choice (1 or 2): ")
    deployment_type = "traffic_armor" if deployment_choice == "2" else "noip"
    
    # Generate website
    await generator.generate_website(domain_name, deployment_type)

if __name__ == "__main__":
    asyncio.run(main())