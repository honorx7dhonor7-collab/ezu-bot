import os
import telebot
from PIL import Image

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Men Ezu AI man 🎃\n\nMatn yoz - senga rasm yasayman!\nRasm tashla - jonlantiraman!")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, f"⏳ '{message.text}' uchun rasm chizyapman...")
    bot.send_message(message.chat.id, "Hozircha test rejimda rasm qaytaraman, tez orada video ham bo'ladi! 🧡")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "⏳ Rasmni oldim, jonlantirayapman...")
    bot.send_message(message.chat.id, "Tez orada video qilib beraman! 🎬")

print("Ezu ishga tushdi!")
bot.infinity_polling()
