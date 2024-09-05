from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import queries
from loader import bot


def type_work():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_installation = InlineKeyboardButton(text='Монтаж', callback_data='Монтаж')
    button_repair = InlineKeyboardButton(text='Ремонт', callback_data='Ремонт')
    button_dismantling = InlineKeyboardButton(text='Демонтаж', callback_data='Демонтаж')
    button_prep = InlineKeyboardButton(text='Подготовка', callback_data='Подготовка')
    button_delivery = InlineKeyboardButton(text='Доставка', callback_data='Доставка')
    keyboard.add(button_installation, button_prep, button_delivery, button_repair, button_dismantling)

    return keyboard


def client_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_mts = InlineKeyboardButton(text='МТС', callback_data='МТС')
    button_bilain = InlineKeyboardButton(text='Билайн', callback_data='Билайн')
    button_motiv = InlineKeyboardButton(text='Мотив', callback_data='Мотив')
    button_megafon = InlineKeyboardButton(text='Мегафон', callback_data='Мегафон')
    button_stoloto = InlineKeyboardButton(text='Столото', callback_data='Столото')
    button_sokolov = InlineKeyboardButton(text='Соколов', callback_data='Соколов')
    button_585 = InlineKeyboardButton(text='585', callback_data='585')
    button_sunlight = InlineKeyboardButton(text='Санлайт', callback_data='Санлайт')

    keyboard.add(button_mts,
                 button_bilain,
                 button_megafon,
                 button_motiv,
                 button_stoloto,
                 button_sokolov,
                 button_585,
                 button_sunlight)

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


def start_buttons_two():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_maling = InlineKeyboardButton(text='Рассылка', callback_data='maling')
    button_upload_work = InlineKeyboardButton(text='Выгрузить работы', callback_data='upload_work')
    keyboard.add(button_maling, button_upload_work)

    return keyboard


def show_partner(user_id):
    keyboard = InlineKeyboardMarkup(row_width=3)
    button_null = InlineKeyboardButton(text="Делал один", callback_data='Null')
    all_partner = queries.show_worker()
    button_all = InlineKeyboardButton(text='Все', callback_data='all')
    for num in range(0, len(all_partner), 3):
        if len(all_partner) > num + 2:
            keyboard.add(InlineKeyboardButton(text=all_partner[num][0], callback_data=all_partner[num][1]),
                         InlineKeyboardButton(text=all_partner[num + 1][0], callback_data=all_partner[num + 1][1]),
                         InlineKeyboardButton(text=all_partner[num + 2][0], callback_data=all_partner[num + 2][1]))
        elif len(all_partner) > num + 1:
            keyboard.add(InlineKeyboardButton(text=all_partner[num][0], callback_data=all_partner[num][1]),
                         InlineKeyboardButton(text=all_partner[num + 1][0], callback_data=all_partner[num + 1][1]))
        else:
            keyboard.add(InlineKeyboardButton(text=all_partner[num][0], callback_data=all_partner[num][1]))
    if bot.get_state(user_id) == 'AdminState:upload_state_one':
        keyboard.add(button_all)
    else:
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
    for hours in range(0, 12, 3):
        keyboard.add(InlineKeyboardButton(text=f"{hours}", callback_data=f"{hours}"),
                     InlineKeyboardButton(text=f"{hours + 1}", callback_data=f"{hours + 1}"),
                     InlineKeyboardButton(text=f"{hours + 2}", callback_data=f"{hours + 2}"), )
    keyboard.add(InlineKeyboardButton(text=f"12", callback_data=f"12"))
    return keyboard


def minutes_button():
    keyboard = InlineKeyboardMarkup(row_width=3)
    for hours in range(0, 60, 15):
        keyboard.add(InlineKeyboardButton(text=f"{hours}", callback_data=f"{hours}"))

    return keyboard


def buttons_yes_or_not():
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_yes = InlineKeyboardButton(text=f'Да', callback_data='yes')
    button_not = InlineKeyboardButton(text=f'Нет', callback_data='not')
    keyboard.add(button_yes, button_not)

    return keyboard
