from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from loader import bot
from states.states import AdminState, AddUserState, SurveyState
from database import queries
from database.queries import users_list
import keyboards


CALL_ADMIN = ['maling']
REPEAT = False


@bot.callback_query_handler(func=lambda callback: callback.data, state=AddUserState.add_user)
def info_user(callback: CallbackQuery):
    if callback.data != 'Отказ':
        with bot.retrieve_data(callback.message.chat.id) as data:
            data['id'] = callback.data
        bot.set_state(callback.from_user.id, AddUserState.info_user)
        bot.send_message(callback.from_user.id, f'Укажите данные пользователя\n'
                                                f'ФИО/Права_Доступа(1-обычные, 2-Админ, 3-Главный админ)')
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


@bot.message_handler(content_types=['media_group_id', 'document', 'photo', 'text'], state=AdminState.state_maling_one)
def maling_func(message: Message):
    global REPEAT
    if message.text:
        text = message.text
        if text == 'Отправить фото.':
            with bot.retrieve_data(message.chat.id) as data:
                count_photo = len(data['photo_id'])
                bot.send_message(message.from_user.id, f'Хотите отправить {count_photo} фото.',
                                 reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())
                bot.set_state(message.from_user.id, AdminState.state_maling_photo, message.chat.id)
                REPEAT = False

        elif text == 'Отправить документы.':
            with bot.retrieve_data(message.chat.id) as data:
                bot.send_message(message.from_user.id,
                                 f'Вы собираетесь отправить следующие документы: {data["document_id"]}.',
                                 reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())
                bot.set_state(message.from_user.id, AdminState.state_maling_documents, message.chat.id)
                REPEAT = False
        else:
            bot.send_message(message.from_user.id, f"Вы хотите отправить: \n{text}",
                             reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())
            with bot.retrieve_data(message.chat.id) as data:
                data['text'] = text
            bot.set_state(message.from_user.id, AdminState.state_maling_text, message.chat.id)

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


@bot.callback_query_handler(func=lambda callback: callback.data, state=AdminState.state_maling_photo)
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


@bot.callback_query_handler(func=lambda callback: callback.data, state=AdminState.state_maling_documents)
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


@bot.callback_query_handler(func=lambda callback: callback.data, state=AdminState.state_maling_text)
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

