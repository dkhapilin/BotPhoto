from marshmallow import ValidationError
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

from utils.req import get_balance_rossko
import keyboards
from database import queries
from database.queries import *
from loader import bot
from states.states import ManagerState, AddUserState, SurveyState, AdminState
from utils.schemas import UserSchema, ClientSchema


REPEAT = False


@bot.callback_query_handler(func=lambda callback: callback.data, state=AddUserState.add_user)
def info_user(callback: CallbackQuery):
    if callback.data != 'Отказ':
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['id'] = callback.data
        bot.set_state(callback.from_user.id, AddUserState.info_user)
        bot.send_message(callback.from_user.id, f'Укажите данные пользователя\n'
                                                f'ФИО/Права_Доступа(1-обычные, 2-Менеджер, 3-Главный админ)')
    else:
        bot.send_message(callback.from_user.id, f'Вы отказали в праве доступа пользователю')


@bot.message_handler(state=AddUserState.info_user)
def add_user(message: Message):
    data_user = message.text.split('/')
    with bot.retrieve_data(message.chat.id) as data:
        new_user = queries.add_user(data_user[0], int(data_user[1]), int(data['id']))

        bot.send_message(message.from_user.id, f'Добавлен новый пользователь:\n{new_user}')
        bot.send_message(data['id'], f'Вам дали доступ!\n'
                                     f'Добро пожаловать!')


@bot.message_handler(content_types=['media_group_id', 'document', 'photo', 'text'], state=ManagerState.state_maling_one)
def maling_func(message: Message):
    global REPEAT
    if message.text:
        text = message.text
        if text == 'Отправить фото.':
            with bot.retrieve_data(message.chat.id) as data:
                count_photo = len(data['photo_id'])
                bot.send_message(message.from_user.id, f'Хотите отправить {count_photo} фото.',
                                 reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())
                bot.set_state(message.from_user.id, ManagerState.state_maling_photo, message.chat.id)
                REPEAT = False

        elif text == 'Отправить документы.':
            with bot.retrieve_data(message.chat.id) as data:
                bot.send_message(message.from_user.id,
                                 f'Вы собираетесь отправить следующие документы: {data["document_id"]}.',
                                 reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())
                bot.set_state(message.from_user.id, ManagerState.state_maling_documents, message.chat.id)
                REPEAT = False
        else:
            bot.send_message(message.from_user.id, f"Вы хотите отправить: \n{text}",
                             reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())
            with bot.retrieve_data(message.chat.id) as data:
                data['text'] = text
            bot.set_state(message.from_user.id, ManagerState.state_maling_text, message.chat.id)

    elif message.photo:
        if not REPEAT:
            bot.send_message(message.from_user.id, f'Фото загружены. Нажми "Отправить фото."',
                             reply_markup=keyboards.reply.button_exit.button_exit('Отправить фото.'))
            REPEAT = True
        with bot.retrieve_data(message.chat.id) as data:
            data['photo_id'].append(message.photo[-1].file_id)

    elif message.document:
        if not REPEAT:
            bot.send_message(message.from_user.id, f'Документы загружены. Нажми "Отправить документы."',
                             reply_markup=keyboards.reply.button_exit.button_exit('Отправить документы.'))
            REPEAT = True
        with bot.retrieve_data(message.chat.id) as data:
            data['document_id'].append(message.document.file_id)


