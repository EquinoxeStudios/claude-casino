#!/usr/bin/env python3
"""
Quick Start script for Casino Website Generator
Automatically runs setup and then launches the main application
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🎰 Casino Website Generator - Quick Start")
    print("=" * 50)
    
    # Check if setup has been run
    if not os.path.exists('.env'):
        print("🔧 First time setup required...")
        print("Running setup script...")
        
        try:
            subprocess.run([sys.executable, "setup.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Setup failed. Please run 'python setup.py' manually.")
            sys.exit(1)
        
        print("\n⚠️  Please edit the .env file with your API keys before continuing.")
        print("Press Enter when ready...")
        input()
    
    # Run the main application
    print("🚀 Launching Casino Website Generator...")
    try:
        subprocess.run([sys.executable, "run.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Application failed to start.")
        sys.exit(1)

if __name__ == "__main__":
    main()