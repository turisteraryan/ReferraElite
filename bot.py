import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import types

# Replace with your bot token
API_TOKEN = '7354300058:AAFGSs0Eg-dBu_XZiZsgLa4kUcjpv7TUa68'

# Admin user ID
ADMIN_USER_ID = 1824621252

# Initialize the bot
bot = telebot.TeleBot(API_TOKEN)

# JSON file to store user data
USER_DATA_FILE = 'user_data.json'

# Store broadcast message temporarily
broadcast_message = None

# Welcome bonus configuration
welcome_bonus_amount = 0
welcome_bonus_enabled = False


# Function to load user data from the JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save user data to the JSON file
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to create the main keyboard layout
def create_main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # First row (Create Ad and Surf Bots)
    btn_create_ad = KeyboardButton("📢 Create Ad")
    btn_surf_bots = KeyboardButton("🤖 Surf Bots")
    # Second row (My Ads and My Account)
    btn_my_ads = KeyboardButton("📋 My Ads")
    btn_my_account = KeyboardButton("👤 My Account")
    # Bottom row (Help)
    btn_help = KeyboardButton("❓ Help")
    
    markup.add(btn_create_ad, btn_surf_bots)
    markup.add(btn_my_ads, btn_my_account)
    markup.add(btn_help)
    
    return markup

# Start command handler with a professional welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"🎉 <b>Welcome to ReferraElite, {message.from_user.first_name}!</b> 🎉\n\n"
        "We are the leading platform for generating <b>referrals</b> and promoting your <b>ads</b> effectively.\n\n"
        "🔹 <b>What can you do?</b>\n"
        "• <b>Create Ads</b> to attract referrals and grow your influence.\n"
        "• <b>Surf Bots</b> to explore new bots and earn rewards.\n"
        "• Manage your <b>ads</b> and <b>account</b> efficiently.\n\n"
        "📞 Need assistance with <b>paid promotions</b> or deposits? Contact @DevCodaZenith for support.\n\n"
        "Feel free to explore the bot using the buttons below and start your journey with ReferraElite today.\n\n"
        "🔧 <b>Developed by</b> @CodaZenith"
    )
    
    # Send welcome message with keyboard
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=create_main_menu())

# My Account button handler to show user details and store in JSON
@bot.message_handler(func=lambda message: message.text == "👤 My Account")
def show_account_info(message):
    # Load existing user data
    user_data = load_user_data()

    # Fetch user details
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name or "N/A"
    last_name = message.from_user.last_name or "N/A"
    username = message.from_user.username or "N/A"
    
    # Check if the user exists in the data, otherwise create a new record
    if user_id not in user_data:
        user_data[user_id] = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'points': 0  # New users start with 0 points
        }

    # Update user details in case they changed
    user_data[user_id]['first_name'] = first_name
    user_data[user_id]['last_name'] = last_name
    user_data[user_id]['username'] = username

    # Save the updated user data back to the JSON file
    save_user_data(user_data)

    # Get the user's points
    points = user_data[user_id]['points']

    # Create the response message with user details
    account_info = (
        "<b>👮 Your Account Details</b>\n\n"
        f"<b>👤 First Name:</b> {first_name}\n"
        f"<b>📝 Last Name:</b> {last_name}\n"
        f"<b>🔗 Username:</b> @{username}\n"
        f"<b>🆔 User ID:</b> {user_id}\n"
        f"<b>💎 Points:</b> {points}\n\n"
        "📞 For help or support, contact @DevCodaZenith.\n"
        "🔧 <b>Developed by</b> @CodaZenith"
    )
    
    # Send the account information to the user
    bot.send_message(message.chat.id, account_info, parse_mode="HTML")

