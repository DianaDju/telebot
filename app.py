import telebot
from confiq import keys, TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    ''' Функция для знакомства. Мой бот очень вежливый, поэтому выводить милое сообщение для знакомства! '''
    text = 'Привет, я Бот для конвертации валют =)\nЧто бы начать введи команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nЕсли нужна помощь нажми сюда: /help'
    bot.reply_to(message,text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    ''' Небольшое объяснение для работы с ботом '''
    text= ('Что бы увидеть доступные валюты нажми: /values\nВводи названия валют в единственном числе!\nНапример:\nрубль \
доллар 3 \nКоличество конвертируемой валюты пиши цифрами: 1, 10, 100\nЭто все что я хотел тебе объяснить =)')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    ''' Выводим доступные для конвертации валюты '''
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message,text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    '''Функция для основного общения с пользователем. После обработки запроса, проверяем на правильность написания.
    В случаи выявления ошибок выводим заранее подготовленные ответы. Если же все хорошо выдаем результат работы нашего бота'''
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите три параметра!')

        quote, base, amount = values

        result = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {result:.2f} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True, timeout=30)

