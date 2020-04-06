from telebot import TeleBot
from .config import TOKEN
from ..db.models import Customer


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Greetings!'
    )


bot.polling()