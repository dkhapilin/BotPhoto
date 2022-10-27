from telebot.types import BotCommand
from config_date.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    """
    Создает меню команд.
    
    :param bot:
    :return:
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )