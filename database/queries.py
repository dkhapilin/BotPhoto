import datetime
import sqlite3
import pathlib

PATH_DB = pathlib.Path.cwd() / 'database' / 'data_base'


def users_list():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        users = cur_db.execute(f"SELECT * FROM users").fetchall()
        pass


def add_user(user_name, access, telegram_id):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        cur_db.execute(f"INSERT INTO users(users_name, access, telegram_id)"
                       f"VALUES ('{user_name}', {access}, {telegram_id});")
        new_user = cur_db.execute(f"SELECT * FROM users "
                                  f"ORDER BY users_id DESC "
                                  f"LIMIT 1 ").fetchall()

        return new_user


def deleted_user():
    pass


def create_user():
    pass


def check_user(user_id):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        answer = cur_db.execute(f"SELECT access "
                                f"FROM users "
                                f"WHERE telegram_id = {user_id}").fetchall()
        if answer:
            return answer[0][0]
        else:
            return False


def message_to_admins():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        answer = cur_db.execute(f"SELECT telegram_id FROM users "
                                f"WHERE access = 2 OR access = 3")
        return answer


def message_to_main_admin():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        answer = cur_db.execute(f"SELECT telegram_id FROM users "
                                f"WHERE access = 3")
        return answer


def history_worker(limit: int, telegram_id: int):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        user_id, users_name = search_user_id(telegram_id)
        answer = cur_db.execute(f"SELECT agent, type_work, city, street, users_name, partner_name, date_work "
                                f"FROM (SELECT agent, type_work, city, street, users_name, partner_name, date_work "
                                f"FROM work w inner join users u on u.users_id = w.users_id "
                                f"WHERE w.users_id = {user_id} "
                                f"ORDER BY work_id DESC "
                                f"LIMIT {limit}) as new_table "
                                f"ORDER BY type_work, agent ").fetchall()

        return answer


def show_worker():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        answer = cur_db.execute(f"SELECT users_name, telegram_id FROM users WHERE access = 1").fetchall()

        return answer


def append_work(telegram_id, agent, type_work, city, street, partner_id):

    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        users_id, _ = search_user_id(telegram_id)
        all_partner = list()
        if len(partner_id):
            all_partner = cur_db.execute(f'SELECT users_id, users_name '
                                         f'FROM users '
                                         f'WHERE telegram_id IN {tuple(partner_id) if len(partner_id) > 1 else f"({partner_id[0]})"} ').fetchall()
            fio_partner = '/'.join([a[1] for a in all_partner])
            fio_partner += f'/{search_user_id(telegram_id)[1]}'
        else:
            fio_partner = search_user_id(telegram_id)[1]

        append_users = list()
        append_users.append(users_id)
        if all_partner:
            for a in all_partner:
                append_users.append(a[0])

        for us_i in append_users:

            cur_db.execute(f"INSERT INTO work (agent, type_work, city, street, users_id, partner_name, date_work) "
                           f"VALUES ("
                           f"'{agent}', "
                           f"'{type_work}', "
                           f"'{city}', "
                           f"'{street}', "
                           f"{us_i}, "
                           f"'{fio_partner}', "
                           f"'{datetime.date.today().isoformat()}')")


def search_user_id(telegram_id: int):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        users_id = cur_db.execute(f"SELECT users_id, users_name FROM users WHERE telegram_id = {telegram_id} ").fetchall()

        return users_id[0]


def record_worker(telegram_id: int):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        user_id, users_name = search_user_id(telegram_id)
        answer = cur_db.execute(f"SELECT work_id, agent, type_work, city, street, users_name, partner_name, date_work "
                                f"FROM (SELECT work_id, agent, type_work, city, street, users_name, partner_name, date_work "
                                f"FROM work w inner join users u on u.users_id = w.users_id "
                                f"WHERE w.users_id = {user_id} AND records IS NULL "
                                f"ORDER BY work_id DESC "
                                f") as new_table "
                                f"ORDER BY type_work, agent ").fetchall()

        return answer


def update_work_records(work_id):
    if len(work_id) > 0:
        with sqlite3.connect(PATH_DB) as db:
            cur_db = db.cursor()
            cur_db.execute(f'UPDATE work '
                           f'SET records = "записал"'
                           f'WHERE work_id IN {tuple(work_id) if len(work_id) > 1 else f"({work_id[0]})"} ')
