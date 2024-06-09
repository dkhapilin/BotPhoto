import pathlib
import threading
from typing import List

from database.queries import recording_work_in_excel


def create_excel_multithreading(users_id: List[tuple], date_works):
    threads = []

    for user_id in users_id:
        thread = threading.Thread(target=recording_work_in_excel, args=(user_id, date_works))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def sending_excel(users_id: List[tuple], date_works):
    docs_excel = []
    path_home_excel = pathlib.Path.cwd()
    for user_id in users_id:
        path_file_excel = path_home_excel / 'working' / date_works[0] / date_works[1] / f"{user_id[0]}.xlsx"
        docs_excel.append(path_file_excel)

    return docs_excel
