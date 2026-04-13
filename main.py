import telebot
import os
import json

TOKEN = os.getenv("TOKEN_BOT")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# Load data
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save data
def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Start
@bot.message_handler(commands=['start'])
def start(message):
    users = load_users()
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "username": message.from_user.username,
            "saldo": 0
        }
        save_users(users)

    bot.reply_to(message, "Halo sayang 😘 Bot kamu udah makin pintar sekarang!")

# Menu
@bot.message_handler(commands=['menu'])
def menu(message):
    teks = """
Halo sayang 😘

Menu:
- /saldo
- /about
"""
    bot.reply_to(message, teks)

# Saldo
@bot.message_handler(commands=['saldo'])
def saldo(message):
    users = load_users()
    user_id = str(message.from_user.id)

    saldo = users.get(user_id, {}).get("saldo", 0)

    bot.reply_to(message, f"Saldo kamu: Rp {saldo}")

# About
@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message, "Ini bot buatan kita berdua 😘🔥")

# Auto reply
@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.reply_to(message, "Aku denger kok sayang 😘")

print("Bot jalan...")
bot.infinity_polling()
