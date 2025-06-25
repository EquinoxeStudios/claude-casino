import asyncio
import aiohttp
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from config import SLOTSLAUNCH_API_TOKEN, SLOTSLAUNCH_BASE_URL, SLOTSLAUNCH_GAMES_ENDPOINT, RATE_LIMIT_DELAY
from utils import print_colored, create_directory, sanitize_filename
from colorama import Fore

class GameManager:
    def __init__(self):
        self.api_token = SLOTSLAUNCH_API_TOKEN
        self.base_url = SLOTSLAUNCH_BASE_URL
        self.games_endpoint = SLOTSLAUNCH_GAMES_ENDPOINT
        
    async def fetch_games(self, domain_name=None):
        """Fetch games from SlotsLaunch API"""
        try:
            # Check if API token is configured
            if not self.api_token or self.api_token == 'your_slotslaunch_token_here':
                print_colored("⚠️ SlotsLaunch API token not configured", Fore.YELLOW)
                print_colored("Using fallback demo games", Fore.YELLOW)
                return self.get_fallback_games()
            
            # Headers according to SlotsLaunch API documentation
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # Add Origin header with the domain being built (required by API)
            if domain_name:
                headers['Origin'] = domain_name
            else:
                print_colored("⚠️ No domain name provided for Origin header", Fore.YELLOW)
            
            # Token goes in the URL as per API documentation
            url = f"{self.base_url}{self.games_endpoint}?token={self.api_token}"
            
            # Debug information (mask token for security)
            masked_token = f"{self.api_token[:6]}..." if len(self.api_token) > 6 else "***"
            print_colored(f"🔗 API URL: {self.base_url}{self.games_endpoint}", Fore.CYAN)
            print_colored(f"🔑 Token: {masked_token}", Fore.CYAN)
            print_colored(f"📤 Headers: {headers}", Fore.CYAN)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # SlotsLaunch API returns games in 'data' array, not 'games'
                        games = data.get('data', [])
                        total_games = data.get('meta', {}).get('total', len(games))
                        
                        print_colored(f"✅ Fetched {len(games)} games from SlotsLaunch API", Fore.GREEN)
                        print_colored(f"📊 Total games available: {total_games}", Fore.CYAN)
                        
                        # If no games, check for error messages in response
                        if len(games) == 0:
                            if 'error' in data:
                                print_colored(f"⚠️ API Error: {data['error']}", Fore.YELLOW)
                            if 'message' in data:
                                print_colored(f"⚠️ API Message: {data['message']}", Fore.YELLOW)
                            print_colored("🔧 Possible issues:", Fore.YELLOW)
                            print_colored("   - Invalid API token", Fore.YELLOW)
                            print_colored("   - Domain not registered for this token", Fore.YELLOW)
                            print_colored("   - Token not configured properly", Fore.YELLOW)
                            return self.get_fallback_games()
                        
                        # Process games data
                        processed_games = []
                        for game in games:
                            processed_game = self.process_game_data(game)
                            processed_games.append(processed_game)
                        
                        return processed_games
                    elif response.status == 401:
                        print_colored(f"❌ API authentication failed: Invalid token", Fore.RED)
                        print_colored("Please check your SLOTSLAUNCH_API_TOKEN in .env file", Fore.YELLOW)
                        return self.get_fallback_games()
                    elif response.status == 403:
                        print_colored(f"❌ API access forbidden: Check Origin header", Fore.RED)
                        print_colored(f"Origin header sent: {headers.get('Origin', 'None')}", Fore.YELLOW)
                        return self.get_fallback_games()
                    else:
                        error_text = await response.text()
                        print_colored(f"❌ API request failed: {response.status} - {error_text}", Fore.RED)
                        return self.get_fallback_games()
                        
        except Exception as e:
            print_colored(f"❌ Error fetching games: {e}", Fore.RED)
            return self.get_fallback_games()
    
    def process_game_data(self, game):
        """Process and normalize game data from SlotsLaunch API"""
        return {
            'id': game.get('id', ''),
            'name': game.get('name', 'Unknown Game'),
            'slug': game.get('slug', game.get('name', '').lower().replace(' ', '-')),
            'provider': game.get('provider', 'Unknown'),
            'category': game.get('type', 'slots').lower(),  # API uses 'type' field
            'thumbnail': game.get('thumb', ''),  # API uses 'thumb' field
            'play_url': game.get('url', ''),  # API uses 'url' field
            'demo_url': game.get('url', ''),  # Same as play_url for SlotsLaunch
            'description': game.get('description', '') or f"Play {game.get('name', 'this game')} from {game.get('provider', 'top provider')}",
            'rtp': f"{game.get('rtp', 96)}%" if game.get('rtp') else '96%',
            'volatility': self._map_volatility(game.get('volatility', '')),
            'min_bet': game.get('min_bet', '0.01'),
            'max_bet': game.get('max_bet', '100.00'),
            'paylines': game.get('payline', '25'),  # API uses 'payline' field
            'reels': game.get('reels', '5'),
            'tags': self._extract_tags(game),
            'features': self._extract_features(game),
            'released': game.get('release', '2023'),  # API uses 'release' field
            'mobile_compatible': True  # Assume all games are mobile compatible
        }
    
    def _map_volatility(self, volatility):
        """Map volatility number to text"""
        if not volatility:
            return 'Medium'
        
        volatility_str = str(volatility)
        volatility_map = {
            '1': 'Very Low',
            '2': 'Low', 
            '3': 'Medium',
            '4': 'High',
            '5': 'Very High'
        }
        return volatility_map.get(volatility_str, 'Medium')
    
    def _extract_tags(self, game):
        """Extract tags from game data"""
        tags = []
        
        # Add provider as tag
        if game.get('provider'):
            tags.append(game['provider'].lower())
        
        # Add themes as tags
        if game.get('themes') and isinstance(game['themes'], list):
            for theme in game['themes']:
                if isinstance(theme, dict) and 'name' in theme:
                    tags.append(theme['name'].lower())
        
        # Add game type as tag
        if game.get('type'):
            tags.append(game['type'].lower())
            
        return tags
    
    def _extract_features(self, game):
        """Extract features from game data"""
        features = []
        
        # Check for various feature flags
        if game.get('megaways'):
            features.append('Megaways')
        if game.get('bonus_buy'):
            features.append('Bonus Buy')
        if game.get('progressive'):
            features.append('Progressive Jackpot')
        if game.get('scatter_pays'):
            features.append('Scatter Pays')
        if game.get('tumbling_reels'):
            features.append('Tumbling Reels')
        if game.get('increasing_multipliers'):
            features.append('Increasing Multipliers')
        if game.get('autoplay'):
            features.append('Autoplay')
        if game.get('quickspin'):
            features.append('Quick Spin')
            
        # If no features found, add some generic ones
        if not features:
            features = ['Wild Symbols', 'Scatter Symbols']
            
        return features
    
    async def download_game_thumbnails(self, games, output_dir):
        """Download game thumbnails concurrently"""
        print_colored("📥 Downloading game thumbnails...", Fore.YELLOW)
        
        # Create images directory
        images_dir = f"{output_dir}/images/games"
        create_directory(images_dir)
        
        # Download thumbnails concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks = []
            for game in games:
                if game.get('thumbnail'):
                    task = executor.submit(self.download_single_thumbnail, game, images_dir)
                    tasks.append(task)
            
            # Wait for all downloads to complete
            for task in tasks:
                task.result()
        
        print_colored(f"✅ Downloaded thumbnails for {len(games)} games", Fore.GREEN)
        return games
    
    def download_single_thumbnail(self, game, images_dir):
        """Download a single game thumbnail"""
        try:
            if not game.get('thumbnail'):
                return
                
            # Add rate limiting
            time.sleep(RATE_LIMIT_DELAY)
            
            response = requests.get(game['thumbnail'], timeout=30)
            if response.status_code == 200:
                # Generate filename
                filename = f"{sanitize_filename(game['slug'])}.jpg"
                filepath = f"{images_dir}/{filename}"
                
                # Save image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # Update game data with local path
                game['local_thumbnail'] = f"images/games/{filename}"
                
        except Exception as e:
            print_colored(f"❌ Error downloading thumbnail for {game.get('name', 'Unknown')}: {e}", Fore.RED)
            game['local_thumbnail'] = "images/placeholder-game.jpg"
    
    def get_game_iframe_code(self, game, width="100%", height="600px"):
        """Generate iframe code for game embedding with proper token handling"""
        if game.get('demo_url'):
            iframe_url = self._build_iframe_url_with_token(game['demo_url'])
            game_title = game.get('name', 'Casino Game')
            
            return f"""
            <!-- Game iframe for {game_title} -->
            <iframe 
                id="gameIframe"
                class="game-iframe"
                src="{iframe_url}" 
                title="{game_title}"
                width="{width}" 
                height="{height}"
                frameborder="0"
                allowfullscreen
                sandbox="allow-scripts allow-same-origin allow-forms"
                loading="lazy"
                onload="hideLoading()"
                onerror="showError()">
            </iframe>
            """
        else:
            return f"""
            <!-- Game not available placeholder -->
            <div class="game-placeholder" style="width:{width}; height:{height};">
                <p>Game not available for demo</p>
            </div>
            """
    
    def _build_iframe_url_with_token(self, base_url):
        """Build iframe URL with API token if needed"""
        if not base_url or base_url == 'about:blank':
            return base_url
            
        # Check if it's a SlotsLaunch iframe URL
        if 'slotslaunch.com/iframe/' in base_url:
            # Only add token if it's configured and not a placeholder
            if self.api_token and self.api_token != 'your_slotslaunch_token_here':
                # Add token parameter
                separator = '&' if '?' in base_url else '?'
                return f"{base_url}{separator}token={self.api_token}"
        
        return base_url
    
    def get_games_by_category(self, games, category):
        """Filter games by category"""
        return [game for game in games if game.get('category', '').lower() == category.lower()]
    
    def get_games_by_provider(self, games, provider):
        """Filter games by provider"""
        return [game for game in games if game.get('provider', '').lower() == provider.lower()]
    
    def get_featured_games(self, games, count=6):
        """Get featured games (random selection)"""
        import random
        if len(games) <= count:
            return games
        return random.sample(games, count)
    
    def get_new_games(self, games, count=8):
        """Get newest games (sorted by release date)"""
        try:
            sorted_games = sorted(games, key=lambda x: x.get('released', '2020'), reverse=True)
            return sorted_games[:count]
        except:
            return games[:count]
    
    def get_popular_games(self, games, count=10):
        """Get popular games (placeholder logic - would use actual analytics)"""
        # For now, just return games with certain features
        popular = [game for game in games if 'free spins' in str(game.get('features', [])).lower()]
        if len(popular) < count:
            popular.extend(games[:count - len(popular)])
        return popular[:count]
    
    def get_fallback_games(self):
        """Return fallback games if API fails"""
        return [
            {
                'id': 'demo1',
                'name': 'Golden Fortune',
                'slug': 'golden-fortune',
                'provider': 'Demo Provider',
                'category': 'slots',
                'thumbnail': 'https://via.placeholder.com/300x200/ffd700/000000?text=Golden+Fortune',
                'demo_url': 'about:blank',
                'description': 'A classic slot game with golden treasures',
                'rtp': '96.5%',
                'volatility': 'Medium',
                'paylines': '25',
                'reels': '5',
                'tags': ['classic', 'gold', 'treasure'],
                'features': ['Free Spins', 'Wild Symbol'],
                'mobile_compatible': True
            },
            {
                'id': 'demo2',
                'name': 'Neon Nights',
                'slug': 'neon-nights',
                'provider': 'Demo Provider',
                'category': 'slots',
                'thumbnail': 'https://via.placeholder.com/300x200/ff00ff/000000?text=Neon+Nights',
                'demo_url': 'about:blank',
                'description': 'A futuristic slot with neon graphics',
                'rtp': '96.2%',
                'volatility': 'High',
                'paylines': '50',
                'reels': '5',
                'tags': ['futuristic', 'neon', 'modern'],
                'features': ['Multipliers', 'Bonus Round'],
                'mobile_compatible': True
            },
            {
                'id': 'demo3',
                'name': 'Mystic Forest',
                'slug': 'mystic-forest',
                'provider': 'Demo Provider',
                'category': 'slots',
                'thumbnail': 'https://via.placeholder.com/300x200/228B22/FFFFFF?text=Mystic+Forest',
                'demo_url': 'about:blank',
                'description': 'Magical forest adventure slot',
                'rtp': '96.8%',
                'volatility': 'Low',
                'paylines': '30',
                'reels': '5',
                'tags': ['magic', 'forest', 'adventure'],
                'features': ['Scatter Symbols', 'Free Games'],
                'mobile_compatible': True
            }
        ]