from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from loader import bot
from states.states import AdminState, AddUserState, SurveyState
from database import queries
import keyboards.inlain.selection_buttons


CALL_ADMIN = ['maling']


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
    bot.set_state(message.from_user.id, AdminState.state_maling_two, message.chat.id)

    if message.text:
        text = message.text
        bot.send_message(message.from_user.id, f"Вы хотите отправить: \n{text}",
                         reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())
        with bot.retrieve_data(message.chat.id) as data:
            data['text'] = text

    elif message.photo:
        bot.send_message(message.from_user.id, f'Вы отправляете фото с сжатием.',
                         reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())
        with bot.retrieve_data(message.chat.id) as data:
            data['photo_id'] = message.photo[-1].file_id    # Надо сделать так чтоб все фото сначала записывались в список

    elif message.document:
        bot.send_message(message.from_user.id, f'Вы хотите отправить документ:\n{message.document.file_name}',
                         reply_markup=keyboards.inlain.selection_buttons.buttons_yes_or_not())

    bot.set_state(message.from_user.id, AdminState.state_maling_three, message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data, state=AdminState.state_maling_three) # У каждого типа сообщения своё состояние в чате.
def maling_run(callback: CallbackQuery):
    if callback.data == 'yes':
        with bot.retrieve_data(callback.message.chat.id) as data:
            if data.get('photo_id'):
                photo = data['photo_id']
                bot.send_photo(callback.from_user.id, photo)
    else:
        bot.send_message(callback.from_user.id, f'Отправка отменена.')
        bot.set_state(callback.from_user.id, SurveyState.main_menu, callback.message.chat.id)
