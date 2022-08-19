""" Основной модуль программы отвечающий за работу бота """
import json
import os
import telebot

from telebot import types

import headhunter
import kwork


def telegram_bot(token):
    '''
    Основная функция бота, где происходит обработка начинающей функции "/start"
    И остальных строковых команд с обращениями к модулям
    '''
    bot = telebot.TeleBot(token)


    @bot.message_handler(commands=["start"])
    def start_message(message):
        ''' Создание кнопок по которым и происходит навигация пользователя '''

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        hunter = types.KeyboardButton('HeadHunter')
        kworks = types.KeyboardButton('Kwork')

        markup.add(hunter, kworks)

        bot.send_message(message.chat.id, "Привіт, Господин?")
        bot.send_message(message.chat.id, "Куды полезем?", reply_markup = markup)


    @bot.message_handler(content_types=['text'])
    def get_text(message):
        ''' Обработка полученного текста от пользователя '''

        if message.text == 'HeadHunter':
            # Обработка полученного json файла от API HH
            data = json.loads(headhunter.parse())
            work = data['items']

            last_vacancy = headhunter.former_time(work[0]['published_at'])
            published = headhunter.read_log(message.text)

            # Проверка чтобы лишний раз не напрягать бота,
            # Если с прошлого запроса ничего не изменилось
            if last_vacancy == published:
                bot.send_message(message.chat.id, 'С прошлого раза ничего не изменилось = (')
            else:
                for element in work:
                    published_at = headhunter.former_time(element['published_at'])

                    # Проверка чтобы обработка шла до тех пор,
                    # Пока не попадется вакансия с датой публикации позже последней
                    if published is None or published_at > published:
                        name = element['name']
                        url = element['alternate_url']
                        schedule = element['schedule']['name']

                        # Проверки на пустые поля, чтобы вывод следать корректным
                        if element['address'] is None or element['address']['street'] is None:
                            address = 'Не указан'
                        else:
                            address = element['address']['street']

                        salary = element['salary']

                        if salary is None:
                            payment = 'Не указана'

                            # Форматирование отправки сообщения выглядит странно,
                            # Ибо при многострочном тексте сохраняет отступы,
                            # Cделанные внутри фукнций
                            bot.send_message(message.chat.id,
f'''Должность - {name}
Улица - {address}
Занятость - {schedule}
Зарплата - {payment}
Сcылка - {url}''')
                        else:
                            from_payment = element['salary']['from']
                            to_payment = element['salary']['to']
                            currency = element['salary']['currency']

                            bot.send_message(message.chat.id,
f'''Должность - {name}
Улица - {address}
Занятость - {schedule}
Зарплата:
    От: {from_payment}
    До: {to_payment}
    Валюта: {currency}
Сcылка - {url}''')
                    else:
                        break

                headhunter.create_log(last_vacancy, message.text)

        if message.text == 'Kwork':
            # Обработка данных полученных после работы модуля Kwork

            bot.send_message(message.chat.id, "Wait a minute....Process...")
            data = kwork.parse()
            log = kwork.read_log(message.text)

            # Проверка чтобы лишний раз не напрягать бота,
            # Если с прошлого запроса ничего не изменилось
            if data[0]['order_name'] == log:
                bot.send_message(message.chat.id, 'С прошлого раза ничего не изменилось = (')
            else:
                for info in data:
                    # Проверка чтобы обработка шла до тех пор,
                    # Пока не попадется заказ с названием как в логах
                    if info['order_name'] != log:
                        name = info['order_name']
                        description = info['order_description']
                        payment = info['order_payment']
                        count_offers = info['count_offers']
                        precent_orders = info['precent_orders']
                        url = info['order_url']

                        bot.send_message(message.chat.id,
f'''Заказ: {name}\n
Описание:\n
    {description}\n
Оплата: {payment}\n
Информация о заказчике:
    -Количество заказов: {count_offers}
    -Процент законченых: {precent_orders}\n
{url}''')
                    else:
                        break

                kwork.create_log(data[0]['order_name'], message.text)

    bot.polling()


def main():
    ''' Функция запускающая бота и берущая токен из переменного окружения '''

    token = os.getenv('TOKEN')

    telegram_bot(token)


if __name__ == '__main__':
    main()
    