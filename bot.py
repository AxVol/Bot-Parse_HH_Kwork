import json
import os
import telebot
import headhunter

from telebot import types


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

            with open('log/headhunter.txt', 'r', encoding='utf-8') as f:
                published = f.read()

                if work[0]['published_at'] == published:
                    bot.send_message(message.chat.id, 'С прошлого раза ничего не изменилось = (')
                else:
                    for el in work:
                        if el['published_at'] != published:
                            name = el['name']
                            url = el['alternate_url']
                            schedule = el['schedule']['name']
                            
                            if el['salary'] == None:
                                payment = 'Не указана'
                            else:
                                from_payment = el['salary']['from']
                                to_payment = el['salary']['to']
                                currency = el['salary']['currency']

                            if el['address'] == None or el['address']['street'] == None:
                                address = 'Не указан'
                            else:
                                address = el['address']['street']
                            
                            if payment:
                                bot.send_message(message.chat.id, 
                                    f'Должность - {name}\nУлица - {address}\nЗанятость - {schedule}\nЗарплата - {payment}\nСcылка - {url}')
                            else:
                                bot.send_message(message.chat.id, 
                                    f'Должность - {name}\nУлица - {address}\nЗанятость - {schedule}\nЗарплата\n    От: {from_payment}\n    До: {to_payment}\n    Валюта: {currency}\nСcылка - {url}')
                        else:
                            break

                    with open('log/headhunter.txt', 'w', encoding='utf-8') as file:
                        log = work[0]['published_at']
                        file.write(log)

        if message.text == 'Kwork':
            bot.send_message(message.chat.id, '1')


    bot.polling()


def main():
    token = os.getenv('TOKEN')

    telegram_bot(token)


if __name__ == '__main__':
    main()