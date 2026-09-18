import os, telebot, threading, time, io, json
from flask import Flask
from PIL import Image, ImageDraw
import numpy as np, imageio
from gtts import gTTS

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 8481826465
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
DB="/tmp/db.json"
DATA={}

def load(): return json.load(open(DB)) if os.path.exists(DB) else {}
def save(d): json.dump(d, open(DB,'w'))
def can(uid):
    if int(uid)==OWNER_ID: return True
    return load().get(str(uid),0) < 3
def use(uid):
    if int(uid)==OWNER_ID: return
    db=load(); db[str(uid)]=db.get(str(uid),0)+1; save(db)

@app.route('/')
def h(): return "Alive"

@bot.message_handler(commands=['start'])
def start(m):
    DATA[m.from_user.id]={'step':1}
    if m.from_user.id==OWNER_ID:
        left="♾️ Sizda cheksiz! Xo'jayin 👑"
    else:
        used=load().get(str(m.from_user.id),0)
        left=f"🎁 Sizda {3-used} ta bepul urinish qoldi"
    bot.send_message(m.chat.id, f"""Salom! 👋

Men O'g'iloy Mamasidiqova tomonidan yaratildim! ✨

Men buyumlar, mevalar, hayvonlar va mult obrazdagi odamlarning tayyor rasmini jonlantirib, gapirtirib beraman! 🎬

Menga tayyor rasm jo'nating! 📸

{left}""")

@bot.message_handler(content_types=['photo'])
def p(m):
    if not can(m.from_user.id):
        bot.send_message(m.chat.id, f"""😔 Bepul urinishlar tugadi!

💰 Narxlar:
🎬 1 ta video - 5 000 so'm
🎬 5 ta video - 20 000 so'm
♾️ 1 oy cheksiz - 50 000 so'm

To'lov uchun 👉 @eeuuzzo ga yozing!""")
        return
    DATA[m.from_user.id]={'photo':m.photo[-1].file_id, 'step':2}
    bot.send_message(m.chat.id, "Qabul qildim! ✅\n\n2️⃣ Endi rasm nima desin? Matn yozing! ✍️")

@bot.message_handler(content_types=['text'])
def t(m):
    if m.text.startswith('/'): return
    if m.from_user.id not in DATA or DATA[m.from_user.id].get('step')!=2:
        bot.send_message(m.chat.id, "Avval tayyor rasm jo'nating! 1️⃣"); return
    DATA[m.from_user.id]['text']=m.text; DATA[m.from_user.id]['step']=3
    kb=telebot.types.InlineKeyboardMarkup(row_width=3)
    kb.add(
        telebot.types.InlineKeyboardButton("📱 9:16", callback_data="9:16"),
        telebot.types.InlineKeyboardButton("🎬 16:9", callback_data="16:9"),
        telebot.types.InlineKeyboardButton("⬜ 1:1", callback_data="1:1")
    )
    bot.send_message(m.chat.id, "3️⃣ Format tanlang! 👇", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    d=c.data
    if c.from_user.id
