import os
from flask import Flask
import telebot
import threading

TOKEN = os.environ.get("BOT_TOKEN") or "8916374024:AAFKfOteBoAUC7LoYU1ear0ZToe_YKaXrus"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti! O'g'iloy Mamasidiqova yaratgan"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Salom! 👋\n📝 Text to Video - matn yoz\n🖼️ Image to Video - rasm yubor\n\nMuallif: O'g'iloy Mamasidiqova")

@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ["kim yaratgan", "seni kim", "кто создал", "who created"]))
def who_created(message):
    bot.send_message(message.chat.id, "Meni O'g'iloy Mamasidiqova yaratgan! ❤️")

@bot.message_handler(content_types=['photo'])
def image_to_video(message):
    bot.send_message(message.chat.id, "🖼️ Rasm qabul qilindi! Videoga aylantirmoqdaman...")

@bot.message_handler(func=lambda m: True, content_types=['text'])
def text_to_video(message):
    if message.text.startswith('/'): return
    bot.send_message(message.chat.id, f"🎬 Prompt: '{message.text}'\n⏳ Video tayyorlanmoqda...")

# MANA SHU OXIRGI QATORLAR - ENG MUHIM JOYI!
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    bot.remove_webhook()
    print("Webhook o'chirildi, bot ishga tushdi...")
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling(skip_pending=True)
