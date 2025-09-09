"""
Configuration settings for the Trading Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the trading bot"""
    
    # Binance Futures Testnet Configuration
    BINANCE_TESTNET_BASE_URL = "https://testnet.binancefuture.com"
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
    BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY', '')
    
    # Trading Configuration
    DEFAULT_SYMBOL = os.getenv('DEFAULT_SYMBOL', 'BTCUSDT')
    DEFAULT_QUANTITY = float(os.getenv('DEFAULT_QUANTITY', '0.001'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'trading_bot.log')
    
    # UI Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', '8501'))
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.BINANCE_API_KEY or not cls.BINANCE_SECRET_KEY:
            raise ValueError("Binance API Key and Secret Key must be provided in environment variables")
        return True
