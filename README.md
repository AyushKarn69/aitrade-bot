# 🚀 Binance Futures Testnet Trading Bot

A comprehensive Python trading bot for Binance Futures Testnet with advanced order types, web interfaces, and comprehensive logging.

## 📋 Features

### Core Features
- ✅ **Market Orders**: Instant buy/sell at current market price
- ✅ **Limit Orders**: Buy/sell at specified price levels
- ✅ **Account Management**: Real-time account balance and position tracking
- ✅ **Order Management**: View, cancel, and track orders
- ✅ **Comprehensive Logging**: All API requests, responses, and errors logged

### Advanced Features
- 🔧 **Stop-Limit Orders**: Advanced order types with stop and limit prices
- 📊 **Grid Trading**: Automated grid-based trading strategies
- ⏰ **TWAP Orders**: Time-Weighted Average Price execution
- 🛑 **Trailing Stop Orders**: Dynamic stop-loss management
- 📈 **OCO Orders**: One-Cancels-Other order management

### User Interfaces
- 💻 **Command Line Interface**: Full-featured CLI with colored output
- 🌐 **Flask Web UI**: Traditional web interface for trading
- 📊 **Streamlit Dashboard**: Modern, interactive trading dashboard

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Binance Futures Testnet account
- API Key and Secret Key from Binance Testnet

### Setup Steps

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   # Copy the template file
   cp env_template .env
   
   # Edit .env file with your API credentials
   BINANCE_API_KEY=your_api_key_here
   BINANCE_SECRET_KEY=your_secret_key_here
   ```

4. **Get Binance Futures Testnet API credentials**:
   - Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
   - Create an account and generate API Key and Secret Key
   - Update your `.env` file with these credentials

## 🚀 Usage

### Command Line Interface (CLI)

Start the CLI interface:
```bash
python cli.py
```

#### Available Commands:
- `help` - Show available commands
- `info` - Display account information
- `positions` - Show current positions
- `orders [symbol]` - Show open orders
- `price <symbol>` - Get current price
- `buy_market <symbol> <quantity>` - Place market buy order
- `sell_market <symbol> <quantity>` - Place market sell order
- `buy_limit <symbol> <quantity> <price>` - Place limit buy order
- `sell_limit <symbol> <quantity> <price>` - Place limit sell order
- `cancel <symbol> <order_id>` - Cancel an order
- `history <symbol>` - Show order history
- `symbols` - List available trading symbols
- `performance` - Show trading performance metrics

#### Example CLI Session:
```
bot> info
==================================================
ACCOUNT INFORMATION
==================================================
Total Wallet Balance: 10000.00 USDT
Available Balance: 10000.00 USDT
Total Unrealized PnL: 0.00 USDT
Total Margin Balance: 10000.00 USDT
Max Withdraw Amount: 10000.00 USDT
==================================================

bot> price BTCUSDT
💰 Current price of BTCUSDT: 43250.50 USDT

bot> buy_market BTCUSDT 0.001
✅ Market BUY order placed successfully!
   Order ID: 123456789
   Symbol: BTCUSDT
   Quantity: 0.001
   Status: FILLED
```

### Streamlit Web Dashboard

Start the Streamlit dashboard:
```bash
streamlit run streamlit_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

#### Dashboard Features:
- 📊 **Real-time Account Overview**: Balance, PnL, and margin information
- 📈 **Position Management**: View and manage open positions
- 📋 **Order Management**: Place, view, and cancel orders
- 🔧 **Advanced Orders**: Stop-limit, grid trading, and TWAP orders
- 📜 **Order History**: Complete trading history
- ⚙️ **Settings**: Configuration and performance metrics

### Flask Web UI

Start the Flask web interface:
```bash
python web_ui.py
```

The web interface will be available at `http://localhost:5000`

## 📁 Project Structure

