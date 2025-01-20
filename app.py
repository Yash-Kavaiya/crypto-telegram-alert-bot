import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import aiohttp
import asyncio
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Store user alerts
# Format: {user_id: {crypto_id: {"initial_price": price, "alerts": [percentages]}}}
user_alerts = {}

async def fetch_crypto_price(crypto_id):
    """Fetch current price of a cryptocurrency using CoinGecko API."""
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": crypto_id,
        "vs_currencies": "usd"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data[crypto_id]["usd"]
                else:
                    return None
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = (
        "Welcome to the Crypto Price Alert Bot! 🚀\n\n"
        "Commands:\n"
        "/track <crypto_id> - Start tracking a cryptocurrency\n"
        "/alerts - View your active alerts\n"
        "/remove <crypto_id> - Stop tracking a cryptocurrency\n"
        "/help - Show this help message\n\n"
        "Example: /track bitcoin"
    )
    await update.message.reply_text(welcome_message)

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start tracking a cryptocurrency."""
    if not context.args:
        await update.message.reply_text("Please provide a cryptocurrency ID.\nExample: /track bitcoin")
        return

    crypto_id = context.args[0].lower()
    user_id = update.effective_user.id
    
    # Fetch initial price
    initial_price = await fetch_crypto_price(crypto_id)
    if initial_price is None:
        await update.message.reply_text(f"Could not find cryptocurrency with ID: {crypto_id}")
        return
    
    # Set up alerts for 5% intervals up to 100%
    alert_percentages = list(range(5, 101, 5))
    
    if user_id not in user_alerts:
        user_alerts[user_id] = {}
    
    user_alerts[user_id][crypto_id] = {
        "initial_price": initial_price,
        "alerts": alert_percentages
    }
    
    await update.message.reply_text(
        f"Now tracking {crypto_id}!\n"
        f"Initial price: ${initial_price:,.2f}\n"
        f"You will receive alerts at these percentage changes: {', '.join(map(str, alert_percentages))}%"
    )

async def check_alerts():
    """Background task to check price changes and send alerts."""
    while True:
        for user_id, cryptos in user_alerts.copy().items():
            for crypto_id, data in cryptos.copy().items():
                current_price = await fetch_crypto_price(crypto_id)
                if current_price is None:
                    continue
                
                initial_price = data["initial_price"]
                percentage_change = ((current_price - initial_price) / initial_price) * 100
                
                # Check both positive and negative changes
                abs_change = abs(percentage_change)
                change_direction = "increased" if percentage_change > 0 else "decreased"
                
                remaining_alerts = []
                for alert_percentage in data["alerts"]:
                    if abs_change >= alert_percentage:
                        try:
                            await application.bot.send_message(
                                user_id,
                                f"🚨 Alert for {crypto_id}!\n"
                                f"Price has {change_direction} by {abs_change:.2f}%\n"
                                f"Initial price: ${initial_price:,.2f}\n"
                                f"Current price: ${current_price:,.2f}"
                            )
                        except Exception as e:
                            logger.error(f"Error sending alert: {e}")
                    else:
                        remaining_alerts.append(alert_percentage)
                
                # Update remaining alerts
                user_alerts[user_id][crypto_id]["alerts"] = remaining_alerts
                
                # Remove tracking if no alerts remain
                if not remaining_alerts:
                    del user_alerts[user_id][crypto_id]
                    if not user_alerts[user_id]:
                        del user_alerts[user_id]
                    try:
                        await application.bot.send_message(
                            user_id,
                            f"All alerts completed for {crypto_id}. Tracking stopped."
                        )
                    except Exception as e:
                        logger.error(f"Error sending completion message: {e}")
        
        await asyncio.sleep(60)  # Check every minute

async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's active alerts."""
    user_id = update.effective_user.id
    if user_id not in user_alerts or not user_alerts[user_id]:
        await update.message.reply_text("You have no active alerts.")
        return
    
    message = "Your active alerts:\n\n"
    for crypto_id, data in user_alerts[user_id].items():
        current_price = await fetch_crypto_price(crypto_id)
        if current_price is None:
            current_price = "Unable to fetch"
        
        message += (
            f"🪙 {crypto_id.upper()}\n"
            f"Initial price: ${data['initial_price']:,.2f}\n"
            f"Current price: ${current_price:,.2f}\n"
            f"Remaining alerts at: {', '.join(map(str, data['alerts']))}%\n\n"
        )
    
    await update.message.reply_text(message)

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop tracking a cryptocurrency."""
    if not context.args:
        await update.message.reply_text("Please provide a cryptocurrency ID.\nExample: /remove bitcoin")
        return

    crypto_id = context.args[0].lower()
    user_id = update.effective_user.id
    
    if user_id in user_alerts and crypto_id in user_alerts[user_id]:
        del user_alerts[user_id][crypto_id]
        if not user_alerts[user_id]:
            del user_alerts[user_id]
        await update.message.reply_text(f"Stopped tracking {crypto_id}")
    else:
        await update.message.reply_text(f"You are not tracking {crypto_id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await start(update, context)

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    global application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("track", track))
    application.add_handler(CommandHandler("alerts", alerts))
    application.add_handler(CommandHandler("remove", remove))

    # Start the background task
    application.create_task(check_alerts())

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
