from loader import bot
from database.queries import init_db
import handlers
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter

if __name__ == '__main__':
    print(handlers.custom_heandlers.survey.PATH_DOWNLOAD)
    init_db()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
