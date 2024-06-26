from telebot.types import Message

from database import queries
from keyboards.inlain import selection_buttons
from loader import bot
from states.states import SurveyState, AddUserState


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Функция срабатывает при команде start.
    Выводит приветственное сообщение, и клавиатуру выбора действий.
    Записывает пользователя в БД.

    :param message:
    :return:
    """
    bot.delete_message(message.chat.id, message.message_id)
    match queries.check_user(message.from_user.id):
        case 1:
            bot.set_state(message.from_user.id, SurveyState.main_menu, message.chat.id)
            bot.send_message(message.from_user.id,
                             f'Привет, {message.from_user.full_name}\n'
                             f'Выбери пункт меню.',
                             reply_markup=selection_buttons.start_buttons_one())
        case 2 | 3:
            bot.set_state(message.from_user.id, SurveyState.main_menu, message.chat.id)
            bot.send_message(message.from_user.id,
                             f'Привет, {message.from_user.full_name}\n',
                             reply_markup=selection_buttons.start_buttons_two())

        case _:
            bot.send_message(message.from_user.id, f'Вас нет в списке разрешенных пользователей.'
                                                   f'Обратитесь к администратору.')
            for admin_id in queries.message_to_main_admin():
                bot.send_message(f'{admin_id[0]}',
                                 f'В бот пишет {message.from_user.full_name}\n'
                                 f'ID Пользователя: {message.from_user.id}',
                                 reply_markup=selection_buttons.add_user_button(message.from_user.id))
                bot.set_state(admin_id[0], AddUserState.add_user, admin_id[0])
