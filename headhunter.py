import os

from datetime import  datetime

import requests

from fake_useragent import UserAgent


def parse() -> dict:
    ua = UserAgent().random

    params = {
        'text': 'Python junior',
        'area': 2,
        'page': 0,
        'per_page': 100,
        'order_by': 'publication_time'
    }

    headers = {
        'User-Agent': ua
    }

    response = requests.get('https://api.hh.ru/vacancies', params=params, headers=headers)
    data = response.content.decode()
    response.close()

    return data


def create_log(date):
    with open('log/headhunter.txt', 'w', encoding='utf-8') as file:
        log = former_time(str(date))

        file.write(str(log))


def read_log() -> datetime:
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
            pass


def former_time(date):
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
