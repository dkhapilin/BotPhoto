from telebot.types import Message, CallbackQuery

from database import queries
from database.queries import show_worker
from loader import bot
from states.states import ManagerState
from utils.creating_files import create_excel_multithreading, sending_excel


@bot.callback_query_handler(func=lambda call: True, state=ManagerState.upload_state_one)
def from_what_date_to_what_date(callback: CallbackQuery):
    with bot.retrieve_data(callback.message.chat.id) as data:
        data['users'] = callback.data
    bot.set_state(callback.from_user.id, ManagerState.upload_state_two, callback.message.chat.id)
    bot.send_message(callback.from_user.id, f'Напиши год-месяц за который надо выгрузить файлы.\nПример: 2023-12')


@bot.message_handler(state=ManagerState.upload_state_two)
def sending_files(message: Message):
    bot.send_message(message.from_user.id, 'Ожидайте подготавливаю файлы')
    with bot.retrieve_data(message.chat.id) as data:
        data['date_work'] = message.text.split('-')
        if data['users'] == "all":
            workers = show_worker()
        else:
            workers_name = queries.search_user_id(data['users'])
            workers = [(workers_name[1], data['users']), ]
        create_excel_multithreading(users_id=workers, date_works=data['date_work'])
        for ex in sending_excel(workers, data['date_work']):
            bot.send_document(message.chat.id, document=open(ex, "rb"))
    bot.delete_state(message.from_user.id, message.chat.id)
