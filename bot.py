import os, telebot, threading
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN") or "8916374024:AAFKfOteBoAUC7LoYU1ear0ZToe_YKaXrus"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Bot Ishlayapti! O'g'iloy Mamasidiqova"

@bot.message_handler(commands=['start'])
def start(m): bot.send_message(m.chat.id, "Salom! Text yoki Rasm yubor! Muallif: O'g'iloy Mamasidiqova")

@bot.message_handler(func=lambda m: m.text and "kim yaratgan" in m.text.lower())
def who(m): bot.send_message(m.chat.id, "Meni O'g'iloy Mamasidiqova yaratgan! ❤️")

@bot.message_handler(content_types=['photo'])
def img(m): bot.send_message(m.chat.id, "🖼️ Image to Video qabul qilindi!")

@bot.message_handler(content_types=['text'])
def txt(m):
    if m.text.startswith('/'): return
    bot.send_message(m.chat.id, f"📝 Text to Video: {m.text}")

def run_bot():
    bot.remove_webhook()
    print("BOT POLLING BOSHLANDI...")
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Flask {port} da ochilmoqda...")
    app.run(host="0.0.0.0", port=port)
