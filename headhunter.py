import requests
import fake_useragent

Agent = fake_useragent.UserAgent().random

data = {
    'area': '2',
    'clusters': 'true',
    'enable_snippets': 'true',
    'ored_clusters': 'true',
    'professional_role': '96',
    'professional_role': '116',
    'professional_role': '124',
    'text': 'Python junior',
    'search_period': '1',
    'hhtmFrom': 'vacancy_search_list'
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '__ddg1_=Jn0GhMVor2FdP4czxpDc; _xsrf=92adaf0cd25988f65abb10390cface27; redirect_host=spb.hh.ru; hhtoken=IfJ7g0Fx7I3MR8o7WcAJFFVYEq5y; hhuid=Rqgywyp8OnULY2KkUKIskg--; hhrole=anonymous; regions=2; region_clarified=NOT_SET; display=desktop; GMT=3; _ym_d=1654935717; _ym_uid=16214037671025711407; tmr_lvid=70969a680703e285e890731399f8be26; tmr_lvidTS=1621403766972; iap.uid=6652b037de924cf38a865a3ce11ec821; __zzatgib-w-hh=MDA0dBA=Fz2+aQ==; __zzatgib-w-hh=MDA0dBA=Fz2+aQ==; _gid=GA1.2.603144835.1660302140; _ym_isad=2; _ga_44H5WGZ123=GS1.1.c313dfbe25e529e43fca8af3f7fd533f830bd3c4fd7c90d4fa3e5dcfb6595354.6.1.1660302276.60; _ga=GA1.2.380235065.1654935718; tmr_detect=0|1660302278958; _gali=HH-React-Root; cfidsgib-w-hh=rkzCllRQoAti9lhfmRT+YZqKerXXn552xpdTICCu3G93rwjWTEV/+cXKKpZQPn2HecC3+cu5sJ/usI/gjbnpEM07s7Ydk8zOq53cn9WhYM37LkklksL6DKcZUnEpY/+ui15gy2fY6jAtFcgKxJVneyXzkM9GsxBYmOOFmA==; gssc58=; cfidsgib-w-hh=rkzCllRQoAti9lhfmRT+YZqKerXXn552xpdTICCu3G93rwjWTEV/+cXKKpZQPn2HecC3+cu5sJ/usI/gjbnpEM07s7Ydk8zOq53cn9WhYM37LkklksL6DKcZUnEpY/+ui15gy2fY6jAtFcgKxJVneyXzkM9GsxBYmOOFmA==; cfidsgib-w-hh=rkzCllRQoAti9lhfmRT+YZqKerXXn552xpdTICCu3G93rwjWTEV/+cXKKpZQPn2HecC3+cu5sJ/usI/gjbnpEM07s7Ydk8zOq53cn9WhYM37LkklksL6DKcZUnEpY/+ui15gy2fY6jAtFcgKxJVneyXzkM9GsxBYmOOFmA==; gsscgib-w-hh=eyhAv1Etw59hxdsMYOW0gzYKPDM1z2vDr+cDP3q0XT7z7s25XRr8KfZQpVWNIsTq2V8qYURQdkOjlWGrxI+w9eRq3pqTSJ7BpU3ZCNKQEsuLILrJKGrxTmA7d1VBFCqw/+0DaiBZ7WQLGCY+UaZN1yFMo5VBlKrL5zZKef7HtZu25K4jUl0vb0ykFTKrQKayxCdBxmQdGgo39IGqqaBJDcYSNXxoym9xmWyrv8TlxlZhNipLDqc4Hgw49uzP2ho=; gsscgib-w-hh=eyhAv1Etw59hxdsMYOW0gzYKPDM1z2vDr+cDP3q0XT7z7s25XRr8KfZQpVWNIsTq2V8qYURQdkOjlWGrxI+w9eRq3pqTSJ7BpU3ZCNKQEsuLILrJKGrxTmA7d1VBFCqw/+0DaiBZ7WQLGCY+UaZN1yFMo5VBlKrL5zZKef7HtZu25K4jUl0vb0ykFTKrQKayxCdBxmQdGgo39IGqqaBJDcYSNXxoym9xmWyrv8TlxlZhNipLDqc4Hgw49uzP2ho=; total_searches=12; tmr_reqNum=181; fgsscgib-w-hh=Gre3026f4c9029a7a8573ce7f2e434303f5aeb43; fgsscgib-w-hh=Gre3026f4c9029a7a8573ce7f2e434303f5aeb43',
    'user-agent': Agent
}

response = requests.get('https://spb.hh.ru', data=data, headers=headers)
print(response)