```
trading_bot/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.py                # Configuration settings
├── env_template             # Environment variables template
├── logger.py                # Logging configuration
├── binance_client.py        # Binance API client
├── trading_bot.py           # Main trading bot class
├── cli.py                   # Command line interface
├── advanced_orders.py       # Advanced order types
├── web_ui.py               # Flask web interface
├── streamlit_app.py        # Streamlit dashboard
└── trading_bot.log         # Log file (created when running)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Binance Futures Testnet Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here

# Trading Configuration
DEFAULT_SYMBOL=BTCUSDT
DEFAULT_QUANTITY=0.001

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=trading_bot.log

# UI Configuration
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
STREAMLIT_PORT=8501
```

### Logging

The bot provides comprehensive logging:
- **File Logging**: All activities logged to `trading_bot.log`
- **Console Logging**: Real-time feedback in CLI
- **API Logging**: All Binance API requests and responses
- **Trade Logging**: All trading actions and results
- **Error Logging**: Detailed error information with stack traces

## 📊 Advanced Order Types

### Stop-Limit Orders
```python
# Place a stop-limit order
order = advanced_orders.place_stop_limit_order(
    symbol="BTCUSDT",
    side="SELL",
    quantity=0.001,
    limit_price=40000.0,
    stop_price=41000.0
)
```

### Grid Trading
```python
# Place grid orders
orders = advanced_orders.place_grid_orders(
    symbol="BTCUSDT",
    side="BUY",
    quantity=0.001,
    start_price=40000.0,
    end_price=45000.0,
    grid_count=10
)
```

### TWAP Orders
```python
# Place TWAP orders
orders = advanced_orders.place_twap_order(
    symbol="BTCUSDT",
    side="BUY",
    total_quantity=0.01,
    duration_minutes=30,
    intervals=10
)
```

## 🛡️ Risk Management

### Built-in Safety Features
- **Testnet Only**: All trading is done on Binance Futures Testnet
- **Input Validation**: All user inputs are validated before API calls
- **Error Handling**: Comprehensive error handling and logging
- **Rate Limiting**: Built-in delays to respect API rate limits
- **Position Tracking**: Real-time position and PnL monitoring

### Best Practices
- Always test strategies on testnet before live trading
- Monitor your positions regularly
- Set appropriate stop-losses and take-profits
- Never risk more than you can afford to lose
- Keep your API keys secure and never share them

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**:
   - Verify your API keys are correct
   - Ensure you're using Binance Futures Testnet credentials
   - Check your internet connection

2. **Invalid Symbol Error**:
   - Use correct symbol format (e.g., BTCUSDT, not BTC/USDT)
   - Check if the symbol is available for trading

3. **Insufficient Balance**:
   - Ensure you have enough balance in your testnet account
   - Check if you have open positions using your balance

4. **Order Placement Failed**:
   - Verify the symbol exists and is tradeable
   - Check minimum order quantities
   - Ensure price and quantity are within valid ranges

### Log Files
Check the `trading_bot.log` file for detailed error information and API responses.

## 📈 Performance Monitoring

The bot tracks several performance metrics:
- Total trades executed
- Successful vs failed trades
- Success rate percentage
- Account balance changes
- Position PnL tracking

View performance metrics in the CLI with the `performance` command or in the web dashboards.

## 🔒 Security Notes

- **API Keys**: Never commit your `.env` file to version control
- **Testnet Only**: This bot is designed for Binance Futures Testnet only
- **Local Use**: The web interfaces run locally and don't expose your API keys
- **Logging**: Be aware that API keys are masked in logs but other sensitive data may be logged

## 📝 License

This project is for educational and testing purposes. Use at your own risk.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your own use.

## ⚠️ Disclaimer

This trading bot is for educational purposes only. Trading cryptocurrencies involves substantial risk of loss. The authors are not responsible for any financial losses. Always test thoroughly on testnet before considering live trading.

---

**Happy Trading! 🚀📈**
