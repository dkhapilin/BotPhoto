from telebot.types import Message, CallbackQuery
from loader import bot
from states.states import SurveyState
from keyboards.inlain.selection_buttons import client_buttons
from utils.check_and_create_directory import check_and_create_directory
import pathlib


PATH_DOWNLOAD = pathlib.Path.home() / 'photo'


@bot.callback_query_handler(func=lambda callback: callback.data, state=SurveyState.type_of_work)
def choice_client(callback: CallbackQuery):
    with bot.retrieve_data(callback.message.chat.id) as data:
        data['type_work'] = callback.data
    bot.send_message(callback.from_user.id,
                     'Выберите заказчика.',
                     reply_markup=client_buttons())
    bot.set_state(callback.from_user.id, SurveyState.client, callback.message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data, state=SurveyState.client)
def choice_city(callback: CallbackQuery):
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

        bot.set_state(message.from_user.id, SurveyState.street, message.chat.id)
        bot.send_message(message.from_user.id, f'Напиши улицу и дом.')
    else:
        bot.send_message(message.from_user.id, f'В названии города могут быть только буквы русского алфавита.')


@bot.message_handler(state=SurveyState.street)
def album(message: Message):
    street = message.text.split('>')

    with bot.retrieve_data(message.chat.id) as data:
        data['street'] = ' '.join(street)

    bot.set_state(message.from_user.id, SurveyState.album, message.chat.id)
    bot.send_message(message.from_user.id, f'Отправляй фотоотчет.')


@bot.message_handler(content_types=['photo', 'text'], state=SurveyState.album)
def download_photo(message: Message):
    if message.photo:
        photo_album = message.photo
        with bot.retrieve_data(message.chat.id) as data:
            file_type_work = data.get('type_work')
            file_client = data.get('client')
            file = f'{data.get("city")}, {data.get("street")}'
            path = pathlib.Path.absolute(PATH_DOWNLOAD) / file_type_work / file_client / file
            check_and_create_directory(path)
            for photo in photo_album:
                if photo.width >= 960:
                    dwn_photo = bot.download_file(bot.get_file(photo.file_id).file_path)
                    name_jpeg = f'{photo.file_unique_id}.jpeg'
                    path_save = pathlib.Path.absolute(path) / name_jpeg
                    print(path_save)
                    with open(path_save, 'wb') as file_o:
                        file_o.write(dwn_photo)

        bot.send_message('802658189', f'Пришел новый фотоотчет.\n'
                                      f'{file_type_work} {file_client} {file}.')

    else:
        bot.send_message(f'Нужно отправить фото.')



