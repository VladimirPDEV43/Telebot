import telebot
from Config import currency, TOKEN
from extensions import APIException, CurrencyTransfer



bot = telebot.TeleBot(TOKEN)


# start, help
@bot.message_handler(commands=['start', 'help'])
def launch(message: telebot.types.Message):
    text = 'Для активации бота введите команду в данном формате: \n "Имя валюты",\
    "В какую валюту нужно перенести", "Кол-во необходимой валюты", \n "Список валют: /values"'
    bot.reply_to(message, text)

# Название валют
@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Список валют:'
    for key in currency:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


# Переводы из одной валюты в другую
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        cash = message.text.split(' ')
        if len(cash) != 3:
            raise APIException('Неверное количество параметров')

        quote, base, amount = cash
        price = CurrencyTransfer.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Вы допустили ошибку: {e}')
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка: {e}')
    else:
        text = f'Цена {amount} {base} в {quote} = {price}'
        bot.send_message(message.chat.id, text)



bot.polling()