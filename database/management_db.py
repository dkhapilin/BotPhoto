import sqlite3
import pathlib

PATH_DB = pathlib.Path.cwd() / 'database' / 'data_base'


def users_list():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        users = cur_db.execute(f"SELECT * FROM users").fetchall()


def add_user(user_name, access, telegram_id):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        print([user_name, access, telegram_id])
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
                                f"WHERE access = 2")
        return answer


def message_to_main_admin():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        answer = cur_db.execute(f"SELECT telegram_id FROM users "
                                f"WHERE access = 3")
        return answer
