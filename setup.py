#!/usr/bin/env python3
"""
Setup script for Casino Website Generator
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print("✅ Python version compatible")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def setup_environment():
    """Set up environment configuration"""
    if not os.path.exists('.env'):
        print("📝 Creating environment file...")
        with open('.env.example', 'r') as example:
            with open('.env', 'w') as env_file:
                env_file.write(example.read())
        print("✅ Environment file created (.env)")
        print("⚠️  Please add your API keys to the .env file before running the generator")
    else:
        print("✅ Environment file already exists")

def create_directories():
    """Create necessary directories"""
    directories = ['output', 'temp', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")

def main():
    """Main setup function"""
    print("🎰 Casino Website Generator Setup")
    print("=" * 40)
    
    check_python_version()
    install_dependencies()
    setup_environment()
    create_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Add your API keys to the .env file:")
    print("   - OPENAI_API_KEY (for content generation)")
    print("   - SLOTSLAUNCH_API_TOKEN (for casino games)")
    print("2. Run: python main.py")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main()