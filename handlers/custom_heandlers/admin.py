from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from loader import bot
from states.states import AdminState, AddUserState
from database import queries


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
