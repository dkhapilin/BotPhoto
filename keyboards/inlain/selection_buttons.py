from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from database import queries
from database.queries import Client
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


def client_buttons(clients: List[Client]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for client in clients:
        keyboard.add(InlineKeyboardButton(text=client.name, callback_data=client.id))

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
    button_history = InlineKeyboardButton(text='Скачать работы.', callback_data='history_unique')
    keyboard.add(button_client, button_history)

    return keyboard


def start_buttons_two():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_maling = InlineKeyboardButton(text='Рассылка', callback_data='maling')
    button_upload_work = InlineKeyboardButton(text='Выгрузить работы', callback_data='upload_work')
    keyboard.add(button_maling, button_upload_work)

    return keyboard


def start_buttons_three():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_manager = InlineKeyboardButton(text='Менеджер', callback_data='manager')
    button_administrator = InlineKeyboardButton(text="Администратор", callback_data='administrator')
    keyboard.add(button_manager, button_administrator)

    return keyboard


def show_partner(user_id):
    keyboard = InlineKeyboardMarkup(row_width=3)
    button_null = InlineKeyboardButton(text="Делал один", callback_data='0')
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
    if bot.get_state(user_id) == 'ManagerState:upload_state_one':
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


def buttons_admin_menu_users():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_list_users = InlineKeyboardButton(text='Список пользователей', callback_data='list_users')
    button_update_users = InlineKeyboardButton(text='Обновить данные пользователя', callback_data='update_users')
    button_delete_users = InlineKeyboardButton(text='Удалить пользователя', callback_data='delete_users')
    keyboard.add(button_list_users, button_update_users, button_delete_users)

    return keyboard


def buttons_admin_menu_clients():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_get_client = InlineKeyboardButton(text='Показать всех клиентов.', callback_data='get_client')
    button_add_client = InlineKeyboardButton(text='Добавить нового клиента.', callback_data='add_new_client')
    button_delete_client = InlineKeyboardButton(text='Удалить клиента.', callback_data='delete_client')
    keyboard.add(button_get_client, button_add_client, button_delete_client)
    return keyboard


def buttons_main_admin_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_user = InlineKeyboardButton(text='Управление пользователями.', callback_data='users_management')
    button_client = InlineKeyboardButton(text='Управление клиентами.', callback_data='clients_management')
    button_type_work = InlineKeyboardButton(text='Управление типами работ.', callback_data='type_work_management')
    keyboard.add(button_user, button_client, button_type_work)
    return keyboard
