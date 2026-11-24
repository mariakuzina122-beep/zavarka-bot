
import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "☕ Добро пожаловать в ЗАВАРКУ!\n\n"
        "Здесь ты найдёшь интересные знакомства.\n\n"
        "Нажми /profile, чтобы создать анкету."
    )

@bot.message_handler(commands=['profile'])
def profile(message):
    bot.send_message(
        message.chat.id,
        "❤️ Давай создадим твою анкету!\n\n"
        "Напиши своё имя:"
    )

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(
        message.chat.id,
        "☕ Заварка уже работает! Скоро здесь появятся новые знакомства."
    )

bot.infinity_polling()
