from telebot.types import Message, ReplyKeyboardRemove
from loader import bot
from keyboards.inlain.selection_buttons import start_buttons, add_user_button
from states.states import SurveyState, AdminState, AddUserState
from database import management_db


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Функция срабатывает при команде start.
    Выводит приветственное сообщение, и клавиатуру выбора действий.
    Записывает пользователя в БД.

    :param message:
    :return:
    """
    match management_db.check_user(message.from_user.id):
        case 1 | 2 | 3:
            bot.set_state(message.from_user.id, SurveyState.type_of_work, message.chat.id)
            bot.send_message(message.from_user.id,
                             f'Привет, {message.from_user.full_name}\n'
                             f'Чтоб отправить фотоотчет нажми соответсвующую кнопку.',
                             reply_markup=start_buttons())

        case _:
            bot.send_message(message.from_user.id, f'Вас нет в списке разрешенных пользователей.'   
                                                   f'Обратитесь к администратору.')
            for admin_id in management_db.message_to_main_admin():

                bot.send_message(f'{admin_id[0]}',
                                 f'В бот пишет {message.from_user.full_name}\n'
                                 f'ID Пользователя: {message.from_user.id}',
                                 reply_markup=add_user_button(message.from_user.id))
                bot.set_state(admin_id[0], AddUserState.add_user, admin_id[0])
