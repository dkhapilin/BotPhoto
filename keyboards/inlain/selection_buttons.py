from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import queries


def type_work():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_installation = InlineKeyboardButton(text='Монтаж', callback_data='Монтаж')
    button_repair = InlineKeyboardButton(text='Ремонт', callback_data='Ремонт')
    button_dismantling = InlineKeyboardButton(text='Демонтаж', callback_data='Демонтаж')
    keyboard.add(button_installation, button_repair, button_dismantling)

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


def add_user_button(id_user):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_add = InlineKeyboardButton(text='Добавить', callback_data=id_user)
    button_not_add = InlineKeyboardButton(text='Отказать', callback_data='Отказ')
    keyboard.add(button_add, button_not_add)

    return keyboard


def start_buttons_one():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_client = InlineKeyboardButton(text='Отправить фото', callback_data='photo')
    button_history = InlineKeyboardButton(text='Посмотреть историю работ.', callback_data='history_unique')
    button_history_records = InlineKeyboardButton(text='Не записанные работы', callback_data='dont_records')
    keyboard.add(button_client, button_history, button_history_records)

    return keyboard


def show_partner():
    keyboard = InlineKeyboardMarkup(row_width=3)
    button_null = InlineKeyboardButton(text="Делал один", callback_data='Null')
    all_partner = queries.show_worker()
    for users_name, users_id in all_partner:
        keyboard.add(InlineKeyboardButton(text=users_name, callback_data=users_id))
    keyboard.add(button_null)
    return keyboard


def number(number_digits: int):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for digit in range(0, number_digits + 1):
        keyboard.add(InlineKeyboardButton(text=f'{digit}', callback_data=f'{digit}'))

    return keyboard


def button_next():
    keyboard = InlineKeyboardMarkup(row_width=1)
    next_step = InlineKeyboardButton(text='Продолжить', callback_data='next')
    keyboard.add(next_step)

    return keyboard


def record_button(work_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_yes = InlineKeyboardButton(text='Записал', callback_data=work_id)
    button_no = InlineKeyboardButton(text='Оставил', callback_data='not')
    keyboard.add(button_yes, button_no)

    return keyboard


def exit_button():
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_exit = InlineKeyboardButton(text='Закончить', callback_data='end')
    keyboard.add(button_exit)

    return keyboard


def hours_button():
    keyboard = InlineKeyboardMarkup(row_width=3)
    for hours in range(0, 13):
        keyboard.add(InlineKeyboardButton(text=f"{hours}", callback_data=f"{hours}"))

    return keyboard


def minutes_button():
    keyboard = InlineKeyboardMarkup(row_width=3)
    for hours in range(0, 60, 15):
        keyboard.add(InlineKeyboardButton(text=f"{hours}", callback_data=f"{hours}"))

    return keyboard
