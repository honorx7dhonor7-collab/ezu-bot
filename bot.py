import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from flask import Flask
import threading

TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

async def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        await message.answer("Salom! Men EzuAiVideoRobot man! Qoyil! 🎉")

    await dp.start_polling(bot)

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(start_bot())