# Help button handler to show detailed information
@bot.message_handler(func=lambda message: message.text == "❓ Help")
def send_help(message):
    help_text = (
        "<b>🛠 What is ReferraElite?</b>\n"
        "ReferraElite is a platform designed to help you grow your influence by creating ads, gaining referrals, "
        "and engaging with bots. Whether you're promoting a product, service, or community, ReferraElite offers "
        "an easy way to get the visibility you need.\n\n"
        
        "<b>🔹 How to Use ReferraElite</b>\n"
        "• <b>Create Ads</b>: Tap '📢 Create Ad' to start promoting your content.\n"
        "• <b>Surf Bots</b>: Explore bots via the '🤖 Surf Bots' option to earn rewards and discover new opportunities.\n"
        "• <b>Manage Ads & Account</b>: Use '📋 My Ads' and '👤 My Account' to view your campaigns and monitor your account.\n\n"
        
        "<b>🔧 Commands</b>\n"
        "/start - Display the welcome message\n"
        "/help - Show this help menu\n"
        "/createad - Create a new ad for promotion\n"
        "/surf - Surf and interact with bots\n"
        "/myads - Manage and view your ads\n"
        "/myaccount - Access your account details\n\n"
        
        "<b>📞 Contact for Promotions & Support</b>\n"
        "For any assistance regarding <b>paid promotions</b>, deposits, or technical support, please contact @DevCodaZenith.\n\n"
        
        "<b>© Developed by</b> @CodaZenith"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="HTML")




# Handler for sending points by the admin
@bot.message_handler(commands=['send'])
def send_points(message):
    if message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 You are not authorized to use this command.")
        return

    try:
        # Extract the command arguments
        command_parts = message.text.split()
        if len(command_parts) != 3:
            bot.reply_to(message, "⚠️ Invalid command format. Use /send {username/userid} {amount}.")
            return

        # Get the target username/user ID and the points to send
        target_user = command_parts[1]
        points_to_send = int(command_parts[2])

        # Load existing user data
        user_data = load_user_data()

        # Try to find the user by username or user ID
        target_user_id = None
        target_username = None
        for user_id, user_info in user_data.items():
            if user_info['username'] == target_user or user_id == target_user:
                target_user_id = user_id
                target_username = user_info['username']
                break

        # If the user doesn't exist, send an error to the admin
        if target_user_id is None:
            bot.reply_to(message, f"❌ This user '{target_user}' has not used the bot yet. Please try again later.")
            return

        # Update the user's points balance
        user_data[target_user_id]['points'] += points_to_send
        save_user_data(user_data)

        # Send a confirmation to the admin
        admin_response = (
            f"<b>✅ Successfully sent {points_to_send} points to @{target_username or target_user_id}.</b>\n"
        )
        bot.send_message(message.chat.id, admin_response, parse_mode="HTML")

        # Notify the user about the points received
        user_response = (
            f"🎉 <b>Congratulations! You have received {points_to_send} points.</b>\n"
            "💰 Check your balance by clicking on '👤 My Account'."
        )
        bot.send_message(target_user_id, user_response, parse_mode="HTML")

    except ValueError:
        bot.reply_to(message, "⚠️ Please enter a valid number for points.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred: {str(e)}")

# Handler for removing points by the admin
@bot.message_handler(commands=['remove'])
def remove_points(message):
    if message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 You are not authorized to use this command.")
        return

    try:
        # Extract the command arguments
        command_parts = message.text.split()
        if len(command_parts) != 3:
            bot.reply_to(message, "⚠️ Invalid command format. Use /remove {username/userid} {amount/max}.")
            return

        # Get the target username/user ID and the points to remove
        target_user = command_parts[1]
        points_to_remove = command_parts[2]

        # Load existing user data
        user_data = load_user_data()

        # Try to find the user by username or user ID
        target_user_id = None
        target_username = None
        for user_id, user_info in user_data.items():
            if user_info['username'] == target_user or user_id == target_user:
                target_user_id = user_id
                target_username = user_info['username']
                break

        # If the user doesn't exist, send an error to the admin
        if target_user_id is None:
            bot.reply_to(message, f"❌ This user '{target_user}' has not used the bot yet. Please try again later.")
            return

        # Remove points based on the input
        current_points = user_data[target_user_id]['points']
        if points_to_remove.lower() == 'max':
            # Remove all points
            points_removed = current_points
            user_data[target_user_id]['points'] = 0
        else:
            points_removed = int(points_to_remove)
            if points_removed > current_points:
                bot.reply_to(message, f"⚠️ User @{target_username or target_user_id} doesn't have enough points to remove.")
                return
            # Update the user's points balance
            user_data[target_user_id]['points'] -= points_removed

        save_user_data(user_data)

        # Send a confirmation to the admin
        admin_response = (
            f"<b>✅ Successfully removed {points_removed} points from @{target_username or target_user_id}.</b>\n"
        )
        bot.send_message(message.chat.id, admin_response, parse_mode="HTML")

        # Notify the user about the points removed
        user_response = (
            f"😔 <b>Ohh sorry! Admin has removed {points_removed} points from your account.</b>\n"
            "If you have any questions or concerns, please contact @DevCodaZenith."
        )
        bot.send_message(target_user_id, user_response, parse_mode="HTML")

    except ValueError:
        bot.reply_to(message, "⚠️ Please enter a valid number for points.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred: {str(e)}")

