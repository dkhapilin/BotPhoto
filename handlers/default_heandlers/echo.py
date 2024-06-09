from telebot.types import Message

from loader import bot


@bot.message_handler(content_types=['photo', 'text'])
def echo(message: Message):
    bot.send_message(message.from_user.id, f'Не известная команда.')
