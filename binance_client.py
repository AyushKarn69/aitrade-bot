"""
Binance Futures Testnet Client
Handles all API interactions with Binance Futures Testnet
"""
import logging
import time
from typing import Dict, List, Optional, Tuple
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from config import Config

class BinanceFuturesClient:
    """Client for interacting with Binance Futures Testnet"""
    
    def __init__(self):
        """Initialize the Binance client"""
        self.client = None
        self.logger = logging.getLogger(__name__)
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Binance client with testnet configuration"""
        try:
            # Initialize client with testnet configuration
            self.client = Client(
                api_key=Config.BINANCE_API_KEY,
                api_secret=Config.BINANCE_SECRET_KEY,
                testnet=True  # This ensures we use the testnet
            )
            
            # Test the connection
            account_info = self.client.futures_account()
            self.logger.info("Successfully connected to Binance Futures Testnet")
            self.logger.info(f"Account balance: {account_info.get('totalWalletBalance', 'N/A')} USDT")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise
    
    def get_account_info(self) -> Dict:
        """Get account information"""
        try:
            account_info = self.client.futures_account()
            return {
                'total_wallet_balance': account_info.get('totalWalletBalance'),
                'total_unrealized_pnl': account_info.get('totalUnrealizedProfit'),
                'total_margin_balance': account_info.get('totalMarginBalance'),
                'available_balance': account_info.get('availableBalance'),
                'max_withdraw_amount': account_info.get('maxWithdrawAmount')
            }
        except Exception as e:
            self.logger.error(f"Failed to get account info: {str(e)}")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict:
        """Get symbol information"""
        try:
            exchange_info = self.client.futures_exchange_info()
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == symbol:
                    return symbol_info
            raise ValueError(f"Symbol {symbol} not found")
        except Exception as e:
            self.logger.error(f"Failed to get symbol info for {symbol}: {str(e)}")
            raise
    
    def get_current_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            self.logger.error(f"Failed to get current price for {symbol}: {str(e)}")
            raise
    
    def get_order_book(self, symbol: str, limit: int = 100) -> Dict:
        """Get order book for a symbol"""
        try:
            order_book = self.client.futures_order_book(symbol=symbol, limit=limit)
            return order_book
        except Exception as e:
            self.logger.error(f"Failed to get order book for {symbol}: {str(e)}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float, 
                          reduce_only: bool = False) -> Dict:
        """
        Place a market order
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            reduce_only: Whether this is a reduce-only order
        """
        try:
            self.logger.info(f"Placing market {side} order for {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity,
                reduceOnly=reduce_only
            )
            
            self.logger.info(f"Market order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error placing market order: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing market order: {str(e)}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                         price: float, time_in_force: str = 'GTC',
                         reduce_only: bool = False) -> Dict:
        """
        Place a limit order
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Order price
            time_in_force: Time in force ('GTC', 'IOC', 'FOK')
            reduce_only: Whether this is a reduce-only order
        """
        try:
            self.logger.info(f"Placing limit {side} order for {quantity} {symbol} at {price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce=time_in_force,
                reduceOnly=reduce_only
            )
            
            self.logger.info(f"Limit order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error placing limit order: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing limit order: {str(e)}")
            raise
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float,
                              price: float, stop_price: float,
                              time_in_force: str = 'GTC') -> Dict:
        """
        Place a stop-limit order
        
        Args:
            symbol: Trading pair symbol
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            price: Limit price
            stop_price: Stop price
            time_in_force: Time in force
        """
        try:
            self.logger.info(f"Placing stop-limit {side} order for {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP_MARKET',
                quantity=quantity,
                stopPrice=stop_price,
                timeInForce=time_in_force
            )
            
            self.logger.info(f"Stop-limit order placed successfully: {order}")
            return order
            
        except Exception as e:
            self.logger.error(f"Error placing stop-limit order: {str(e)}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an order"""
        try:
            self.logger.info(f"Cancelling order {order_id} for {symbol}")
            
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            
            self.logger.info(f"Order cancelled successfully: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error cancelling order: {str(e)}")
            raise
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get open orders"""
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol)
            else:
                orders = self.client.futures_get_open_orders()
            
            return orders
            
        except Exception as e:
            self.logger.error(f"Error getting open orders: {str(e)}")
            raise
    
    def get_order_history(self, symbol: str, limit: int = 100) -> List[Dict]:
        """Get order history"""
        try:
            orders = self.client.futures_get_all_orders(
                symbol=symbol,
                limit=limit
            )
            return orders
            
        except Exception as e:
            self.logger.error(f"Error getting order history: {str(e)}")
            raise
    
    def get_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get current positions"""
        try:
            positions = self.client.futures_position_information()
            
            if symbol:
                positions = [pos for pos in positions if pos['symbol'] == symbol]
            
            # Filter out positions with zero size
            active_positions = [pos for pos in positions if float(pos['positionAmt']) != 0]
            
            return active_positions
            
        except Exception as e:
            self.logger.error(f"Error getting positions: {str(e)}")
            raise
