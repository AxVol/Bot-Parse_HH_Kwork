""" Модуль отвечающий за сбор данных с Kwork и создание логов к нему"""
#import os
import requests

from bs4 import BeautifulSoup as BS

import connect_sheet


def parse() -> list:
    '''
    Функция отвечающая за парсинг кворка и собирающая все нужные данные.
    Название заказа, его ценник и описание, а так же важную информациюю о заказчике,
    Такую как количество созданных им заказов и нанятых фрилансеров,
    Чтобы отсеивать тех кто просто выкладывают заказы и не закрывают их.
    '''
    result_list = []

    for pagination in range(1, 20):

        response = requests.get(f'https://kwork.ru/projects?c=41&page={pagination}').text
        soup = BS(response, 'lxml')
        block = soup.find('div', {'class': 'wants-content'})
        content = block.find_all('div', {'class': 'card__content pb5'})

        for data in content:
            offer = data.find('div', {'class': 'mb15'})
            order_name = offer.find('div', {
                    'class': 'wants-card__header-title first-letter breakwords pr250'
                })
            order_payment = offer.find('div', {
                    'class': 'wants-card__header-price wants-card__price m-hidden'
                })
            order_discription = offer.find('div', {
            'class': 'breakwords first-letter js-want-block-toggle js-want-block-toggle-full hidden'
            })
            customer = data.find('div', {'class': 'dib v-align-t ml10'})
            count_orders = customer.find('div', {'class': 'dib v-align-t'}).text

            former =count_orders.replace('\n', '').split()
            count_offers = f'{former[0]} {former[1]} {former[2]} {former[3]} {former[4]}'

            # Блок с проверками на пустые поля и прочие мелочи, чтобы вывод данных был корректным
            if former[-1] != '1':
                precent_orders = f'{former[-2]} {former[-1]}'
            else:
                precent_orders = 'Нету данных'

            if order_name is None:
                order_name = offer.find('div', {
                        'class': 'wants-card__header-title first-letter breakwords pr200'
                    })
                order_url = order_name.find('a').get('href')
            else:
                order_url = order_name.find('a').get('href')

            if order_discription is None:
                order_discription = offer.find('div', {'class': 'breakwords first-letter'}).text
            else:
                order_discription = order_discription.text.replace('Скрыть', '')

            # Загрузка данных в словарь чтобы потом бот их распарсил
            result_list.append(
                {
                    'order_name': order_name.text,
                    'order_description': order_discription,
                    'order_payment': order_payment.text,
                    'count_offers': count_offers,
                    'precent_orders': precent_orders,
                    'order_url': order_url
                }
            )

    return result_list


# Если вы не хотите настраивать подключение к гугл таблицам для ведения логов,
# (Мне так было удобнее, для взаимодествие с ботом когда он лежит на сервере),
# То просто закомментируйте соответствующие строки, а раскомментируйте те,
# Которые отвечают за запись в локальный файл txt

# ******* Не забудьте раскомментировать импорт модуля os

def create_log(name: str, kwork: str):
    '''
    Создание логов на основе названия заказа,
    Чтобы при следующем запросе к модулю, не получать повторные данные.
    '''
    #with open('log/kwork.txt', 'w', encoding='utf-8') as file:
        #file.write(name)

    connect_sheet.main('write', name, kwork)

def read_log(kwork: str) -> str:
    '''Чтение логов.

    *** Это при условии что вы используете локальную запись файлов

    Так как чтение логов в боте встречается раньше чем запись,
    То тут добавлена проверка на существование пути,
    А так же на то, что другой модуль в программе уже мог создать эту папку.
    '''

    result = connect_sheet.main('read', kwork)

    return result

    #try:
        #with open('log/kwork.txt', 'r', encoding='utf-8') as file:
            #log = file.read()

    #except FileNotFoundError:
        #try:
            #os.mkdir('log')
        #except FileExistsError:
            #return None
