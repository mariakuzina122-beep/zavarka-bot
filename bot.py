
import telebot
from telebot import types
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

users = {}

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("❤️ Создать анкету")
    keyboard.add("🔎 Смотреть анкеты")
    keyboard.add("ℹ️ О проекте")

    bot.send_message(
        message.chat.id,
        "☕ Добро пожаловать в ЗАВАРКУ!\n\n"
        "Знакомства по-московски: без лишней воды ❤️",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda m: m.text == "❤️ Создать анкету")
def create_profile(message):
    bot.send_message(message.chat.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    users[message.chat.id] = {"name": message.text}
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    if not message.text.isdigit() or not 18 <= int(message.text) <= 99:
        bot.send_message(message.chat.id, "Укажи возраст от 18 до 99.")
        bot.register_next_step_handler(message, get_age)
        return

    users[message.chat.id]["age"] = int(message.text)
    bot.send_message(message.chat.id, "Из какого ты города?")
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    users[message.chat.id]["city"] = message.text
    bot.send_message(message.chat.id, "Напиши немного о себе.")
    bot.register_next_step_handler(message, get_about)

def get_about(message):
    users[message.chat.id]["about"] = message.text
    bot.send_message(message.chat.id, "❤️ Анкета создана!\n\n" + format_profile(users[message.chat.id]))

def format_profile(profile):
    return (
        f"👤 {profile['name']}, {profile['age']}\n"
        f"📍 {profile['city']}\n"
        f"💬 {profile['about']}"
    )

@bot.message_handler(func=lambda m: m.text == "🔎 Смотреть анкеты")
def show_profiles(message):
    other = next(
        (p for uid, p in users.items() if uid != message.chat.id),
        None
    )
    if other:
        bot.send_message(message.chat.id, format_profile(other))
    else:
        bot.send_message(message.chat.id, "Пока анкет нет. Загляни чуть позже ☕")

@bot.message_handler(func=lambda m: m.text == "ℹ️ О проекте")
def about(message):
    bot.send_message(message.chat.id, "ЗАВАРКА ☕ — место новых знакомств.")

bot.infinity_polling()
