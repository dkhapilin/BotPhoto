import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
ROSSKO_KEY_1 = os.getenv('ROSSKO_KEY_1')
ROSSKO_KEY_2 = os.getenv('ROSSKO_KEY_2')
DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    # ('help', 'Вывести справку'),
    # ('add_photo', 'Добавить фотоотчет'),
)
