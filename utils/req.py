from zeep import Client, helpers

from config_date import config


URL = "http://api.rossko.ru/service/v2.1/GetSettlements"

KEY_1 = config.ROSSKO_KEY_1
KEY_2 = config.ROSSKO_KEY_2


def get_balance_rossko():
    session = Client(URL)

    response = session.service.GetSettlements(KEY_1, KEY_2)
    data = helpers.serialize_object(response, dict)

    info = data.get("Info")
    balance = int(info.get("balance"))

    return balance
