""" Модуль отвечающий за сбор данных с HeadHunter'a через его API и создание логов """
import os

from datetime import  datetime

import requests

from fake_useragent import UserAgent


def parse() -> dict:
    '''
    Функция отвечающая за обращение к API HH и вытягиванию нужных параметров в json файле,
    Фильтр для которых прописан в словарике "params"
    '''
    agent = UserAgent().random

    params = {
        'text': 'Python junior',
        'area': 2,
        'page': 0,
        'per_page': 100,
        'order_by': 'publication_time'
    }

    headers = {
        'User-Agent': agent
    }

    response = requests.get('https://api.hh.ru/vacancies', params=params, headers=headers)
    data = response.content.decode()

    return data


def create_log(date):
    '''
    Функция отвечающая за созднаие логов на основе времени последней вакансии,
    Чтобы при следующем запросе не получать повторные данные
    '''
    with open('log/headhunter.txt', 'w', encoding='utf-8') as file:
        log = former_time(str(date))

        file.write(str(log))


def read_log() -> datetime:
    '''Чтение логов.

    Так как чтение логов в боте встречается раньше чем запись,
    То тут добавлена проверка на существование пути,
    А так же на то, что другой модуль в программе уже мог создать эту папку.
    '''
    try:
        with open('log/headhunter.txt', 'r', encoding='utf-8') as file:
            log = file.read()

            if log is None:
                return log
            else:
                publish_time = former_time(log)

                return publish_time
    except FileNotFoundError:
        try:
            os.mkdir('log')
        except FileExistsError:
            return None


def former_time(date) -> datetime:
    '''
    Функция отвечающая за формирование человеко-понятного времени в логах,
    На случай если их надо будет проверить вручную
    '''
    format_time = "%Y-%m-%dT%H:%M:%S+%f"
    second_format = "%Y-%m-%d %H:%M:%S"
    new_time_format = "%Y-%m-%d %H:%M:%S.030000"

    try:
        date = datetime.strptime(date, format_time)
        date = datetime.strptime(str(date), new_time_format)

        return date
    except ValueError:
        if date == '':
            return None
        else:
            date = datetime.strptime(date, second_format)

            return date
