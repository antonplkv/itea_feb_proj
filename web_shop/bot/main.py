from telebot import TeleBot
from .config import TOKEN
from .keyboards import START_KB
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from ..db.models import (
    Customer,
    Category,
    News,
    Product
)

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(value) for value in START_KB.values()]
    kb.add(*buttons)

    bot.send_message(
        message.chat.id,
        'Greetings!',
        reply_markup=kb
    )


@bot.message_handler(func=lambda message: message.text == START_KB['categories'])
def get_categories(message):
    kb = InlineKeyboardMarkup(row_width=2)
    categories = Category.objects()






@bot.message_handler(func=lambda message: message.text == START_KB['news'])
def get_news(message):
    pass


@bot.message_handler(func=lambda message: message.text == START_KB['discount_products'])
def get_discount_products(message):
    pass

