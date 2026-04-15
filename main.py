import telebot
import os
import json
import time
from telebot import types

TOKEN = os.getenv("TOKEN_BOT")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# ================= LOAD & SAVE =================
def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ================= KEYBOARD =================
def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📄 Menu Utama")
    btn2 = types.KeyboardButton("🎁 Claim Saldo")
    btn3 = types.KeyboardButton("💰 Saldo")
    btn4 = types.KeyboardButton("💸 Deposit")
    btn5 = types.KeyboardButton("👑 Panel Admin")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    return markup

# ================= START =================
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

    menu(message)

# ================= MENU FUNCTION =================
def menu(message):
    users = load_users()
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "username": message.from_user.username,
            "saldo": 0,
            "last_claim": 0
        }
        save_users(users)

    username = users[user_id].get("username") or "-"
    nama = message.from_user.first_name
    saldo = users[user_id].get("saldo", 0)
    total_user = len(users)

    teks = f"""
👤 *INFO AKUN KAMU*

Halo {nama} 👋

🆔 ID : `{user_id}`
👤 Username : @{username}

💰 Saldo : Rp {saldo}
📊 Total User : {total_user}

—————————————
Silakan pilih menu di bawah ya 😘
"""

    bot.send_message(
        message.chat.id,
        teks,
        parse_mode="Markdown",
        reply_markup=menu_keyboard()
    )

# ================= ADD SALDO (ADMIN) =================
@bot.message_handler(commands=['addsaldo'])
def add_saldo(message):
    ADMIN_ID = 6509182985

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Kamu bukan admin")
        return

    try:
        _, target_id, jumlah = message.text.split()

        users = load_users()

        if target_id not in users:
            bot.reply_to(message, "User tidak ditemukan")
            return

        users[target_id]["saldo"] += int(jumlah)
        save_users(users)

        bot.reply_to(message, f"✅ Berhasil tambah saldo Rp {jumlah}")

        bot.send_message(
            target_id,
            f"💰 Deposit berhasil!\nSaldo kamu sekarang: Rp {users[target_id]['saldo']}"
        )

    except:
        bot.reply_to(message, "Format salah!\nContoh: /addsaldo 123456789 10000")

# ================= HANDLE BUTTON =================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()

    # biar command gak ganggu
    if text.startswith("/"):
        return

    users = load_users()
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "username": message.from_user.username,
            "saldo": 0,
            "last_claim": 0
        }
        save_users(users)

    # ===== MENU =====
    if "Menu Utama" in text:
        menu(message)

    # ===== DEPOSIT =====
    elif "Deposit" in text:
        bot.send_message(
            message.chat.id,
            """
💸 *DEPOSIT SALDO*

Silakan transfer ke:

🏦 DANA : 08xxxxxxxxxx
🏦 OVO  : 08xxxxxxxxxx

📌 Minimal deposit: Rp 5.000

Setelah transfer, kirim bukti ke admin ya 😘
""",
            parse_mode="Markdown"
        )

    # ===== CLAIM =====
    elif "Claim Saldo" in text:
        now = int(time.time())
        last_claim = users[user_id].get("last_claim", 0)

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

        menu(message)

    # ===== SALDO =====
    elif "Saldo" in text:
        saldo = users[user_id].get("saldo", 0)

        bot.send_message(
            message.chat.id,
            f"💰 Saldo kamu: Rp {saldo}"
        )

    # ===== ADMIN PANEL =====
    elif "Panel Admin" in text:
        bot.send_message(
            message.chat.id,
            "👑 Kamu admin ya 😏"
        )

# ================= RUN =================
bot.infinity_polling()
