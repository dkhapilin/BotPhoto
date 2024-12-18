import pathlib
import re
from datetime import datetime

from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

from database import queries
from keyboards.inlain.selection_buttons import (client_buttons, show_partner, number,
                                                button_next, hours_button, minutes_button)
from keyboards.reply.button_exit import button_exit
from loader import bot
from states.states import SurveyState
from utils.check_and_create_directory import check_and_create_directory

CALL_WORK = ['Монтаж', 'Ремонт', 'Демонтаж', 'Демонтаж', 'Подготовка', 'Доставка']
CALL_AGENT = ['МТС', 'Билайн', 'Мотив', 'Мегафон', 'Столото', 'Соколов', '585 Gold', 'Санлайт', '585 Золотой']

PATH_DOWNLOAD = pathlib.Path.cwd().parent / 'photo'


@bot.callback_query_handler(func=lambda callback: callback.data in CALL_WORK, state=SurveyState.type_of_work)
def choice_client(callback: CallbackQuery):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

    with bot.retrieve_data(callback.message.chat.id) as data:
        data['type_work'] = callback.data
    bot.send_message(callback.from_user.id,
                     'Выберите заказчика.',
                     reply_markup=client_buttons())
    bot.set_state(callback.from_user.id, SurveyState.client, callback.message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data in CALL_AGENT, state=SurveyState.client)
def choice_city(callback: CallbackQuery):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)

    with bot.retrieve_data(callback.message.chat.id) as data:
        data['client'] = callback.data
    bot.set_state(callback.from_user.id, SurveyState.city, callback.message.chat.id)
    bot.send_message(callback.from_user.id, f'Напиши город.')


@bot.message_handler(state=SurveyState.city)
def choice_street(message: Message):
    city: str = message.text
    if all(word.isalpha() for word in city.split()):
        with bot.retrieve_data(message.chat.id) as data:
            data['city'] = city
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.set_state(message.from_user.id, SurveyState.count_partner, message.chat.id)
        bot.send_message(message.from_user.id, f'Напиши улицу и дом.')
    else:
        bot.send_message(message.from_user.id, f'В названии города могут быть только буквы русского алфавита.')


