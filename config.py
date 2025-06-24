import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SLOTSLAUNCH_API_TOKEN = os.getenv('SLOTSLAUNCH_API_TOKEN')

# SlotsLaunch API Configuration
# Production API endpoint
SLOTSLAUNCH_BASE_URL = os.getenv('SLOTSLAUNCH_BASE_URL', "https://slotslaunch.com")
SLOTSLAUNCH_GAMES_ENDPOINT = "/api/games"

THEME_COLORS = {
    'primary': '#1a1a2e',
    'secondary': '#16213e',
    'accent': '#0f3460',
    'gold': '#ffd700',
    'red': '#e94560',
    'green': '#2ed573',
    'white': '#ffffff',
    'gray': '#f5f5f5'
}

GOOGLE_FONTS = [
    'Roboto', 'Open Sans', 'Lato', 'Montserrat', 'Source Sans Pro',
    'Raleway', 'Nunito', 'Poppins', 'Playfair Display', 'Merriweather'
]

RATE_LIMIT_DELAY = 0.1  # seconds between API calls