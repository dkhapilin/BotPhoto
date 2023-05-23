from loader import bot
from telebot.types import Message, CallbackQuery
from states.states import HistoryStates, SurveyState
from database import queries
from keyboards.inlain import selection_buttons


@bot.message_handler(state=HistoryStates.history_menu)
def show_history(message: Message):
    if message.text.isdigit():
        answer = queries.history_worker(int(message.text), message.from_user.id)
        count = 0
        for string in answer:
            bot.send_message(message.from_user.id, f'{string[6]} {string[0]} {string[1]} {string[2]} {string[3]}\n'
                                                   f'{string[5]}\n'
                                                   f'{f"Время ремонта {string[7]}" if string[1] == "Ремонт" else ""}')
            count += 1

        bot.set_state(message.from_user.id, SurveyState.main_menu, message.chat.id)
        if count == int(message.text):
            bot.send_message(message.from_user.id, f'Это {count} последних твоих работ.',
                             reply_markup=selection_buttons.start_buttons_one())
        else:
            bot.send_message(message.from_user.id, f'У тебя пока только {count} выполненных работ.',
                             reply_markup=selection_buttons.start_buttons_one())
    else:
        bot.send_message(message.from_user.id, f"Введи число.")


def func_records(user_id):
    answer = queries.record_worker(user_id)
    count = 0
    for string in answer:
        bot.send_message(user_id, f'{string[7]} {string[1]} {string[2]} {string[3]} {string[4]}\n'
                                  f'{string[6]}\n'
                                  f'{f"Время ремонта {string[8]}" if string[2] == "Ремонт" else ""}',
                         reply_markup=selection_buttons.record_button(string[0]))
        count += 1

    bot.set_state(user_id, HistoryStates.number_records, user_id)
    bot.send_message(user_id, f'ПОСЛЕ ТОГО КАК ЗАПИШИШЬ ВСЮ РАБОТЫ НАЖМИ КНОПКУ ЗАКОНЧИТЬ.\n'
                              f'ЕСЛИ НАЖАЛ ОШИБОЧНО ТО ПОВТОРИ ВСЁ ЗАНОГО, ТЕБЕ ПОКАЖУТ ТОЛЬКО ТО,\n'
                              f'ЧТО ТЫ НЕ ЗАПИСАЛ.', reply_markup=selection_buttons.exit_button())

    with bot.retrieve_data(user_id) as data:
        data['records'] = list()
        data['count_deleted_message'] = count


@bot.callback_query_handler(func=lambda callback: callback.data, state=HistoryStates.number_records)
def record_map(callback: CallbackQuery):
    if callback.data == 'end':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.set_state(callback.from_user.id, SurveyState.main_menu, callback.message.chat.id)
        with bot.retrieve_data(callback.from_user.id) as data:
            queries.update_work_records(data['records'])
            for number_deleted in range(1, data['count_deleted_message'] + 1):
                bot.delete_message(callback.message.chat.id, callback.message.message_id - number_deleted)
        bot.send_message(callback.from_user.id, f'Записи в базе данных изменены.\n'
                                                f'Если что то надо поправить, обратись к администратору.',
                         reply_markup=selection_buttons.start_buttons_one())

    else:
        with bot.retrieve_data(callback.from_user.id) as data:
            data['records'].append(callback.data)
