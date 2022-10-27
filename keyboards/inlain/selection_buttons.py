from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_installation = InlineKeyboardButton(text='Монтаж', callback_data='Монтаж')
    button_repair = InlineKeyboardButton(text='Ремонт', callback_data='Ремонт')
    keyboard.add(button_installation, button_repair)

    return keyboard


def client_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_MTC = InlineKeyboardButton(text='МТС', callback_data='МТС')
    button_Bilain = InlineKeyboardButton(text='Билайн', callback_data='Билайн')
    button_Motiv = InlineKeyboardButton(text='Мотив', callback_data='Мотив')
    button_Megafon = InlineKeyboardButton(text='Мегафон', callback_data='Мегафон')
    button_Stoloto = InlineKeyboardButton(text='Столото', callback_data='Столото')
    button_Sokolov = InlineKeyboardButton(text='Соколов', callback_data='Соколов')
    button_585 = InlineKeyboardButton(text='585', callback_data='585')

    keyboard.add(button_MTC,
                 button_Bilain,
                 button_Megafon,
                 button_Motiv,
                 button_Stoloto,
                 button_Sokolov,
                 button_585)

    return keyboard
