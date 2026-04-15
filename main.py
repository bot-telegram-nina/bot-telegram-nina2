import telebot
import os
import json
import time
from telebot import types

TOKEN = os.getenv("TOKEN_BOT")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# ================================
# LOAD & SAVE
# ================================
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ================================
# KEYBOARD
# ================================
def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📋 Menu Utama")
    btn2 = types.KeyboardButton("🎁 Claim Saldo")
    btn3 = types.KeyboardButton("👑 Panel Admin")

    markup.add(btn1, btn2)
    markup.add(btn3)

    return markup

# ================================
# START
# ================================
@bot.message_handler(commands=['start'])
def start(message):
    users = load_users()
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "username": message.from_user.username,
            "saldo": 0,
            "last_claim": 0
        }
        save_users(users)

    bot.send_message(
        message.chat.id,
        "Halo sayang 😘 Bot kamu sudah aktif!",
        reply_markup=menu_keyboard()
    )

# ================================
# MENU COMMAND
# ================================
@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(
        message.chat.id,
        "Pilih menu ya sayang 😘",
        reply_markup=menu_keyboard()
    )

# ================================
# HANDLE BUTTON
# ================================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text

    if text == "📋 Menu Utama":
        bot.send_message(message.chat.id, "Ini Menu Utama kamu 😘")

    elif text == "🎁 Claim Saldo":
        users = load_users()
        user_id = str(message.from_user.id)
        now = int(time.time())

        last_claim = users.get(user_id, {}).get("last_claim", 0)

        if now - last_claim < 86400:
            sisa = 86400 - (now - last_claim)
            jam = sisa // 3600
            menit = (sisa % 3600) // 60

            bot.send_message(
                message.chat.id,
                f"⏳ Tunggu ya {jam} jam {menit} menit lagi 😘"
            )
            return

        reward = 200

        users[user_id]["saldo"] += reward
        users[user_id]["last_claim"] = now
        save_users(users)

        bot.send_message(
            message.chat.id,
            f"🎁 Kamu dapat {reward} saldo! 💰"
        )

    elif text == "👑 Panel Admin":
        bot.send_message(message.chat.id, "Kamu admin ya 😏")

    elif text == "/saldo":
        users = load_users()
        user_id = str(message.from_user.id)

        saldo = users.get(user_id, {}).get("saldo", 0)

        bot.send_message(
            message.chat.id,
            f"Saldo kamu: Rp {saldo}"
        )

# ================================
# RUN BOT
# ================================
bot.infinity_polling()
