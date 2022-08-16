import json
import os
import telebot

from telebot import types

import headhunter
import kwork


def telegram_bot(token):
    bot = telebot.TeleBot(token)


    @bot.message_handler(commands=["start"])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        HeadHunter = types.KeyboardButton('HeadHunter')
        Kwork = types.KeyboardButton('Kwork')

        markup.add(HeadHunter, Kwork)

        bot.send_message(message.chat.id, "Привіт, Господин?")
        bot.send_message(message.chat.id, "Куды полезем?", reply_markup = markup)


    @bot.message_handler(content_types=['text'])
    def get_text(message):
        if message.text == 'HeadHunter':
            data = json.loads(headhunter.parse())
            work = data['items']
            last_vacancy = headhunter.former_time(work[0]['published_at'])

            published = headhunter.read_log()

            if last_vacancy == published:
                bot.send_message(message.chat.id, 'С прошлого раза ничего не изменилось = (')
            else:
                for el in work:
                    published_at = headhunter.former_time(el['published_at'])
                    if published is None or published_at > published:
                        name = el['name']
                        url = el['alternate_url']
                        schedule = el['schedule']['name']

                        if el['address'] is None or el['address']['street'] is None:
                            address = 'Не указан'
                        else:
                            address = el['address']['street']

                        salary = el['salary']

                        if salary is None:
                            payment = 'Не указана'

                            bot.send_message(message.chat.id,
                                f'Должность - {name}\nУлица - {address}\nЗанятость - {schedule}\nЗарплата - {payment}\nСcылка - {url}')
                        else:
                            from_payment = el['salary']['from']
                            to_payment = el['salary']['to']
                            currency = el['salary']['currency']

                            bot.send_message(message.chat.id,
                                f'Должность - {name}\nУлица - {address}\nЗанятость - {schedule}\nЗарплата\n    От: {from_payment}\n    До: {to_payment}\n    Валюта: {currency}\nСcылка - {url}')
                    else:
                        break

                headhunter.create_log(last_vacancy)

        if message.text == 'Kwork':
            bot.send_message(message.chat.id, "Wait a minute....Process...")
            data = kwork.parse()
            log = kwork.read_log()

            if data[0]['order_name'] == log:
                bot.send_message(message.chat.id, 'С прошлого раза ничего не изменилось = (')
            else:
                for info in data:
                    if info['order_name'] != log:
                        name = info['order_name']
                        description = info['order_description']
                        payment = info['order_payment']
                        count_offers = info['count_offers']
                        precent_orders = info['precent_orders']
                        url = info['order_url']

                        bot.send_message(message.chat.id,
                            f'Заказ: {name}\n\nОписание:\n {description}\n\nОплата: {payment}\n\nИнформация о заказчике:\n   -Количество заказов: {count_offers}\n   -Процент законченых: {precent_orders}\n\n{url}')
                    else:
                        break

                kwork.create_log(data[0]['order_name'])

    bot.polling()


def main():
    token = os.getenv('TOKEN')

    telegram_bot(token)


if __name__ == '__main__':
    main()
    