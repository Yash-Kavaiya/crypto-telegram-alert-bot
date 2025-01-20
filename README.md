# Cryptocurrency Price Alert Telegram Bot 🚀

A powerful and flexible Telegram bot for tracking cryptocurrency price movements and receiving customized alerts. Monitor multiple cryptocurrencies simultaneously with automated percentage-based price change notifications.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Telegram](https://img.shields.io/badge/telegram-bot-blue.svg)

## 📚 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Command Reference](#command-reference)
- [Architecture](#architecture)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Real-time Price Tracking**: Monitors cryptocurrency prices using CoinGecko API
- **Customizable Alerts**: Automated notifications for price changes at 5% intervals (5% to 100%)
- **Multi-Cryptocurrency Support**: Track multiple cryptocurrencies simultaneously
- **Bi-directional Alerts**: Notifications for both price increases and decreases
- **Smart Alert Management**: Automatic cleanup of completed alerts
- **User-friendly Commands**: Intuitive interface for managing tracked cryptocurrencies
- **Robust Error Handling**: Graceful handling of API failures and network issues

## 🛠 Prerequisites

- Python 3.7 or higher
- Telegram account
- Internet connection
- Basic understanding of cryptocurrency markets

## 📥 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/crypto-alert-bot.git
cd crypto-alert-bot
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
```

3. **Install Dependencies**
```bash
pip install python-telegram-bot aiohttp
```

## ⚙️ Configuration

### 1. Get Your Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Start a chat and use the `/newbot` command
3. Follow the prompts to create your bot
4. Copy the provided API token

### 2. Configure the Bot

1. Open `bot.py`
2. Replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual token:
```python
TOKEN = "your_token_here"
```

## 🚀 Usage

1. **Start the Bot**
```bash
python bot.py
```

2. **Initial Setup**
- Open Telegram
- Search for your bot using the username you created
- Start a conversation with `/start`

## 💬 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize bot and show welcome message | `/start` |
| `/track` | Begin tracking a cryptocurrency | `/track bitcoin` |
| `/alerts` | View all active alerts | `/alerts` |
| `/remove` | Stop tracking a cryptocurrency | `/remove bitcoin` |
| `/help` | Display help information | `/help` |

## 🏗 Architecture

### Components

1. **Main Bot Application**
```python
def main():
    application = Application.builder().token(TOKEN).build()
    # Command handlers and background tasks setup
```

2. **Price Tracking System**
```python
async def fetch_crypto_price(crypto_id):
    # CoinGecko API integration
    # Price fetching logic
```

3. **Alert Management**
```python
async def check_alerts():
    # Background task for monitoring prices
    # Alert triggering system
```

### Data Structure

```python
user_alerts = {
    user_id: {
        crypto_id: {
            "initial_price": float,
            "alerts": [percentages]
        }
    }
}
```

## 🛡 Error Handling

The bot implements comprehensive error handling for:

- API failures
- Network connectivity issues
- Invalid cryptocurrency IDs
- User input validation
- Message delivery failures

Example:
```python
try:
    async with session.get(url, params=params) as response:
        if response.status == 200:
            # Process successful response
except Exception as e:
    logger.error(f"Error fetching price: {e}")
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch
```bash
git checkout -b feature/YourFeature
```
3. Commit your changes
```bash
git commit -m 'Add some feature'
```
4. Push to the branch
```bash
git push origin feature/YourFeature
```
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 Troubleshooting

Common issues and solutions:

1. **Bot Not Responding**
   - Verify your internet connection
   - Check if the bot token is correct
   - Ensure Python version compatibility

2. **Price Updates Not Working**
   - Check CoinGecko API status
   - Verify cryptocurrency ID spelling
   - Confirm network connectivity

3. **Alert Delays**
   - Default check interval is 60 seconds
   - Adjust `asyncio.sleep(60)` value if needed

## 📮 Support

For support and questions:
- Open an issue in the GitHub repository
- Contact the maintainers
- Check the [Telegram Bot API documentation](https://core.telegram.org/bots/api)

---

**Note**: This bot uses the free CoinGecko API, which has rate limits. For production use, consider obtaining an API key or implementing rate limiting mechanisms.

Remember to star ⭐ the repository if you find it helpful!
