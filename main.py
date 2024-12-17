from loader import bot
from database.queries import init_db
import handlers
import schedule
import time
import threading

from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':
    schedule.every().day.at("10:00").do(handlers.custom_heandlers.admin.note_rossko_balance)

    thread = threading.Thread(target=schedule_checker).start()

    init_db()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