@bot.callback_query_handler(func=lambda callback: callback.data, state=ManagerState.state_maling_photo)
def maling_photo(callback: CallbackQuery):
    bot.delete_message(callback.message.chat.id, callback.message.id)
    members = users_list()
    if callback.data == 'yes':
        with bot.retrieve_data(callback.message.chat.id) as data:
            for member in members:
                for photo in data['photo_id']:
                    bot.send_photo(member[1], photo)

        bot.send_message(callback.from_user.id, f'Фото отправлены.', reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(callback.from_user.id, f'Отправка отменена.', reply_markup=ReplyKeyboardRemove())
        bot.set_state(callback.from_user.id, SurveyState.main_menu, callback.message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data, state=ManagerState.state_maling_documents)
def maling_documents(callback: CallbackQuery):
    bot.delete_message(callback.message.chat.id, callback.message.id)
    members = users_list()
    if callback.data == 'yes':
        with bot.retrieve_data(callback.message.chat.id) as data:
            for member in members:
                for document in data['document_id']:
                    bot.send_document(member[1], document)
        bot.send_message(callback.from_user.id, f'Документы отправлены.', reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(callback.from_user.id, f'Отправка отменена.', reply_markup=ReplyKeyboardRemove())
        bot.set_state(callback.from_user.id, SurveyState.main_menu, callback.message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data, state=ManagerState.state_maling_text)
def maling_text(callback: CallbackQuery):
    bot.delete_message(callback.message.chat.id, callback.message.id)
    members = users_list()
    if callback.data == 'yes':
        for member in members:
            with bot.retrieve_data(callback.message.chat.id) as data:
                bot.send_message(member[1], data['text'])
        bot.send_message(callback.from_user.id, f'Сообщение отправлено.', reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(callback.from_user.id, f'Отправка отменена.', reply_markup=ReplyKeyboardRemove())
        bot.set_state(callback.from_user.id, SurveyState.main_menu, callback.message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data, state=AdminState.admin_menu)
def admin_menu(callback: CallbackQuery):
    bot.delete_message(callback.message.chat.id, callback.message.id)
    data = callback.data
    match data:
        case 'list_users':
            members = users_list_for_admin()
            text_members = 'Права доступа 1-монтажник, 2-менеджер, 3-администратор.\n'
            for member in members:
                text_members += f'id-{member[0]}; ФИО-{member[1]}; права-{member[2]}; telegram_id-{member[3]}\n'
            bot.send_message(
                callback.from_user.id,
                text_members,
                reply_markup=keyboards.inlain.selection_buttons.buttons_admin_menu_users()
            )
        case 'delete_users':
            bot.set_state(callback.from_user.id, AdminState.delete_user)
            bot.send_message(callback.from_user.id,
                             f"Укажите telegram_id;ФИО;права пользователя, которого хотите удалить.")
        case 'update_users':
            text = """
            Форма замены данных:\n
            telegram_id;ФИО;права\n
            Пример:\n
            1235678;Иванов И.И.;2\n
            То что не нужно менять, укажите текущие данные.\n
            ВАЖНО - telegram_id менять нельзя. \nТочка с запятой обязательны для разделения данных.
            """
            bot.set_state(callback.from_user.id, AdminState.update_user)
            bot.send_message(callback.from_user.id, text)
        case 'users_management':
            bot.send_message(
                callback.from_user.id,
                "Что ты хочешь сделать с этими неудачниками?",
                reply_markup=keyboards.inlain.selection_buttons.buttons_admin_menu_users()
            )
        case 'clients_management':
            bot.send_message(
                callback.from_user.id,
                "Снова новый заказчик?",
                reply_markup=keyboards.inlain.selection_buttons.buttons_admin_menu_clients()
            )
        case 'get_client':
            all_clients = get_all_clients()
            text = 'id----name\n'
            for client in all_clients:
                text += f'{client.id}----{client.name}\n'
            bot.send_message(callback.from_user.id, text)
        case 'add_new_client':
            bot.set_state(callback.from_user.id, AdminState.add_client, callback.message.chat.id)
            bot.send_message(callback.from_user.id, "Напишите название новой организации.")
        case 'delete_client':
            bot.set_state(callback.from_user.id, AdminState.delete_client, callback.message.chat.id)
            bot.send_message(callback.from_user.id, "Напишите данные организации по форме ниже.\n"
                                                    "id;name\n"
                                                    "Обязательно через точку с запятой.")


@bot.message_handler(state=AdminState.delete_client)
def delete_client(message: Message):
    data = message.text.split(";")
    data_json = {
        "id": data[0],
        "name": data[1],
    }
    schema = ClientSchema()
    try:
        schema.load(data_json)
        bot.send_message(message.from_user.id, 'Не нашли такие данные. Попробуй ещё раз.')
    except ValidationError as err:
        client = schema.create_client(data_json)
        delete_client_from_db(client.id)
        bot.set_state(message.from_user.id, AdminState.choice_access, message.chat.id)
        bot.send_message(
            message.from_user.id,
            f"Клиент {data[0]} {data[1]} удален.",
            reply_markup=keyboards.inlain.selection_buttons.start_buttons_three()
        )


@bot.message_handler(state=AdminState.add_client)
def add_new_client(message: Message):
    data = {
        'name': message.text
    }
    schema = ClientSchema()
    try:
        client = schema.load(data)
        new_client = add_client_to_db(client)
        bot.set_state(message.from_user.id, AdminState.choice_access, message.chat.id)
        bot.send_message(
            message.chat.id,
            f"Добавлен новый клиент.\n{new_client.name}, id - {new_client.id}",
            reply_markup=keyboards.inlain.selection_buttons.start_buttons_three()
        )
    except ValidationError as err:
        bot.send_message(message.chat.id, f"{err.messages}")


@bot.message_handler(state=AdminState.update_user)
def update_user(message: Message):
    data = message.text.split(";")
    data_json = {
        'telegram_id': data[0],
        'users_name': data[1],
        'access': data[2]
    }
    schema = UserSchema()
    try:
        user = schema.load(data_json)
        new_user = update_user_in_db(user)
        bot.set_state(message.from_user.id, AdminState.choice_access, message.chat.id)
        bot.send_message(message.from_user.id,
                         f'Новые данные:\n'
                         f'ФИО-{new_user.users_name}, Права-{new_user.access}',
                         reply_markup=keyboards.inlain.selection_buttons.start_buttons_three()
                         )
        bot.send_message(new_user.telegram_id, f'Ваши данные обновлены:\n'
                                               f'ФИО-{new_user.users_name}, Права-{new_user.access}')
    except ValidationError as err:
        bot.send_message(message.chat.id, err.messages)


@bot.message_handler(state=AdminState.delete_user)
def delete_user(message: Message):
    data = message.text.split(";")
    data_json = {
        'telegram_id': data[0],
        'users_name': data[1],
        'access': data[2]
    }
    schema = UserSchema()
    try:
        user = schema.load(data_json)
        answer = deleted_user_in_db(user)
        bot.set_state(message.from_user.id, AdminState.choice_access, message.chat.id)
        bot.send_message(
            message.from_user.id,
            answer,
            reply_markup=keyboards.inlain.selection_buttons.start_buttons_three()
        )
    except ValidationError as err:
        bot.send_message(message.chat.id, err.messages)


def note_rossko_balance():
    for admin in queries.message_to_admins():
        balance = get_balance_rossko()
        if balance < 0:
            bot.send_message(admin[0], f"В Росско отрицательный баланс: {balance} руб.")
