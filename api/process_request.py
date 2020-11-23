import datetime

import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError

from .models import Record


def process_request(code):
    zakupki_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    _headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Authorization": "Basic Z2FyYW50QGFrYml6LnJ1OjJUalhFNWJq",
        "Cookie": "JSESSIONID=nhzf83k7uune3ngbuvxke16p",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    zakupki_req_addr = f'https://zakupki.gov.ru/epz/ktru/search/results.html?searchString={code}&morphology=on'
    _req_addr = f''
    query = Record.objects.filter(okpd=code).first()
    if query and \
            query.date_changed.replace(tzinfo=None) > datetime.datetime.utcnow() - datetime.timedelta(hours=2) \
            and query.ktru_records_count != 'Код не найден':
        return {'status': 'Valid'}
    else:
        got_result = False
        while not got_result:
            time_delay = datetime.datetime.utcnow()
            content_zak = requests.get(zakupki_req_addr, headers=zakupki_headers)
            content = requests.get(_req_addr, headers=_headers)
            if time_delay < datetime.datetime.utcnow() - datetime.timedelta(seconds=30):
                return False
            if content_zak.status_code == requests.codes.ok and content.status_code == requests.codes.ok:
                got_result = True
                try:
                    _resp_dict = content.json()['models'][0].copy()
                except IndexError:
                    rec = Record(okpd=code,
                                 ktru_records_count='Код не найден',
                                 isCanceled=False,
                                 zapret='0',
                                 ogranichenia='0',
                                 preimuschestvo='0',
                                 dopusk='0',
                                 perechen='0',
                                 forma='0',
                                 tk='0',
                                 efektivnost='0',
                                 perechenTryUIS='0',
                                 nepubl='0',
                                 got_results=True
                                 )
                    try:
                        rec.save()
                        return {'status': 'Not found'}
                    except IntegrityError:
                        pass
                        return {'status': 'Not found saving error'}
                # Zakupki
                soup = BeautifulSoup(content_zak.text, "html5lib")
                element = soup.find("div", class_="search-results__total")

                #

                if query:
                    query.date_changed = datetime.datetime.utcnow()
                    query.save()
                    return {'status': 'Refreshed'}
                else:
                    rec = Record(okpd=code,
                                 ktru_records_count=element.text.strip(),
                                 isCanceled=any([_resp_dict['isCanceled'], 'Исключен' in _resp_dict['name']]),
                                 zapret=_resp_dict['zapret'],
                                 ogranichenia=_resp_dict['ogranichenia'],
                                 preimuschestvo=_resp_dict['preimuschestvo'],
                                 dopusk=_resp_dict['dopusk'],
                                 perechen=_resp_dict['perechen'],
                                 forma=_resp_dict['forma'],
                                 tk=_resp_dict['tk'],
                                 efektivnost=_resp_dict['efektivnost'],
                                 perechenTryUIS=_resp_dict['perechenTry'],
                                 nepubl=_resp_dict['nePazmeschaetncya'],
                                 got_results=True
                                 )
                    try:
                        rec.save()
                        return {'status': 'Created'}
                    except IntegrityError:
                        pass
                        return {'status': 'Error while saving cancelled'}
            else:
                return {'status': 'General error'}