# Handler for the /stats command (admin only)
@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 You are not authorized to use this command.")
        return

    try:
        # Load the user data from the JSON file
        user_data = load_user_data()

        # Calculate the total number of users
        total_users = len(user_data)

        # Admin response with bot stats
        admin_response = (
            f"📊 <b>Bot Statistics</b>\n\n"
            f"👥 <b>Total Users:</b> {total_users}\n"
        )

        bot.send_message(message.chat.id, admin_response, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred: {str(e)}")
    

# Handler for the /broadcast command (admin only)
@bot.message_handler(commands=['broadcast'])
def start_broadcast(message):
    if message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 You are not authorized to use this command.")
        return

    # Ask the admin to send or forward a message
    msg = bot.reply_to(message, "📢 <b>Please send me or forward the message you want to broadcast.</b>", parse_mode="HTML")
    
    # Move to the next step: waiting for the message to broadcast
    bot.register_next_step_handler(msg, get_broadcast_message)

# Function to receive the broadcast message from the admin
def get_broadcast_message(message):
    global broadcast_message
    broadcast_message = message  # Store the message (can be long or forwarded)

    # Confirm the message with the admin
    bot.reply_to(message, "✅ <b>Message received. Starting broadcast...</b>", parse_mode="HTML")

    # Start broadcasting to all users
    broadcast_to_users(broadcast_message)

# Function to broadcast the message to all users
def broadcast_to_users(message):
    global broadcast_message
    successful = 0
    failed = 0
    user_data = load_user_data()  # Load all user data from JSON

    for user_id in user_data:
        try:
            if message.forward_from_chat or message.forward_from:
                # Forwarded message - retain original format and buttons
                sent_msg = bot.forward_message(user_id, message.chat.id, message.message_id)
            else:
                # Regular message - add #PaidPromotion and other info
                msg_text = f"📢 #PaidPromotion\n\n{broadcast_message.text}"
                sent_msg = bot.send_message(user_id, msg_text, parse_mode="HTML")
            
            # Pin the message in user's chat
            bot.pin_chat_message(user_id, sent_msg.message_id)

            # Increment success count
            successful += 1

        except Exception as e:
            # Increment failed count if there's an issue
            failed += 1
            print(f"Failed to send message to user {user_id}: {str(e)}")

    # Show broadcast stats to admin
    show_broadcast_stats(successful, failed)

# Function to show broadcast statistics to the admin
def show_broadcast_stats(successful, failed):
    total = successful + failed

    stats_message = (
        f"📊 <b>Broadcast Details</b>\n\n"
        f"🟢 <b>Successful Broadcasts:</b> {successful}\n"
        f"🔴 <b>Failed Broadcasts:</b> {failed}\n"
        f"📈 <b>Total Users Targeted:</b> {total}\n\n"
        f"🏁 <b>Broadcast Completed!</b>\n"
    )

    bot.send_message(ADMIN_USER_ID, stats_message, parse_mode="HTML")
    



# Welcome bonus configuration
welcome_bonus_amount = 0
welcome_bonus_enabled = False

# Load user data from local JSON
def load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save user data to local JSON
def save_user_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Function to award welcome bonus to new users
def award_welcome_bonus(user_id, first_name):
    global welcome_bonus_amount, welcome_bonus_enabled
    user_data = load_user_data()

    # Check if the user is using the bot for the first time and bonus is enabled
    if welcome_bonus_enabled and user_id not in user_data:
        user_data[user_id] = {
            'first_name': first_name,
            'points': welcome_bonus_amount,
        }
        save_user_data(user_data)

        # Notify the user about their bonus
        bot.send_message(user_id, 
            f"🎉 Congratulations {first_name}! You have received <b>{welcome_bonus_amount} points</b> as a welcome bonus! 🎁\n"
            "Hurry up and explore the bot features!", 
            parse_mode="HTML"
        )

# Admin command to set the welcome bonus amount
@bot.message_handler(commands=['welcome_bonus'])
def handle_welcome_bonus(message):
    if message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 You are not authorized to use this command.")
        return

    # Parse the command input
    command = message.text.split()

    if len(command) == 2 and command[1].isdigit():
        global welcome_bonus_amount
        welcome_bonus_amount = int(command[1])
        bot.reply_to(message, f"🎁 Welcome bonus set to {welcome_bonus_amount} points.", parse_mode="HTML")

    elif len(command) == 2 and command[1].lower() == 'on':
        global welcome_bonus_enabled
        welcome_bonus_enabled = True
        bot.reply_to(message, "🎁 Welcome bonus is now <b>enabled</b>.", parse_mode="HTML")

    elif len(command) == 2 and command[1].lower() == 'off':
        welcome_bonus_enabled = False
        bot.reply_to(message, "🎁 Welcome bonus is now <b>disabled</b>.", parse_mode="HTML")

    else:
        bot.reply_to(message, "⚠️ Invalid command format. Use `/welcome_bonus {amount}` to set points or `/welcome_bonus on/off` to toggle the feature.", parse_mode="HTML")

# Start command handler for new users
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # Load user data and award welcome bonus if applicable
    award_welcome_bonus(user_id, first_name)

    # Load user info
    user_data = load_user_data()

    if user_id not in user_data:
        user_data[user_id] = {
            'first_name': first_name,
            'points': 0,  # Initial points if no bonus applied
        }
        save_user_data(user_data)

    # Send welcome message
    welcome_text = (
        f"🎉 <b>Welcome to ReferraElite, {message.from_user.first_name}!</b> 🎉\n\n"
        "We are the leading platform for generating <b>referrals</b> and promoting your <b>ads</b> effectively.\n\n"
        "🔹 <b>What can you do?</b>\n"
        "• <b>Create Ads</b> to attract referrals and grow your influence.\n"
        "• <b>Surf Bots</b> to explore new bots and earn rewards.\n"
        "• Manage your <b>ads</b> and <b>account</b> efficiently.\n\n"
        "📞 Need assistance with <b>paid promotions</b> or deposits? Contact @DevCodaZenith for support.\n\n"
        "Feel free to explore the bot using the buttons below and start your journey with ReferraElite today.\n\n"
        "🔧 <b>Developed by</b> @CodaZenith"
    )

    bot.reply_to(message, welcome_text, parse_mode="HTML")
    
@bot.message_handler(commands=['update'])
def handle_update(message):
    if message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 You are not authorized to use this command.")
        return

    # Ask the admin for the update message
    update_text = message.text[7:].strip()  # Get text after /update command

    if not update_text:
        bot.reply_to(message, "⚠️ Please provide an update message after the command.")
        return

    # Load user data
    user_data = load_user_data()
    successful_sends = 0
    failed_sends = 0

    for user_id, user_info in user_data.items():
        try:
            # Send the update message to each user
            bot.send_message(user_id, 
                f"📢 <b>Update Notification:</b>\n\n{update_text}", 
                parse_mode="HTML"
            )
            # Pin the message (This will work only in groups/channels, not in private chats)
            # Uncomment below line if you are sending messages in a group
            # bot.pin_chat_message(chat_id=user_id, message_id=message_id)

            successful_sends += 1
        except Exception as e:
            failed_sends += 1
            print(f"Failed to send message to {user_id}: {e}")

    # Prepare and send the status report to the admin
    status_report = (
        f"✅ Successfully sent updates to <b>{successful_sends}</b> users.\n"
        f"❌ Failed to send updates to <b>{failed_sends}</b> users."
    )
    bot.reply_to(message, status_report, parse_mode="HTML")
    


# Polling for new messages
bot.polling()
  
