from telebot.types import Message, ReplyKeyboardRemove
from loader import bot
from keyboards.inlain.selection_buttons import start_buttons
from states.states import SurveyState


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Функция срабатывает при команде start.
    Выводит приветственное сообщение, и клавиатуру выбора действий.
    Записывает пользователя в БД.

    :param message:
    :return:
    """
    bot.set_state(message.from_user.id, SurveyState.type_of_work, message.chat.id)
    bot.send_message(message.from_user.id,
                     f'Привет, {message.from_user.full_name}\n'
                     f'Чтоб отправить фотоотчет нажми соответсвующую кнопку.',
                     reply_markup=start_buttons())
    print(message.from_user.id)
