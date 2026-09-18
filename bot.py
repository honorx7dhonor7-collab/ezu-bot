import telebot
TOKEN = "8916374024:AAFKfOteBoAUC7LoYU1ear0ZToe_YKaXrus"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m): bot.send_message(m.chat.id, "Ishlayapti! Muallif: O'g'iloy Mamasidiqova")

@bot.message_handler(func=lambda m: "kim yaratgan" in m.text.lower() if m.text else False)
def who(m): bot.send_message(m.chat.id, "Meni O'g'iloy Mamasidiqova yaratgan!")

@bot.message_handler(content_types=['photo'])
def img(m): bot.send_message(m.chat.id, "Rasm qabul qilindi - Image to Video!")

@bot.message_handler(content_types=['text'])
def txt(m): bot.send_message(m.chat.id, f"Text qabul qilindi - Text to Video: {m.text}")

bot.remove_webhook()
print("Bot polling boshlandi...")
bot.infinity_polling()
