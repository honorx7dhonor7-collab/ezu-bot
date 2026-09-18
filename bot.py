import os, telebot, threading, time, io, json
from flask import Flask
from PIL import Image, ImageDraw
import numpy as np, imageio
from gtts import gTTS

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 8481826465
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
DB = "/tmp/db.json"
DATA = {}

def load():
    if os.path.exists(DB):
        with open(DB, 'r') as f:
            return json.load(f)
    return {}

def save(d):
    with open(DB, 'w') as f:
        json.dump(f, d)

def can(uid):
    if int(uid) == OWNER_ID:
        return True
    db = load()
    return db.get(str(uid), 0) < 3

def use(uid):
    if int(uid) == OWNER_ID:
        return
    db = load()
    db[str(uid)] = db.get(str(uid), 0) + 1
    save(db)

@app.route('/')
def h():
    return "Alive"

@bot.message_handler(commands=['start'])
def start(m):
    DATA[m.from_user.id] = {'step': 1}
    if m.from_user.id == OWNER_ID:
        left = "Cheksiz! Xo'jayin"
    else:
        used = load().get(str(m.from_user.id), 0)
        left = f"Sizda {3-used} ta bepul urinish qoldi"
    text = f"Salom! \n\nMen O'g'iloy Mamasidiqova tomonidan yaratildim!\n\nMen buyumlar, mevalar, hayvonlar va mult obrazdagi odamlarning tayyor rasmini jonlantirib, gapirtirib beraman!\n\nMenga tayyor rasm jo'nating!\n\n{left}"
    bot.send_message(m.chat.id, text)

@bot.message_handler(content_types=['photo'])
def photo_handler(m):
    if not can(m.from_user.id):
        bot.send_message(m.chat.id, "Bepul urinishlar tugadi! Tolov uchun @eeuuzzo ga yozing!")
        return
    DATA[m.from_user.id] = {'photo': m.photo[-1].file_id, 'step': 2}
    bot.send_message(m.chat.id, "Qabul qildim! Endi rasm nima desin? Matn yozing!")

@bot.message_handler(content_types=['text'])
def text_handler(m):
    if m.text.startswith('/'):
        return
    if m.from_user.id not in DATA:
        bot.send_message(m.chat.id, "Avval tayyor rasm jo'nating!")
        return
    if DATA[m.from_user.id].get('step') != 2:
        bot.send_message(m.chat.id, "Avval tayyor rasm jo'nating!")
        return
    DATA[m.from_user.id]['text'] = m.text
    DATA[m.from_user.id]['step'] = 3
    kb = telebot.types.InlineKeyboardMarkup(row_width=3)
    kb.add(
        telebot.types.InlineKeyboardButton("9:16", callback_data="9:16"),
        telebot.types.InlineKeyboardButton("16:9", callback_data="16:9"),
        telebot.types.InlineKeyboardButton("1:1", callback_data="1:1")
    )
    bot.send_message(m.chat.id, "Format tanlang!", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: True)
def callback_handler(c):
    d = c.data
    if c.from_user.id not in DATA:
        return
    if d == "9:16" or d == "16:9" or d == "1:1":
        DATA[c.from_user.id]['format'] = d
        kb = telebot.types.InlineKeyboardMarkup()
        kb.add(telebot.types.InlineKeyboardButton("VIDEO GENERATSIYA", callback_data="generate"))
        bot.edit_message_text(f"{d} tanlandi! Tayyor bo'lsangiz bosing!", c.message.chat
