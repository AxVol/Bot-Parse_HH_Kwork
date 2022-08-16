import os
import requests

from bs4 import BeautifulSoup as BS


def parse() -> list:
    result_list = []

    for pagination in range(1, 15):

        response = requests.get(f'https://kwork.ru/projects?c=41&page={pagination}').text
        soup = BS(response, 'lxml')
        block = soup.find('div', {'class': 'wants-content'})
        content = block.find_all('div', {'class': 'card__content pb5'})

        for data in content:
            offer = data.find('div', {'class': 'mb15'})
            order_name = offer.find('div', {'class': 'wants-card__header-title first-letter breakwords pr250'})
            order_payment = offer.find('div', {'class': 'wants-card__header-price wants-card__price m-hidden'})
            order_discription = offer.find('div', {'class': 'breakwords first-letter js-want-block-toggle js-want-block-toggle-full hidden'})
            customer = data.find('div', {'class': 'dib v-align-t ml10'})
            count_off = customer.find('div', {'class': 'dib v-align-t'}).text

            former = count_off.replace('\n', '').split()
            count_offers = f'{former[0]} {former[1]} {former[2]} {former[3]} {former[4]}'

            if former[-1] != '1':
                precent_orders = f'{former[-2]} {former[-1]}'
            else:
                precent_orders = 'Нету данных'

            if order_name is None:
                order_name = offer.find('div', {'class': 'wants-card__header-title first-letter breakwords pr200'})
                order_url = order_name.find('a').get('href')
            else:
                order_url = order_name.find('a').get('href')

            if order_discription is None:
                order_discription = offer.find('div', {'class': 'breakwords first-letter'}).text
            else:
                order_discription = order_discription.text.replace('Скрыть', '')

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


def create_log(name: str):
    with open('log/kwork.txt', 'w', encoding='utf-8') as file:
        file.write(name)


def read_log() -> str:
    try:
        with open('log/kwork.txt', 'r', encoding='utf-8') as file:
            log = file.read()

            return log
    except FileNotFoundError:
        try:
            os.mkdir('log')
        except FileExistsError:
            pass
