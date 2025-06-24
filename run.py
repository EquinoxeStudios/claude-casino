#!/usr/bin/env python3
"""
Enhanced CLI runner for Casino Website Generator with improved interface
"""

import asyncio
import sys
import os
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Import main application
from main import CasinoWebsiteGenerator, print_colored

def display_welcome():
    """Display welcome screen with ASCII art"""
    welcome_art = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║    ░█████╗░░█████╗░░██████╗██╗███╗░░██╗░█████╗░  ░██████╗░███████╗███╗░░██╗    ║
║    ██╔══██╗██╔══██╗██╔════╝██║████╗░██║██╔══██╗  ██╔════╝░██╔════╝████╗░██║    ║
║    ██║░░╚═╝███████║╚█████╗░██║██╔██╗██║██║░░██║  ██║░░██╗░█████╗░░██╔██╗██║    ║
║    ██║░░██╗██╔══██║░╚═══██╗██║██║╚████║██║░░██║  ██║░░╚██╗██╔══╝░░██║╚████║    ║
║    ╚█████╔╝██║░░██║██████╔╝██║██║░╚███║╚█████╔╝  ╚██████╔╝███████╗██║░╚███║    ║
║    ░╚════╝░╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝░╚════╝░  ░╚═════╝░╚══════╝╚═╝░░╚══╝    ║
║                                                                      ║
║              🎰 COMPLETE DYNAMIC CASINO WEBSITE GENERATOR 🎰          ║
║                        Powered by AI & Real Games                   ║
║                              Version 1.0                            ║
╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(welcome_art)

def check_requirements():
    """Check if all requirements are met"""
    print_colored("🔍 Checking requirements...", Fore.YELLOW)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print_colored("❌ .env file not found!", Fore.RED)
        print_colored("Please run 'python setup.py' first or create .env file with your API keys", Fore.YELLOW)
        return False
    
    # Check if API keys are set
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    slots_token = os.getenv('SLOTSLAUNCH_API_TOKEN')
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print_colored("❌ OpenAI API key not configured!", Fore.RED)
        print_colored("Please add your OpenAI API key to the .env file", Fore.YELLOW)
        return False
    
    if not slots_token or slots_token == 'your_slotslaunch_token_here':
        print_colored("⚠️  SlotsLaunch API token not configured", Fore.YELLOW)
        print_colored("Using fallback demo games (add token for real games)", Fore.YELLOW)
    
    print_colored("✅ Requirements check passed!", Fore.GREEN)
    return True

def get_domain_input():
    """Get domain name with validation"""
    while True:
        domain = input(f"{Fore.CYAN}🌐 Enter domain name (e.g., mycasino.com): {Style.RESET_ALL}").strip()
        
        if not domain:
            print_colored("❌ Domain name cannot be empty", Fore.RED)
            continue
        
        if len(domain) < 3:
            print_colored("❌ Domain name too short", Fore.RED)
            continue
        
        # Basic domain validation
        if not domain.replace('.', '').replace('-', '').replace('_', '').isalnum():
            print_colored("❌ Invalid domain name format", Fore.RED)
            continue
        
        return domain

def get_deployment_type():
    """Get deployment type with validation"""
    print(f"\n{Fore.CYAN}📁 Select deployment type:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. {Fore.GREEN}Standard{Fore.WHITE} - Uses .html extensions (recommended for most users)")
    print(f"{Fore.WHITE}2. {Fore.BLUE}Traffic Armor{Fore.WHITE} - Uses folder structure with index.php files")
    
    while True:
        choice = input(f"{Fore.CYAN}Enter choice (1 or 2): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            return 'noip'
        elif choice == '2':
            return 'traffic_armor'
        else:
            print_colored("❌ Invalid choice. Please enter 1 or 2", Fore.RED)

def show_progress_info():
    """Show information about the generation process"""
    info = f"""
{Fore.CYAN}📋 Generation Process Overview:{Style.RESET_ALL}

{Fore.YELLOW}1. Theme Generation{Style.RESET_ALL} - AI creates 3 unique theme concepts
{Fore.YELLOW}2. Design System{Style.RESET_ALL} - Color palettes and typography
{Fore.YELLOW}3. Image Generation{Style.RESET_ALL} - DALL-E creates hero image & favicon  
{Fore.YELLOW}4. Games Integration{Style.RESET_ALL} - Fetches real casino games
{Fore.YELLOW}5. Content Creation{Style.RESET_ALL} - AI generates all page content
{Fore.YELLOW}6. Website Building{Style.RESET_ALL} - HTML, CSS, and JS generation
{Fore.YELLOW}7. Anti-Fingerprinting{Style.RESET_ALL} - Unique code obfuscation

{Fore.GREEN}⏱️  Estimated time: 5-10 minutes{Style.RESET_ALL}
{Fore.BLUE}💡 Tip: Have a coffee while the AI works its magic!{Style.RESET_ALL}
"""
    print(info)

async def main():
    """Main application entry point"""
    display_welcome()
    
    # Check requirements
    if not check_requirements():
        print_colored("\n❌ Setup incomplete. Please fix the issues above and try again.", Fore.RED)
        sys.exit(1)
    
    print_colored("🚀 Ready to generate your casino website!", Fore.GREEN)
    
    # Get user inputs
    domain_name = get_domain_input()
    deployment_type = get_deployment_type()
    
    # Show process info
    show_progress_info()
    
    # Confirm before starting
    confirm = input(f"{Fore.YELLOW}🎯 Ready to generate website for '{domain_name}'? (y/N): {Style.RESET_ALL}").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print_colored("👋 Generation cancelled. See you next time!", Fore.YELLOW)
        sys.exit(0)
    
    # Initialize and run generator
    try:
        generator = CasinoWebsiteGenerator()
        await generator.generate_website(domain_name, deployment_type)
        
        # Success message
        success_msg = f"""
{Fore.GREEN}🎉 SUCCESS! Your casino website has been generated!{Style.RESET_ALL}

{Fore.CYAN}📁 Output Location:{Style.RESET_ALL} output/{domain_name.replace('.', '_')}/
{Fore.CYAN}🌐 Domain:{Style.RESET_ALL} {domain_name}
{Fore.CYAN}📦 Deployment:{Style.RESET_ALL} {deployment_type}

{Fore.YELLOW}📋 Next Steps:{Style.RESET_ALL}
1. Review the generated files in the output directory
2. Upload files to your web server
3. Configure domain DNS settings
4. Test the website functionality

{Fore.BLUE}💡 Pro Tips:{Style.RESET_ALL}
- All games are for entertainment only (no real money)
- Legal pages are included for compliance
- Website is mobile-responsive and SEO-ready
- Each generation is unique with anti-fingerprinting

{Fore.GREEN}🎰 Happy gaming and good luck with your casino website!{Style.RESET_ALL}
"""
        print(success_msg)
        
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Generation cancelled by user", Fore.YELLOW)
    except Exception as e:
        print_colored(f"\n❌ Generation failed: {str(e)}", Fore.RED)
        print_colored("Check the error above and try again", Fore.YELLOW)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_colored("\n👋 Goodbye!", Fore.CYAN)
        sys.exit(0)