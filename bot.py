from flask import Flask
import threading, os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. WEB SERVER - Render uchun
app = Flask(__name__)
@app.route('/')
def home(): return "Ezu Bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask).start()

# 2. TELEGRAM BOT
TOKEN = os.environ.get("BOT_TOKEN") # Render Environment ga BOT_TOKEN ni qoygan bo'lishing kerak
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salom! Bot ishlayapti! ✅")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
