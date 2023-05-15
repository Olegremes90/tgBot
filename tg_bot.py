import telebot
from extensions import ConvertionException, CryptoConvertor
import traceback
from config import keys, TOKEN
# создаем бота
bot = telebot.TeleBot(TOKEN)

# обрабатываем команды start и help
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты>  \
    <в какую валюту перевести> \
    <количество переводимой валюты>\nУвидеть список всех доступных валют: /values"
    bot.send_message(message.chat.id, text)

# выводим список возможных конвертаций валюты
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

# обработчик
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    try:
        # разбили строку на эелементы
        values = message.text.split(' ')
        # проверили количество
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров!')
        # каждому эелементу присвоили переменную
        quote, base, amount = values
        # вызвали функцию конвертации
        total_base = CryptoConvertor.convertor(quote, base, amount)
        # обрабатываем возможные исключения
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # формируем ответ для пользователя
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()