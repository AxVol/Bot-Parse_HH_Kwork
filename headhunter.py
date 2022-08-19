""" Модуль отвечающий за сбор данных с HeadHunter'a через его API и создание логов """
#import os

from datetime import  datetime

import requests

from fake_useragent import UserAgent

import connect_sheet


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


# Если вы не хотите настраивать подключение к гугл таблицам для ведения логов,
# (Мне так было удобнее, для взаимодествие с ботом когда он лежит на сервере),
# То просто закомментируйте соответствующие строки, а раскомментируйте те,
# Которые отвечают за запись в локальный файл txt

# ******* Не забудьте раскомментировать импорт модуля os

def create_log(date: datetime, headhunter: str):
    '''
    Функция отвечающая за созднаие логов на основе времени последней вакансии,
    Чтобы при следующем запросе не получать повторные данные
    '''

    log = former_time(str(date))

    connect_sheet.main('write', str(log), headhunter)

    # with open('log/headhunter.txt', 'w', encoding='utf-8') as file:
    #     log = former_time(str(date))

    #     file.write(str(log))


def read_log(headhunter: str) -> datetime:
    '''Чтение логов.

    *** Это при условии что вы используете локальную запись файлов

    Так как чтение логов в боте встречается раньше чем запись,
    То тут добавлена проверка на существование пути,
    А так же на то, что другой модуль в программе уже мог создать эту папку.
    '''

    result = connect_sheet.main('read', headhunter)

    if result is None:
        return None
    else:
        publish_time = former_time(result)

        return publish_time

    # try:
    #     with open('log/headhunter.txt', 'r', encoding='utf-8') as file:
    #         log = file.read()

    #         if log is None:
    #             return log
    #         else:
    #             publish_time = former_time(log)

    #             return publish_time
    # except FileNotFoundError:
    #     try:
    #         os.mkdir('log')
    #     except FileExistsError:
    #         return None


def former_time(date: str) -> datetime:
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
