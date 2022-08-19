""" Этот модуль отвечает за работу с гугл таблицами, чтением из них и записыванием """
from __future__ import print_function

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def write_sheet(fields: list, values: str, cred: str, sheet_id: str):
    """ Запись в таблтицу на основе переданных ей полей и данных которых надо записать в них """
    service = build('sheets', 'v4', credentials=cred)

    data = [{
        'range': fields,
        'values': values
    }]

    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }

    sheet = service.spreadsheets()
    sheet.values().batchUpdate(spreadsheetId=sheet_id,
                                body=body).execute()


def read_sheet(fields: list, cred: str, sheet_id: str):
    """
    Чтение данных из передаваемых полей, которые возвращаются в виде списка,
    И так как в моем случае нужно читать только одно поле, он его и забирает, если вам нужно больше,
    Измените цикл 'for row in values'
    """
    service = build('sheets', 'v4', credentials=cred)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=fields).execute()
    values = result.get('values', [])

    if not values:
        return None

    for row in values:
        result = row[0]

        return result


def main(todo: str, *args):
    """
    Соединение с API таблицы и получением токенов хранящихся в переменном окружении.
    """
    # При изменении этих областей удалите файл token.json.
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    # ID таблицы
    spreadsheet_id = os.getenv('SHEET')
    creds = None
    # В файле token.json хранятся токены доступа и обновления пользователя.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # Если нет доступных (действительных) учетных данных, позвольте пользователю войти в систему.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Сохраните учетные данные для следующего запуска
        with open('token.json', 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    #Проверки на то, какие функции нужно выполнять
    try:
        if todo == 'read':
            if args[0] == 'Kwork':
                range_name = 'logs!B1'
            elif args[0] == 'HeadHunter':
                range_name = 'logs!A1'

            result = read_sheet(range_name, creds, spreadsheet_id)

            return result

        elif todo == 'write':
            if args[1] == 'Kwork':
                range_name = 'logs!B1'
            elif args[1] == 'HeadHunter':
                range_name = 'logs!A1'

            writer = [[args[0]]]

            write_sheet(range_name, writer, creds, spreadsheet_id)

    except HttpError as err:
        print(err)
