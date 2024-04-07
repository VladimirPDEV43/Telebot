import requests
import json
from Config import currency

# Исключения
class APIException(Exception):
    pass


# Класс для перевода валют
class CurrencyTransfer:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException("Запрещается переводить одинаковые валюты")

        try:
            quote_tick = currency[quote]
        except KeyError:
            raise APIException(f'Выбрана неподходящая валюта - {quote}')

        try:
            base_tick = currency[base]
        except KeyError:
            raise APIException(f'Выбрана неподходящая валюта - {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверно введено количество валюты - {amount}')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_tick}&tsyms={base_tick}")
        price = json.loads(r.content)[base_tick]

        return price




