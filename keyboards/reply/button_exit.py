from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def button_exit():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text='фотоотчет отправлен')
    keyboard.add(button)
    return keyboard
