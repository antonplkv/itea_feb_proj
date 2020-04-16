from telebot import TeleBot
from .config import TOKEN
from .keyboards import START_KB
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from ..db.models import (
    Customer,
    Category,
    News,
    Product
)

from flask import Flask
from flask import request, abort

bot = TeleBot(TOKEN)
app = Flask(__name__)


@app.route('/', methods=['POST'])
def process_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(status=403)


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
    categories = Category.get_root()
    buttons = [InlineKeyboardButton(text=category.title, callback_data=f'category_{category.id}') for category in categories]
    kb.add(*buttons)

    bot.send_message(
        message.chat.id,
        "Выберите категорию",
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('category'))
def category_handler(call):
    category_id = '_'.join(call.data.split('_')[1::])
    category = Category.objects.get(id=category_id)
    kb = InlineKeyboardMarkup(row_width=2)

    if category.subcategories:
        buttons = [InlineKeyboardButton(text=category.title, callback_data=f'category_{category.id}') for category in
                    category.subcategories]
        kb.add(*buttons)

        bot.edit_message_text(
            category.title,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kb
        )

    elif category.is_leaf:

        for product in category.products:
            button = InlineKeyboardButton(text='Добавить в корзину', callback_data=f'product_{product.id}')
            kb.keyboard = [[button.to_dic()]]

            bot.send_photo(
                call.message.chat.id,
                product.image.read(),
                caption=product.description,
                disable_notification=True,
                reply_markup=kb

            )


@bot.callback_query_handler(func=lambda call: call.data.startswith('product'))
def add_to_cart(call):
    pass


@bot.message_handler(func=lambda message: message.text == START_KB['news'])
def get_news(message):
    pass


@bot.message_handler(func=lambda message: message.text == START_KB['discount_products'])
def get_discount_products(message):
    pass


def set_webhook():
    import time

    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(
        url='https://34.89.209.222/tg',
        certificate=open('web_shop/bot/webhook_cert.pem', 'r')
    )