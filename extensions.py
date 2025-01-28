import json
import requests
from confiq import keys


class APIException(Exception):
    '''Пишем свое исключение для того чтобы бот не слетел при малейших ошибках'''
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        '''Функция обрабатывает ошибки пользователя и вызывает наше исключение с объяснением ошибки.
        Помимо этого в этой функции находиться наше api, тут же мы отправляем запрос на сайт для получения актуального курса валют.
         После конвертируем валюту в соответствии введенными пользователем данными и получаем результат.'''

        if quote == base:
            raise APIException('Вы ввели одинаковые валюты.\nЯ так не работаю =(')

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}.\nВозможно я не работаю с этой валютой.\
Посмотрите список доступных валют здесь:/values')

        try:
            base_ticket = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}.\nПосмотрите правильно ли вы вводите название валют')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать сумму: {amount}.\nВводите цифры!\nПосмотрите правиле здесь:/help')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/232f2f7e8d02b9e14cf5aee5/pair/{keys[quote]}/{keys[base]}')
        data = json.loads(r.content)
        conversion_rate = data['conversion_rate']
        result = float(amount) * conversion_rate
        return result

