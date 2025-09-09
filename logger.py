"""
Logging configuration for the Trading Bot
"""
import logging
import os
from datetime import datetime
from config import Config

def setup_logger():
    """Set up logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger('trading_bot')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # File handler for detailed logs
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Console handler for user-friendly output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    return logger

def log_api_request(method: str, endpoint: str, params: dict = None, response: dict = None):
    """Log API requests and responses"""
    logger = logging.getLogger('trading_bot.api')
    
    # Log request
    logger.info(f"API Request: {method} {endpoint}")
    if params:
        # Mask sensitive information
        safe_params = {k: v for k, v in params.items() 
                      if k.lower() not in ['api_key', 'secret', 'signature']}
        logger.debug(f"Request params: {safe_params}")
    
    # Log response
    if response:
        logger.info(f"API Response: {response.get('status', 'unknown')}")
        logger.debug(f"Response data: {response}")

def log_trade_action(action: str, symbol: str, side: str, quantity: float, 
                    price: float = None, order_id: str = None):
    """Log trading actions"""
    logger = logging.getLogger('trading_bot.trades')
    
    message = f"TRADE: {action} {side} {quantity} {symbol}"
    if price:
        message += f" @ {price}"
    if order_id:
        message += f" (Order ID: {order_id})"
    
    logger.info(message)

def log_error(error: Exception, context: str = ""):
    """Log errors with context"""
    logger = logging.getLogger('trading_bot.errors')
    
    message = f"ERROR in {context}: {str(error)}"
    logger.error(message, exc_info=True)

def log_performance_metrics(metrics: dict):
    """Log performance metrics"""
    logger = logging.getLogger('trading_bot.performance')
    
    logger.info("PERFORMANCE METRICS:")
    for key, value in metrics.items():
        logger.info(f"  {key}: {value}")

# Initialize logger when module is imported
main_logger = setup_logger()
