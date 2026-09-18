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

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Salom! 👋 Men Kling AI kabi video yasaydigan botman!\n\n"
        "🎬 Funksiyalarim:\n"
        "📝 Text to Video - matn yozsang video qilaman\n"
        "🖼️ Image to Video - rasm yuborsang videoga aylantiraman\n\n"
        "Shunchaki matn yoz yoki rasm yubor!\n\n"
        "Muallif: O'g'iloy Mamasidiqova"
    )

# KIM YARATGAN - ASOSIY QISM
@bot.message_handler(func=lambda m: m.text and any(x in m.text.lower() for x in ["kim yaratgan", "seni kim", "кто создал", "who created", "muallifing kim"]))
def who_created(message):
    bot.send_message(message.chat.id, "Meni O'g'iloy Mamasidiqova yaratgan! ❤️")

# TEXT TO VIDEO
@bot.message_handler(func=lambda m: m.text and not m.text.startswith('/') and "kim yaratgan" not in m.text.lower() and "seni kim" not in m.text.lower())
def text_to_video(message):
    prompt = message.text
    bot.send_message(message.chat.id, f"🎬 Prompt qabul qilindi:\n\n'{prompt}'\n\n⏳ Video tayyorlanmoqda... (Kling AI uslubida)")
    # Bu yerda keyin haqiqiy API ulaymiz
    bot.send_message(message.chat.id, "✅ Demo: Hozircha text qabul qilindi. Tez orada haqiqiy video yuboraman!")

# IMAGE TO VIDEO
@bot.message_handler(content_types=['photo'])
def image_to_video(message):
    bot.send_message(message.chat.id, "🖼️ Rasm qabul qilindi!\n\n🎥 Uni Kling AI uslubida videoga aylantirmoqdaman...")
    # Rasmni saqlab olish
    file_info = bot.get_file(message.photo[-1].file_id)
    bot.send_message(message.chat.id, "✅ Demo: Rasm qabul qilindi. Tez orada video versiyasini yuboraman!\n\nMuallif: O'g'iloy Mamasidiqova")

def run_bot():
    print("Bot ishga tushdi...")
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
