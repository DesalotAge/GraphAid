import requests
import threading
import time
import pandas as pd
import sys
from typing import Optional
from utils import models

HOST = 'https://www.tks.ru/'


def get_rw_urls() -> list[str]:

    not_used_pages = set(range(1, 86))
    ans = []

    def request_for_page(page: int) -> requests.Request:
        return requests.get(
            HOST +
            f'db/rwstation?mode=search&second=x&page={page}&kodstan='
            f'&naimstan=&koddor=&kodotd=&kodtam=&namt=&freight='
        )

    def load_by_page(page: int) -> list[str]:
        nonlocal ans
        url_list = []

        retrieve = 70

        res = request_for_page(page)

        while retrieve > 0 and res.status_code != 200:
            res = request_for_page(page)
            retrieve -= 1
        # print(res)
        html_doc = res.text

        for after_correct_url_beginning in html_doc.split('/db/rwstation/'):
            cur_id = ''
            for i in after_correct_url_beginning:
                if i.isnumeric():
                    cur_id += i
                else:
                    break

            if cur_id:
                url_list.append('/db/rwstation/' + cur_id)
        ans += list(set(url_list))
        not_used_pages.remove(page)
        return url_list

    for page in range(1, 86):
        t = threading.Thread(target=load_by_page, args=(page, ))
        t.start()

    # waiting all threads to end

    while len(not_used_pages):
        pass

    return list(set(ans))


def get_stations_info(url_list: list[str]) -> list[models.Station]:

    url_set = set(url_list)
    assert len(url_list) == len(url_set)
    ans = []
    thread_counter = 0

    def get_info_about_station(url: str) -> models.Station:
        nonlocal ans
        nonlocal thread_counter

        def get_page() -> requests.Response:
            retrieve = 70
            res = requests.get(HOST + url[1:])
            while res.status_code != 200 and retrieve > 0:
                retrieve -= 1
                try:
                    res = requests.get(HOST + url[1:])
                except Exception as e:
                    print(e, file=sys.stderr)
            return res

        def get_info(html: str) -> str:
            return html.split('<td width="70%">')[1].split('</td>')[0].strip()

        html_page = get_page().text
        possible_values = html_page.split('tr>')
        name, id, railway, customhouse = [None] * 4

        for incide in possible_values:
            if '<td width="70%">' in incide:
                if 'Наименование ж/д станции' in incide:
                    name = get_info(incide)
                elif 'Код ж/д станции' in incide:
                    id = get_info(incide)
                elif 'Железная дорога' in incide:
                    railway = get_info(incide)
                elif 'Адрес таможни' in incide:
                    customhouse = get_info(incide)

        info = models.Station(name=name, id=id, railway=railway, customhouse=customhouse, x_coord=None, y_coord=None)
        print(url, name, id, railway, customhouse, sep=';')

        thread_counter -= 1
        ans.append(info)
        url_set.remove(url)
        return info

    for url in url_list:
        t = threading.Thread(target=get_info_about_station, args=(url,))
        thread_counter += 1
        t.start()
        while thread_counter > 10:
            pass

    time.sleep(10)

    return ans


def add_coords2stations(stations_list: pd.DataFrame) -> list[models.Station]:

    completed_threads = 0
    current_threads = 0
    ans = []

    def decode_address2coords(address: str) -> str:
        nonlocal  current_threads
        # print(address)

        data = requests.get(f'https://geocode-maps.yandex.ru/1.x/'
                            f'?apikey={os.environ.get("api-key")}'
                            f'&format=json&geocode={address}')
        retrieve = 70
        while retrieve > 0 and data.status_code != 200:
            data = requests.get(f'https://geocode-maps.yandex.ru/1.x/'
                                f'?apikey={os.environ.get("api-key")}'
                                f'&format=json&geocode={address}')
            retrieve -= 1
        if len(data.json()['response']['GeoObjectCollection']['featureMember']) == 0:
            return None
        return tuple(
            map(
                float,
                data.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[::-1]
            )
        )

    def fill_coords(station: models.Station) -> Optional[models.Station]:
        nonlocal current_threads, completed_threads, ans

        if isinstance(station.customhouse, str):
            coords = decode_address2coords("Железнодорожная станци " + station.name.title())
        else:
            current_threads -= 1
            completed_threads += 1
            return None

        if coords is None:
            current_threads -= 1
            completed_threads += 1
            return None
        # print(coords)
        station_copy = models.Station(
            id=station.id,
            name=station.name,
            customhouse=station.customhouse,
            railway=station.railway,
            x_coord=coords[0],
            y_coord=coords[1],
        )
        ans.append(station_copy)
        current_threads -= 1
        completed_threads += 1
        return station_copy

    for station_id_in_list in range(len(stations_list)):
    # for  station_id_in_list in range(100):
        t = threading.Thread(target=fill_coords, args=(
                models.Station(
                    id=stations_list.at[station_id_in_list, 'id'],
                    railway=stations_list.at[station_id_in_list, 'railway'],
                    customhouse=stations_list.at[station_id_in_list, 'customhouse'],
                    name=stations_list.at[station_id_in_list, 'name'],
                    x_coord=None,
                    y_coord=None
                ),
            )
        )
        t.start()
        current_threads += 1

        while current_threads > 10:
            pass

    while current_threads != 0:
        pass
    return ans


