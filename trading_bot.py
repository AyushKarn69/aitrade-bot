"""
Main Trading Bot Class
Orchestrates all trading operations and provides the main interface
"""
import logging
from typing import Dict, List, Optional, Tuple
from binance_client import BinanceFuturesClient
from logger import log_trade_action, log_error, log_performance_metrics
from config import Config

class TradingBot:
    """Main trading bot class"""
    
    def __init__(self):
        """Initialize the trading bot"""
        self.logger = logging.getLogger(__name__)
        self.client = BinanceFuturesClient()
        self.running = False
        
        # Performance tracking
        self.trade_count = 0
        self.successful_trades = 0
        self.failed_trades = 0
        
        self.logger.info("Trading Bot initialized successfully")
    
    def start(self):
        """Start the trading bot"""
        self.running = True
        self.logger.info("Trading Bot started")
        
        # Display initial account info
        self.display_account_info()
    
    def stop(self):
        """Stop the trading bot"""
        self.running = False
        self.logger.info("Trading Bot stopped")
        
        # Display final performance metrics
        self.display_performance_metrics()
    
    def display_account_info(self):
        """Display current account information"""
        try:
            account_info = self.client.get_account_info()
            
            print("\n" + "="*50)
            print("ACCOUNT INFORMATION")
            print("="*50)
            print(f"Total Wallet Balance: {account_info['total_wallet_balance']} USDT")
            print(f"Available Balance: {account_info['available_balance']} USDT")
            print(f"Total Unrealized PnL: {account_info['total_unrealized_pnl']} USDT")
            print(f"Total Margin Balance: {account_info['total_margin_balance']} USDT")
            print(f"Max Withdraw Amount: {account_info['max_withdraw_amount']} USDT")
            print("="*50 + "\n")
            
        except Exception as e:
            log_error(e, "display_account_info")
            print(f"Error getting account info: {str(e)}")
    
    def display_positions(self):
        """Display current positions"""
        try:
            positions = self.client.get_positions()
            
            if not positions:
                print("No open positions")
                return
            
            print("\n" + "="*80)
            print("CURRENT POSITIONS")
            print("="*80)
            print(f"{'Symbol':<12} {'Side':<6} {'Size':<15} {'Entry Price':<12} {'Mark Price':<12} {'PnL':<12}")
            print("-"*80)
            
            for pos in positions:
                symbol = pos['symbol']
                side = "LONG" if float(pos['positionAmt']) > 0 else "SHORT"
                size = abs(float(pos['positionAmt']))
                entry_price = pos['entryPrice']
                mark_price = pos['markPrice']
                pnl = pos['unRealizedProfit']
                
                print(f"{symbol:<12} {side:<6} {size:<15.6f} {entry_price:<12} {mark_price:<12} {pnl:<12}")
            
            print("="*80 + "\n")
            
        except Exception as e:
            log_error(e, "display_positions")
            print(f"Error getting positions: {str(e)}")
    
    def display_open_orders(self, symbol: Optional[str] = None):
        """Display open orders"""
        try:
            orders = self.client.get_open_orders(symbol)
            
            if not orders:
                print(f"No open orders{' for ' + symbol if symbol else ''}")
                return
            
            print(f"\n{'='*100}")
            print(f"OPEN ORDERS{' for ' + symbol if symbol else ''}")
            print(f"{'='*100}")
            print(f"{'Order ID':<12} {'Symbol':<12} {'Side':<6} {'Type':<12} {'Quantity':<15} {'Price':<12} {'Status':<12}")
            print("-"*100)
            
            for order in orders:
                order_id = str(order['orderId'])
                symbol = order['symbol']
                side = order['side']
                order_type = order['type']
                quantity = order['origQty']
                price = order.get('price', 'Market')
                status = order['status']
                
                print(f"{order_id:<12} {symbol:<12} {side:<6} {order_type:<12} {quantity:<15} {price:<12} {status:<12}")
            
            print("="*100 + "\n")
            
        except Exception as e:
            log_error(e, "display_open_orders")
            print(f"Error getting open orders: {str(e)}")
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> bool:
        """Place a market order"""
        try:
            self.logger.info(f"Placing market {side} order for {quantity} {symbol}")
            
            order = self.client.place_market_order(symbol, side, quantity)
            
            log_trade_action("MARKET_ORDER", symbol, side, quantity, 
                           order_id=str(order['orderId']))
            
            self.trade_count += 1
            self.successful_trades += 1
            
            print(f"✅ Market {side} order placed successfully!")
            print(f"   Order ID: {order['orderId']}")
            print(f"   Symbol: {symbol}")
            print(f"   Quantity: {quantity}")
            print(f"   Status: {order['status']}")
            
            return True
            
        except Exception as e:
            log_error(e, f"place_market_order({symbol}, {side}, {quantity})")
            self.trade_count += 1
            self.failed_trades += 1
            
            print(f"❌ Failed to place market {side} order: {str(e)}")
            return False
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                         price: float) -> bool:
        """Place a limit order"""
        try:
            self.logger.info(f"Placing limit {side} order for {quantity} {symbol} at {price}")
            
            order = self.client.place_limit_order(symbol, side, quantity, price)
            
            log_trade_action("LIMIT_ORDER", symbol, side, quantity, price, 
                           str(order['orderId']))
            
            self.trade_count += 1
            self.successful_trades += 1
            
            print(f"✅ Limit {side} order placed successfully!")
            print(f"   Order ID: {order['orderId']}")
            print(f"   Symbol: {symbol}")
            print(f"   Quantity: {quantity}")
            print(f"   Price: {price}")
            print(f"   Status: {order['status']}")
            
            return True
            
        except Exception as e:
            log_error(e, f"place_limit_order({symbol}, {side}, {quantity}, {price})")
            self.trade_count += 1
            self.failed_trades += 1
            
            print(f"❌ Failed to place limit {side} order: {str(e)}")
            return False
    
    def cancel_order(self, symbol: str, order_id: int) -> bool:
        """Cancel an order"""
        try:
            self.logger.info(f"Cancelling order {order_id} for {symbol}")
            
            result = self.client.cancel_order(symbol, order_id)
            
            print(f"✅ Order {order_id} cancelled successfully!")
            print(f"   Symbol: {symbol}")
            print(f"   Status: {result['status']}")
            
            return True
            
        except Exception as e:
            log_error(e, f"cancel_order({symbol}, {order_id})")
            print(f"❌ Failed to cancel order {order_id}: {str(e)}")
            return False
    
    def get_current_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            price = self.client.get_current_price(symbol)
            return price
        except Exception as e:
            log_error(e, f"get_current_price({symbol})")
            raise
    
    def display_performance_metrics(self):
        """Display performance metrics"""
        if self.trade_count == 0:
            print("No trades executed yet.")
            return
        
        success_rate = (self.successful_trades / self.trade_count) * 100
        
        metrics = {
            "Total Trades": self.trade_count,
            "Successful Trades": self.successful_trades,
            "Failed Trades": self.failed_trades,
            "Success Rate": f"{success_rate:.2f}%"
        }
        
        log_performance_metrics(metrics)
        
        print("\n" + "="*40)
        print("PERFORMANCE METRICS")
        print("="*40)
        for key, value in metrics.items():
            print(f"{key}: {value}")
        print("="*40 + "\n")
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists and is tradeable"""
        try:
            symbol_info = self.client.get_symbol_info(symbol)
            return symbol_info['status'] == 'TRADING'
        except Exception as e:
            self.logger.warning(f"Symbol validation failed for {symbol}: {str(e)}")
            return False
    
    def get_symbol_info(self, symbol: str) -> Dict:
        """Get detailed symbol information"""
        try:
            return self.client.get_symbol_info(symbol)
        except Exception as e:
            log_error(e, f"get_symbol_info({symbol})")
            raise
