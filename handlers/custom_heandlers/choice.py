from telebot.types import CallbackQuery

from handlers.custom_heandlers.history import func_records
from keyboards.inlain import selection_buttons
from loader import bot
from states.states import SurveyState, HistoryStates, AdminState


@bot.callback_query_handler(func=lambda callback: callback.data, state=SurveyState.main_menu)
def choice_main_menu(callback: CallbackQuery):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    match callback.data:
        case 'photo':
            bot.set_state(callback.from_user.id, SurveyState.type_of_work, callback.message.chat.id)
            bot.send_message(callback.from_user.id, f'Выбери вид работ.', reply_markup=selection_buttons.type_work())
        case 'history_unique':
            bot.set_state(callback.from_user.id, HistoryStates.history_menu, callback.message.chat.id)
            bot.send_message(callback.from_user.id, f'Напиши сколько последних работ тебе показать.')
        case 'dont_records':
            bot.set_state(callback.from_user.id, HistoryStates.records, callback.message.chat.id)
            func_records(callback.from_user.id)
        case 'maling':
            bot.set_state(callback.from_user.id, AdminState.state_maling_one, callback.message.chat.id)
            bot.send_message(callback.from_user.id, f'Напишите или пришлите файл(фото), что нужно отправить.')
            with bot.retrieve_data(callback.message.chat.id) as data:
                data['photo_id'] = list()
                data['document_id'] = list()
        case "upload_work":
            bot.set_state(callback.from_user.id, AdminState.upload_state_one, callback.message.chat.id)
            bot.send_message(callback.from_user.id, f'Чьи работы вы хотите выгрузить?',
                             reply_markup=selection_buttons.show_partner(callback.from_user.id))
