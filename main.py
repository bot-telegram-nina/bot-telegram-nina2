import telebot
import os
import json
from telebot import types

TOKEN = os.getenv("TOKEN_BOT")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# ========================
# LOAD & SAVE DATA
# ========================
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ========================
# KEYBOARD MENU
# ========================
def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📄 Menu Utama")
    btn2 = types.KeyboardButton("🎁 Claim Saldo")
    btn3 = types.KeyboardButton("👑 Panel Admin")

    markup.add(btn1, btn2)
    markup.add(btn3)

    return markup

# ========================
# START COMMAND
# ========================
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

    bot.send_message(
        message.chat.id,
        "Halo sayang 😘 Bot kamu sudah aktif!",
        reply_markup=menu_keyboard()
    )

# ========================
# MENU COMMAND
# ========================
@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(
        message.chat.id,
        "Pilih menu di bawah ya 😚",
        reply_markup=menu_keyboard()
    )

# ========================
# HANDLE BUTTON
# ========================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text

    if text == "📄 Menu Utama":
        bot.send_message(message.chat.id, "Ini menu utama 😏")

    elif text == "🎁 Claim Saldo":
        bot.send_message(message.chat.id, "Saldo berhasil diklaim 💰")

    elif text == "👑 Panel Admin":
        bot.send_message(message.chat.id, "Akses admin 😎")

    else:
        bot.send_message(message.chat.id, "Pakai tombol yang ada ya 😒")

# ========================
# RUN BOT
# ========================
bot.infinity_polling()
