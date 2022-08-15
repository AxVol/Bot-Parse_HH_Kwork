from tkinter import E
import requests
import json

from bs4 import BeautifulSoup as BS


def parse() -> dict:
    response = requests.get('https://kwork.ru/projects?c=41').text
    soup = BS(response, 'lxml')
    block = soup.find('div', {'class': 'wants-content'})
    content = block.find_all('div', {'class': 'card__content pb5'})

    for data in content:
        offer = data.find('div', {'class': 'mb15'})
        order_name = offer.find('div', {'class': 'wants-card__header-title first-letter breakwords pr250'})
        order_payment = offer.find('div', {'class': 'wants-card__header-price wants-card__price m-hidden'})
        order_discription = offer.find('div', {'class': 'breakwords first-letter js-want-block-toggle js-want-block-toggle-full hidden'}).text.replace('Скрыть', '')
        customer = data.find('div', {'class': 'dib v-align-t ml10'})
        count_off = customer.find('div', {'class': 'dib v-align-t'}).text

        former = count_off.replace('\n', '').split()
        count_offers = f'{former[0]} {former[1]} {former[2]} {former[3]} {former[4]}'

        if former[-1] != '1':
            precent_orders = f'{former[-2]} {former[-1]}'
        else:
            precent_orders = 'Нету данных'

        if order_name == None:
            order_name = offer.find('div', {'class': 'wants-card__header-title first-letter breakwords pr200'})
            order_url = order_name.find('a').get('href')

            continue    

        order_url = order_name.find('a').get('href')

        #f'Заказ - {order_name.text}\nОписание - {order_discription}\n{order_payment.text}\n{count_offers}\n
        # {precent_orders}\n')


parse()