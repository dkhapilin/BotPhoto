from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def button_exit(answer):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text=f'{answer}')
    keyboard.add(button)
    return keyboard
