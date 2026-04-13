import telebot
import os

TOKEN = os.getenv("TOKEN_BOT")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def awal(message):
    bot.reply_to(message, "Halo sayang 😘 bot aktif nih")

@bot.message_handler(func=lambda message: True)
def gema(message):
    bot.reply_to(message, message.text)

print("Bot jalan...")
bot.infinity_polling()
