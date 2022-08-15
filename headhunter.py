import requests
import os

from fake_useragent import UserAgent


def parse() -> dict:
    ua = UserAgent().random

    params = {
        'text': 'Python junior',
        'area': 2,
        'page': 0,
        'per_page': 100,
    }

    headers = {
        'User-Agent': ua
    }

    response = requests.get('https://api.hh.ru/vacancies', params=params, headers=headers)
    data = response.content.decode()
    response.close()

    return data


def create_log(date: str):
    with open('log/headhunter.txt', 'w', encoding='utf-8') as f:
        f.write(date)


def read_log() -> str:
    try:
        with open('log/headhunter.txt', 'r', encoding='utf-8') as f:
            log = f.read()

            return log
    except:
        os.mkdir('log')