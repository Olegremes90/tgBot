import json
import requests
from config import keys

""" Обработка исключений"""
class ConvertionException(Exception):
    pass


class CryptoConvertor:
    @staticmethod
    def convertor(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"Невозможно перевести одинаковые валюты {base}.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}")
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {base}")
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {amount}")
      # получаем api конвертирующий одну валюту в другую
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # преобразовывем ответ формата json в объект python
        resp = json.loads(r.content)[keys[base]]
       # умножаем полученный объект на колисчество валюты
        return resp * amount

