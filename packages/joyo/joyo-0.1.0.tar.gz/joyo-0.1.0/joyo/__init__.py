import pickle
from functools import lru_cache
from pathlib import Path
from typing import Final

import requests
from bs4 import BeautifulSoup

JOYO_PATH: Final[Path] = Path('joyo.pkl').absolute()


@lru_cache(maxsize=None)
def fetch_joyo():
    url = 'https://ja.wikipedia.org/wiki/%E5%B8%B8%E7%94%A8%E6%BC%A2%E5%AD%97%E4%B8%80%E8%A6%A7'
    resp = requests.get(url)
    assert 200 <= resp.status_code < 300
    soup = BeautifulSoup(resp.text, 'html.parser')

    tbody = soup.find('table', {'class': 'wikitable'}).find('tbody')
    trs = tbody.findAll('tr')[1:]
    s = ''
    for tr in trs:
        href = tr.find('a')
        s += href.text

    return s


def update(path: Path = JOYO_PATH) -> None:
    with open(str(path), 'wb') as f:
        pickle.dump(fetch_joyo(), f)


def load(path: Path = JOYO_PATH) -> str:
    if path.exists():
        with open(str(path), 'rb') as f:
            return pickle.load(f)
    else:
        update(path)
        return load(path)


if __name__ == '__main__':
    print(load())
