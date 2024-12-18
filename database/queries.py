import datetime
import pathlib
import sqlite3
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

PATH_DB = pathlib.Path.cwd() / 'database' / 'data_base'
ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"


@dataclass
class User:
    users_name: str
    access: int
    telegram_id: int
    users_id: Optional[int] = None


create_table_users = """
CREATE TABLE users(
    users_id INTEGER PRIMARY KEY AUTOINCREMENT,
    users_name TEXT NOT NULL,
    access INTEGER NOT NULL,
    telegram_id INTEGER NOT NULL
)
"""

create_table_work = """
CREATE TABLE work(
    work_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL,
    type_work TEXT NOT NULL,
    city TEXT NOT NULL,
    street TEXT NOT NULL,
    users_id INTEGER NOT NULL,
    partner_name TEXT NOT NULL,
    records TEXT,
    date_work TEXT NOT NULL,
    time_repair TEXT,
    FOREIGN KEY (users_id) REFERENCES users(users_id)
    )
"""


def checking_exist_table(conn: sqlite3.Connection, table_name: str) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name FROM main.sqlite_master
        WHERE type = 'table' AND name = ?
        """, (table_name,)
    )
    return bool(cursor.fetchone())


def init_db():
    with sqlite3.connect(PATH_DB) as conn:
        exist_table_users = checking_exist_table(conn, "users")
        exist_table_work = checking_exist_table(conn, "work")
        conn.execute(ENABLE_FOREIGN_KEY)
        cursor = conn.cursor()
        if not exist_table_users:
            cursor.executescript(create_table_users)
        if not exist_table_work:
            cursor.executescript(create_table_work)


def users_list():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        users = cur_db.execute(f"SELECT users_name, telegram_id FROM users").fetchall()

    return users


def users_list_for_admin():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        cur_db.execute(
            """
            SELECT users_id, users_name, access, telegram_id FROM users
            """
        )

        return cur_db.fetchall()


def add_user(user_name, access, telegram_id):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        cur_db.execute(f"INSERT INTO users(users_name, access, telegram_id)"
                       f"VALUES (?, ?, ?);", (user_name, access, telegram_id))
        new_user = cur_db.execute(f"SELECT * FROM users "
                                  f"ORDER BY users_id DESC "
                                  f"LIMIT 1 ").fetchall()

        return new_user


def deleted_user_in_db(user: User) -> str:
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        cur_db.execute(
            """
            SELECT users_id, users_name, access, telegram_id FROM users
            WHERE users_name = ? AND access = ? AND telegram_id = ?
            """, (user.users_name, user.access, user.telegram_id)
        )
        user_for_deleted = cur_db.fetchone()
        if user_for_deleted:
            cur_db.execute(
                """
                DELETE FROM users
                WHERE telegram_id = ?
                """, (user.telegram_id,)
            )
            return "Пользователь удален."
        else:
            return 'Пользователь не найден.'


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


def history_worker_count(limit: int, telegram_id: int):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        user_id, users_name = search_user_id(telegram_id)
        answer = cur_db.execute(f"SELECT agent, type_work, city, street, users_name, partner_name, "
                                f"date_work, time_repair "
                                f"FROM (SELECT agent, type_work, city, street, users_name, partner_name, "
                                f"date_work, time_repair "
                                f"FROM work w inner join users u on u.users_id = w.users_id "
                                f"WHERE w.users_id = ? "
                                f"ORDER BY work_id DESC "
                                f"LIMIT ?) as new_table "
                                f"ORDER BY type_work, agent ", (user_id, limit)).fetchall()

        return answer


def show_worker():
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        answer = cur_db.execute(
            f"SELECT users_name, telegram_id FROM users WHERE access = 1").fetchall()

        return answer


def append_work(telegram_id, agent, type_work, city, street, partner_id, time_repair=None):
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
            date = datetime.date.today().isoformat()
            cur_db.execute(
                f"""
                INSERT INTO work 
                (agent, type_work, city, street, users_id, partner_name,date_work, time_repair)
                VALUES (?, ?, ?, ?, ?, ?, ?,?)
                """,
                (agent, type_work, city, street, us_i, fio_partner, date,
                 time_repair if type_work == 'Ремонт' else 'Null')
            )


def search_user_id(telegram_id: int):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        users_id = cur_db.execute(
            f"SELECT users_id, users_name FROM users WHERE telegram_id = {telegram_id} ").fetchall()

        return users_id[0]


def record_worker(telegram_id: int):
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        user_id, users_name = search_user_id(telegram_id)
        answer = cur_db.execute(f"SELECT work_id, agent, type_work, city, street, users_name, partner_name, "
                                f"date_work, time_repair "
                                f"FROM (SELECT work_id, agent, type_work, city, street, users_name, partner_name, "
                                f"date_work, time_repair "
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


def recording_work_in_excel(user_id: tuple, date_work: List[str]):
    with sqlite3.connect(PATH_DB) as db:
        query = f"""
        select agent as Клиент, type_work as Тип_работ, city as Город, street as Улица, users_name as Монтажник, 
        partner_name as Напарники, date_work as Дата_выполнения, time_repair as Время_ремонта
        from work JOIN users u on u.users_id = work.users_id
        where date_work between "{date_work[0]}-{date_work[1]}-00" and "{date_work[0]}-{date_work[1]}-32" 
        and work.users_id = (select users_id from users WHERE telegram_id = {user_id[1]})"""
        data = pd.read_sql(query, db)
    path_file_excel = pathlib.Path.cwd() / 'working' / date_work[0] / date_work[1]
    path_file_excel.mkdir(parents=True, exist_ok=True)
    data.to_excel(path_file_excel / f"{user_id[0]}.xlsx", index=False)


def check_user_by_telegram_id(telegram_id: int) -> bool:
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        cur_db.execute(
            """
            SELECT users_name FROM users WHERE telegram_id = ?
            """, (telegram_id,)
        )

        exist = cur_db.fetchone()
        if exist:
            return True


def update_user_in_db(user: User) -> User:
    with sqlite3.connect(PATH_DB) as db:
        cur_db = db.cursor()
        cur_db.execute(
            """
            UPDATE users
            SET users_name = ?, access = ?
            WHERE telegram_id = ?
            """, (user.users_name, user.access, user.telegram_id)
        )
        user.users_id = cur_db.lastrowid

        return user
