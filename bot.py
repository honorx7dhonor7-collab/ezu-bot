import os, telebot, threading, time, io, json
from flask import Flask
from PIL import Image
import numpy as np, imageio

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
DATA = {}

@app.route('/')
def home():
    return "Alive"

@bot.message_handler(commands=['start'])
def start(m):
    DATA[m.from_user.id] = {'step':1}
    msg = "Salom!\n\nMen Ogiloy Mamasidiqova tomonidan yaratildim!\n\nMen buyumlar, mevalar, hayvonlar va mult obrazdagi odamlarning tayyor rasmini jonlantirib beraman!\n\nMenga tayyor rasm jonating!"
    bot.send_message(m.chat.id, msg)

@bot.message_handler(content_types=['photo'])
def ph(m):
    DATA[m.from_user.id] = {'photo': m.photo[-1].file_id, 'step':2}
    bot.send_message(m.chat.id, "Qabul qildim! Endi rasm nima desin? Yozing!")

@bot.message_handler(content_types=['text'])
def tx(m):
    if m.text.startswith('/'):
        return
    if m.from_user.id not in DATA:
        return
    if DATA[m.from_user.id].get('step')!= 2:
        return
    DATA[m.from_user.id]['text'] = m.text
    DATA[m.from_user.id]['step'] = 3
    kb = telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton("9:16", callback_data="9:16"))
    kb.add(telebot.types.InlineKeyboardButton("16:9", callback_data="16:9"))
    kb.add(telebot.types.InlineKeyboardButton("1:1", callback_data="1:1"))
    bot.send_message(m.chat.id, "Format tanlang!", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    d = c.data
    uid = c.from_user.id
    if uid not in DATA:
        return
    if d == "9:16" or d == "16:9" or d == "1:1":
        DATA[uid]['format'] = d
        kb = telebot.types.InlineKeyboardMarkup()
        kb.add(telebot.types.InlineKeyboardButton("VIDEO", callback_data="go"))
        bot.edit_message_text("Tanlandi: " + d, c.message.chat.id, c.message.message_id, reply_markup=kb)
    if d == "go":
        info = DATA.get(uid)
        bot.edit_message_text("Jonlantiryapman...", c.message.chat.id, c.message.message_id)
        try:
            f = bot.get_file(info['photo'])
            data = bot.download_file(f.file_path)
            base = Image.open(io.BytesIO(data)).convert("RGB")
            fmt = info['format']
            if fmt == "9:16":
                w = 720
                h = 1280
            elif fmt == "16:9":
                w = 1280
                h = 720
            else:
                w = 720
                h = 720
            base = base.resize((w, h))
            writer = imageio.get_writer("/tmp/out.mp4", fps=12, macro_block_size=1)
            for i in range(60):
                zoom = 1 + 0.03 * np.sin(i * 0.2)
                nw = int(w * zoom)
                nh = int(h * zoom)
                tmp = base.resize((nw, nh))
                l = (nw - w) // 2
                t = (nh - h) // 2
                fr = tmp.crop((l, t, l+w, t+h))
                writer.append_data(np.array(fr))
            writer.close()
            with open("/tmp/out.mp4", 'rb') as v:
                bot.send_video(c.message.chat.id, v, caption="Tayyor!")
            DATA.pop(uid, None)
        except Exception as e:
            bot.send_message(c.message.chat.id, "Xato: " + str(e))

def run():
    time.sleep(2)
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
