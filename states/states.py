from telebot.handler_backends import State, StatesGroup


class SurveyState(StatesGroup):
    main_menu = State()
    type_of_work = State()
    client = State()
    city = State()
    street = State()
    count_partner = State()
    partner = State()
    album = State()


class AddUserState(StatesGroup):
    add_user = State()
    info_user = State()


class AdminState(StatesGroup):
    admin_menu = State()


class HistoryStates:
    history_menu = State()
    records = State()
    number_records = State()

