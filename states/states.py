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
    repair = State()
    repair_time = State()


class AddUserState(StatesGroup):
    add_user = State()
    info_user = State()


class ManagerState(StatesGroup):
    state_maling_one = State()
    state_maling_two = State()
    state_maling_photo = State()
    state_maling_documents = State()
    state_maling_text = State()
    upload_state_one = State()
    upload_state_two = State()


class AdminState(StatesGroup):
    choice_access = State()
    admin_menu = State()
    delete_user = State()
    update_user = State()


class HistoryStates:
    history_menu = State()
    records = State()
    number_records = State()
