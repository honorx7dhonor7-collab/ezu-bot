import os
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Salom! Men ishlayapman 😊 Video yubor!")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(m):
    bot.reply_to(m, "Video qabul qilindi! Tez orada tayyorlayman...")

def run_bot():
    print("Bot polling boshlandi...")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
