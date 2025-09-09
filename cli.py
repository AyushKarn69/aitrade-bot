"""
Command Line Interface for the Trading Bot
"""
import sys
import logging
from typing import Optional
from colorama import init, Fore, Style
from tabulate import tabulate
from trading_bot import TradingBot
from config import Config

# Initialize colorama for colored output
init(autoreset=True)

class TradingBotCLI:
    """Command Line Interface for the Trading Bot"""
    
    def __init__(self):
        """Initialize the CLI"""
        self.bot = TradingBot()
        self.logger = logging.getLogger(__name__)
        
    def display_welcome(self):
        """Display welcome message"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🚀 BINANCE FUTURES TESTNET TRADING BOT")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}Welcome to the Trading Bot CLI!")
        print(f"{Fore.YELLOW}This bot connects to Binance Futures Testnet for safe trading practice.")
        print(f"{Fore.GREEN}Type 'help' to see available commands or 'quit' to exit.")
        print(f"{Fore.CYAN}{'='*60}\n")
    
    def display_help(self):
        """Display help information"""
        help_data = [
            ["Command", "Description"],
            ["help", "Show this help message"],
            ["info", "Display account information"],
            ["positions", "Show current positions"],
            ["orders [symbol]", "Show open orders (optionally for specific symbol)"],
            ["price <symbol>", "Get current price for a symbol"],
            ["buy_market <symbol> <quantity>", "Place market buy order"],
            ["sell_market <symbol> <quantity>", "Place market sell order"],
            ["buy_limit <symbol> <quantity> <price>", "Place limit buy order"],
            ["sell_limit <symbol> <quantity> <price>", "Place limit sell order"],
            ["cancel <symbol> <order_id>", "Cancel an order"],
            ["history <symbol>", "Show order history for symbol"],
            ["symbols", "List available trading symbols"],
            ["performance", "Show trading performance metrics"],
            ["start", "Start the trading bot"],
            ["stop", "Stop the trading bot"],
            ["quit/exit", "Exit the application"]
        ]
        
        print(f"\n{Fore.GREEN}AVAILABLE COMMANDS:")
        print(tabulate(help_data, headers="firstrow", tablefmt="grid"))
        print()
    
    def parse_command(self, command: str) -> tuple:
        """Parse user command"""
        parts = command.strip().split()
        if not parts:
            return None, []
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        return cmd, args
    
    def handle_info(self, args: list):
        """Handle info command"""
        self.bot.display_account_info()
    
    def handle_positions(self, args: list):
        """Handle positions command"""
        self.bot.display_positions()
    
    def handle_orders(self, args: list):
        """Handle orders command"""
        symbol = args[0] if args else None
        self.bot.display_open_orders(symbol)
    
    def handle_price(self, args: list):
        """Handle price command"""
        if not args:
            print(f"{Fore.RED}❌ Please provide a symbol. Usage: price <symbol>")
            return
        
        symbol = args[0].upper()
        
        try:
            price = self.bot.get_current_price(symbol)
            print(f"{Fore.GREEN}💰 Current price of {symbol}: {price} USDT")
        except Exception as e:
            print(f"{Fore.RED}❌ Error getting price for {symbol}: {str(e)}")
    
    def handle_buy_market(self, args: list):
        """Handle market buy order"""
        if len(args) < 2:
            print(f"{Fore.RED}❌ Usage: buy_market <symbol> <quantity>")
            return
        
        symbol = args[0].upper()
        try:
            quantity = float(args[1])
        except ValueError:
            print(f"{Fore.RED}❌ Invalid quantity. Please enter a number.")
            return
        
        if not self.bot.validate_symbol(symbol):
            print(f"{Fore.RED}❌ Invalid or non-tradeable symbol: {symbol}")
            return
        
        self.bot.place_market_order(symbol, "BUY", quantity)
    
    def handle_sell_market(self, args: list):
        """Handle market sell order"""
        if len(args) < 2:
            print(f"{Fore.RED}❌ Usage: sell_market <symbol> <quantity>")
            return
        
        symbol = args[0].upper()
        try:
            quantity = float(args[1])
        except ValueError:
            print(f"{Fore.RED}❌ Invalid quantity. Please enter a number.")
            return
        
        if not self.bot.validate_symbol(symbol):
            print(f"{Fore.RED}❌ Invalid or non-tradeable symbol: {symbol}")
            return
        
        self.bot.place_market_order(symbol, "SELL", quantity)
    
    def handle_buy_limit(self, args: list):
        """Handle limit buy order"""
        if len(args) < 3:
            print(f"{Fore.RED}❌ Usage: buy_limit <symbol> <quantity> <price>")
            return
        
        symbol = args[0].upper()
        try:
            quantity = float(args[1])
            price = float(args[2])
        except ValueError:
            print(f"{Fore.RED}❌ Invalid quantity or price. Please enter numbers.")
            return
        
        if not self.bot.validate_symbol(symbol):
            print(f"{Fore.RED}❌ Invalid or non-tradeable symbol: {symbol}")
            return
        
        self.bot.place_limit_order(symbol, "BUY", quantity, price)
    
    def handle_sell_limit(self, args: list):
        """Handle limit sell order"""
        if len(args) < 3:
            print(f"{Fore.RED}❌ Usage: sell_limit <symbol> <quantity> <price>")
            return
        
        symbol = args[0].upper()
        try:
            quantity = float(args[1])
            price = float(args[2])
        except ValueError:
            print(f"{Fore.RED}❌ Invalid quantity or price. Please enter numbers.")
            return
        
        if not self.bot.validate_symbol(symbol):
            print(f"{Fore.RED}❌ Invalid or non-tradeable symbol: {symbol}")
            return
        
        self.bot.place_limit_order(symbol, "SELL", quantity, price)
    
    def handle_cancel(self, args: list):
        """Handle cancel order command"""
        if len(args) < 2:
            print(f"{Fore.RED}❌ Usage: cancel <symbol> <order_id>")
            return
        
        symbol = args[0].upper()
        try:
            order_id = int(args[1])
        except ValueError:
            print(f"{Fore.RED}❌ Invalid order ID. Please enter a number.")
            return
        
        self.bot.cancel_order(symbol, order_id)
    
    def handle_history(self, args: list):
        """Handle order history command"""
        if not args:
            print(f"{Fore.RED}❌ Please provide a symbol. Usage: history <symbol>")
            return
        
        symbol = args[0].upper()
        
        try:
            orders = self.bot.client.get_order_history(symbol, limit=20)
            
            if not orders:
                print(f"No order history found for {symbol}")
                return
            
            print(f"\n{Fore.GREEN}Order History for {symbol}:")
            print("-" * 80)
            
            for order in orders[-10:]:  # Show last 10 orders
                order_id = order['orderId']
                side = order['side']
                order_type = order['type']
                quantity = order['origQty']
                price = order.get('price', 'Market')
                status = order['status']
                time = order['time']
                
                print(f"ID: {order_id} | {side} {order_type} | Qty: {quantity} | "
                      f"Price: {price} | Status: {status} | Time: {time}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error getting order history: {str(e)}")
    
    def handle_symbols(self, args: list):
        """Handle symbols command"""
        try:
            exchange_info = self.bot.client.client.futures_exchange_info()
            symbols = [s['symbol'] for s in exchange_info['symbols'] 
                      if s['status'] == 'TRADING']
            
            print(f"\n{Fore.GREEN}Available Trading Symbols ({len(symbols)} total):")
            print("-" * 50)
            
            # Display symbols in columns
            for i in range(0, len(symbols), 4):
                row_symbols = symbols[i:i+4]
                print("  ".join(f"{s:<12}" for s in row_symbols))
            
            print()
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error getting symbols: {str(e)}")
    
    def handle_performance(self, args: list):
        """Handle performance command"""
        self.bot.display_performance_metrics()
    
    def handle_start(self, args: list):
        """Handle start command"""
        self.bot.start()
    
    def handle_stop(self, args: list):
        """Handle stop command"""
        self.bot.stop()
    
    def run(self):
        """Run the CLI"""
        self.display_welcome()
        
        # Start the bot
        self.bot.start()
        
        try:
            while True:
                try:
                    # Get user input
                    command = input(f"{Fore.CYAN}bot> {Style.RESET_ALL}").strip()
                    
                    if not command:
                        continue
                    
                    # Parse command
                    cmd, args = self.parse_command(command)
                    
                    if not cmd:
                        continue
                    
                    # Handle commands
                    if cmd in ['quit', 'exit']:
                        print(f"{Fore.YELLOW}👋 Goodbye!")
                        break
                    elif cmd == 'help':
                        self.handle_help()
                    elif cmd == 'info':
                        self.handle_info(args)
                    elif cmd == 'positions':
                        self.handle_positions(args)
                    elif cmd == 'orders':
                        self.handle_orders(args)
                    elif cmd == 'price':
                        self.handle_price(args)
                    elif cmd == 'buy_market':
                        self.handle_buy_market(args)
                    elif cmd == 'sell_market':
                        self.handle_sell_market(args)
                    elif cmd == 'buy_limit':
                        self.handle_buy_limit(args)
                    elif cmd == 'sell_limit':
                        self.handle_sell_limit(args)
                    elif cmd == 'cancel':
                        self.handle_cancel(args)
                    elif cmd == 'history':
                        self.handle_history(args)
                    elif cmd == 'symbols':
                        self.handle_symbols(args)
                    elif cmd == 'performance':
                        self.handle_performance(args)
                    elif cmd == 'start':
                        self.handle_start(args)
                    elif cmd == 'stop':
                        self.handle_stop(args)
                    else:
                        print(f"{Fore.RED}❌ Unknown command: {cmd}")
                        print(f"{Fore.YELLOW}Type 'help' to see available commands.")
                
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}👋 Goodbye!")
                    break
                except EOFError:
                    print(f"\n{Fore.YELLOW}👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"{Fore.RED}❌ Unexpected error: {str(e)}")
                    self.logger.error(f"CLI error: {str(e)}", exc_info=True)
        
        finally:
            self.bot.stop()

if __name__ == "__main__":
    try:
        cli = TradingBotCLI()
        cli.run()
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to start CLI: {str(e)}")
        sys.exit(1)
