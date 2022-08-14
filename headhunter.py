import requests
import json

from fake_useragent import UserAgent


def parse() -> json:
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


def main() -> json:
    JsonObject = json.loads(parse()) 

    with open('json/headhunter.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(JsonObject, ensure_ascii=False))

    with open('log/headhunter.txt', 'w', encoding='utf-8') as f:
        log = JsonObject['items'][0]['published_at']
        f.write(log)


if __name__ == '__main__': #NAME, ADRESS, published_at, url, snippet(requirement, responsibility) Schedule(name), 
    main()                 # salary(from, to, currency)