@bot.message_handler(state=SurveyState.count_partner)
def count_part(message: Message):
    street = message.text
    street_new = re.sub(r'[\\/]', '.', street)
    with bot.retrieve_data(message.chat.id) as data:
        data['street'] = street_new
        data['partner_id'] = list()
        data['counter'] = 0
        data['count_partner'] = 0
    bot.set_state(message.from_user.id, SurveyState.partner, message.chat.id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(message.from_user.id, f'Сколько у тебя было напарников?', reply_markup=number(5))


@bot.callback_query_handler(func=lambda callback: callback.data, state=SurveyState.partner)
def choice_partner(callback: CallbackQuery):
    with bot.retrieve_data(callback.from_user.id) as data:
        if int(callback.data) in (1, 2, 3, 4, 5):
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            count = int(callback.data)

            data['count_partner'] = count

            bot.send_message(callback.from_user.id, f'Выбери напарников с кем выполнял работу.',
                             reply_markup=show_partner(callback.from_user.id))

        elif callback.data and data['counter'] < data['count_partner'] - 1:
            data['counter'] += 1
            data['partner_id'].append(int(callback.data))

        else:
            if int(callback.data) != 0:
                data['partner_id'].append(int(callback.data))
            data['counter'] = 0
            if data['type_work'] == 'Ремонт':
                bot.set_state(callback.from_user.id, SurveyState.repair_time, callback.message.chat.id)
                bot.send_message(callback.from_user.id, f"Выбери сколько ЧАСОВ ты выполнял ремонт",
                                 reply_markup=hours_button())
                data['hours_flag'] = True
            else:
                bot.delete_message(callback.message.chat.id, callback.message.message_id)
                bot.set_state(callback.from_user.id, SurveyState.street, callback.message.chat.id)
                bot.send_message(callback.from_user.id,
                                 f"Запись напарника(ов) прошла успешно.\n"
                                 f"Нажми продолжить.",
                                 reply_markup=button_next())

            if len(data['partner_id']) > 0:
                for users_id in data['partner_id']:
                    bot.send_message(users_id, f'{queries.search_user_id(callback.from_user.id)[1]} '
                                               f'добавил вас в {data["type_work"]}.')


@bot.callback_query_handler(func=lambda callback: callback.data, state=SurveyState.street)
def album(callback: CallbackQuery):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    with bot.retrieve_data(callback.message.chat.id) as data:
        file_type_work = data.get('type_work')
        file_client = data.get('client')
        file = f'{data.get("city")}, {data.get("street")}, {callback.from_user.full_name}'
        data_save = datetime.now()
        path = pathlib.Path.absolute(PATH_DOWNLOAD) / data_save.strftime('%Y') / data_save.strftime(
            '%m') / file_type_work / file_client / file
        check_and_create_directory(path)
        data['path'] = path

    bot.set_state(callback.from_user.id, SurveyState.album, callback.message.chat.id)
    bot.send_message(callback.from_user.id, f'Отправляй фотоотчет.\n'
                                            f'Дождись отправки(загрузки) и нажми кнопку.\n'
                                            f'"Фотоотчет отправлен"',
                     reply_markup=button_exit('Фотоотчет отправлен.'))


@bot.message_handler(content_types=['media_group_id', 'document', 'photo', 'text'], state=SurveyState.album)
def download_photo(message: Message):
    if message.photo:
        photo_album = message.photo
        with bot.retrieve_data(message.chat.id) as data:
            path = data['path']
            photo = photo_album[-1]
            dwn_photo = bot.download_file(bot.get_file(photo.file_id).file_path)
            name_jpeg = f'{photo.file_unique_id}.jpeg'
            path_save = pathlib.Path.absolute(path) / name_jpeg
            with open(path_save, 'wb') as file_o:
                file_o.write(dwn_photo)

    elif message.document:
        photo_document = message.document
        with bot.retrieve_data(message.chat.id) as data:
            path = data['path']
            photo = photo_document.file_id
            dwn_photo = bot.download_file(bot.get_file(photo).file_path)
            name_jpeg = f'{photo_document.file_unique_id}.jpeg'
            path_save = pathlib.Path.absolute(path) / name_jpeg
            with open(path_save, 'wb') as file_o:
                file_o.write(dwn_photo)
    elif message.text.lower() == 'фотоотчет отправлен.':
        with bot.retrieve_data(message.chat.id) as data:
            for admin in queries.message_to_admins():
                bot.send_message(f'{admin[0]}', f'Пришел новый фотоотчет.\n'
                                                f'{data["type_work"]} {data["client"]} {data["city"]}, {data["street"]},'
                                                f'{message.from_user.full_name}.')
            queries.append_work(message.from_user.id,
                                data['client'],
                                data['type_work'],
                                data['city'],
                                data['street'],
                                data['partner_id'],
                                data.get('repair_time'))
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.from_user.id, f"До скорой встречи!", reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, SurveyState.main_menu, message.chat.id)

    else:
        bot.send_message(f'Нужно отправить фото.'
                         f'Или нажать кнопку "Фотоотчет отправлен"'
                         f'Или написать "фотоотчет отправлен"')


@bot.callback_query_handler(func=lambda callback: callback.data, state=SurveyState.repair_time)
def repair_time_minutes(callback: CallbackQuery):
    with bot.retrieve_data(callback.from_user.id) as data:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        if data['hours_flag']:
            data['hours_flag'] = False
            data['repair_time'] = callback.data + 'ч'
            bot.send_message(callback.from_user.id, f"Выбери сколько МИНУТ ты выполнял ремонт",
                             reply_markup=minutes_button())
        else:
            data['repair_time'] = data['repair_time'] + callback.data + 'мин'
            bot.set_state(callback.from_user.id, SurveyState.street, callback.message.chat.id)
            bot.send_message(callback.from_user.id,
                             f"Время ремонта записано.\n"
                             f"Нажми продолжить.",
                             reply_markup=button_next())
