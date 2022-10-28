from telebot.handler_backends import State, StatesGroup


class SurveyState(StatesGroup):
    main_menu = State()
    type_of_work = State()
    client = State()
    city = State()
    street = State()
    album = State()
