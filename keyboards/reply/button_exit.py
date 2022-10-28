from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def button_exit():
    keyboard = ReplyKeyboardMarkup()
    button = KeyboardButton(text='фотоотчет отправлен')
    keyboard.add(button)
    return keyboard