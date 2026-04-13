from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo sayang 😘")

app = ApplicationBuilder().token("8761594910:AAG984I89hleez6DUQ4DK_dbOYrsMeL7FkI").build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
