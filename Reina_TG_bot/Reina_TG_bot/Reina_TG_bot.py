import telebot
from currency_converter import CurrencyConverter
from telebot import types
import requests
import json


# bot TOKEN
bot = telebot.TeleBot("5817778920:AAFfaAqXVtLZMBW3xutDkK0ipUkQsROF4mw")

# API Ключ от акка для просмотра погоды
API = "f67ae1b2c208ebabdbc1ab606b40464c"

# Объект конвертера 
currency = CurrencyConverter()
# Значение глобальной переменной конвертера
amount = 0


# en.bot commands start; ru.комманда запуска бота
@bot.message_handler(commands=["start"])
def start(message):
    mess = "Привет! Меня зовут Рейна, рада знакомству <3"
    bot.send_message(message.chat.id, mess) 
    

# en.bot commands convert; ru.комманда запуска конвертера валют
@bot.message_handler(commands=["convert"])
def convert(message):
    bot.send_message(message.chat.id, "Введите нужную сумму:")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат, впишите сумму!")
        bot.register_next_step_handler(message, summa)
        return
    
    if amount >= 1:
        markup = types.InlineKeyboardMarkup(row_width=2) 
        bit1 = types.InlineKeyboardButton("RUB/USD", callback_data="rub/usd")
        bit2 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        bit3 = types.InlineKeyboardButton("RUB/EUR", callback_data="rub/eur")
        bit4 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        markup.row(bit1, bit2, bit3, bit4)  
        bot.send_message(message.chat.id, "Выберите нужную пару валют:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число должно быть >/= 1. Впишите нужную сумму!")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    values = call.data.upper().split("/")
    res =currency.convert(amount, values[0], values[1])
    bot.send_message(call.message.chat.id, f"Получается: {res}. Можете заново вписать сумму")
    bot.register_next_step_handler(call.message, summa)


# bot commands WEATHER; комманда для просмотра погоды
@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(message.chat.id, "Приветствую! Введи нужный город, чтобы узнать погоду <3")


@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if res.status_code == 200:    
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f"Сейчас погода: {temp} градуса;",)
    else:
        bot.reply_to(message, f"Город указан не верно!")

# bot commands help
#@bot.message_handler(commands=["help"])
#def helps(message):
    #bot.send_message(message.chat.id, "")


# bot commands groups 
@bot.message_handler(commands=["groups"])
def groups(message):
    markup = types.InlineKeyboardMarkup() 
    bit1 = types.InlineKeyboardButton("Телеграм группа", url="https://t.me/+dTelnpFMbqJmY2Q6")
    bit2 = types.InlineKeyboardButton("VK группа", url="https://vk.com/imitif_udsu")
    markup.row(bit1, bit2)
    bit3 = types.InlineKeyboardButton("Discord группа", url="https://discord.gg/VbCga5rSzc")
    markup.row(bit3)
    bot.reply_to(message, "Вот доступные группы, на которые тебе стоит подписаться UwU", reply_markup=markup)


# bot commands language
@bot.message_handler(commands=["language"])
def language(message):
    markup = types.ReplyKeyboardMarkup()
    bit1 = types.KeyboardButton("🇷🇺 Русский")
    markup.row(bit1)
    bit2 = types.KeyboardButton("🇺🇸 English")
    markup.row(bit2)
    bot.send_message(message.chat.id, "Выбери нужный Язык:", reply_markup=markup)


# bot settings none stop
bot.polling(none_stop=True)
