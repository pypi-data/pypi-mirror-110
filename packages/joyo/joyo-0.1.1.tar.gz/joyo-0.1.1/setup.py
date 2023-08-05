# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['joyo']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'flake8-quotes>=3.2.0,<4.0.0',
 'flake8>=3.8.4,<4.0.0',
 'invoke>=1.5.0,<2.0.0',
 'ipython>=7.20.0,<8.0.0',
 'isort>=5.7.0,<6.0.0',
 'mypy>=0.902,<0.903',
 'pudb>=2020.1,<2021.0',
 'py-term>=0.6,<0.7',
 'requests>=2.25.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'yapf>=0.30.0,<0.31.0']

setup_kwargs = {
    'name': 'joyo',
    'version': '0.1.1',
    'description': '',
    'long_description': "jyoyou\n===========\n\n![image](https://img.shields.io/pypi/v/joyo)\n![image](https://img.shields.io/pypi/pyversions/joyo)\n![image](https://gitlab.com/yassu/jyoyou.py/badges/master/pipeline.svg)\n![image](https://img.shields.io/pypi/l/joyo)\n\njyoyouは常用漢字一覧を取得するプロジェクトです.\n\n簡単な漢字の一覧を取得したい時などに使用できると思います.\n\n## 使い方\n\n`joyo.load`関数を使って常用漢字一覧を取得する. その際, 常用漢字一覧が取得されていなければ 取得する:\n\n``` python\nimport joyo\n\nkanjis = joyo.load()\nprint(kanjis)\n```\n\n出力:\n\n```\n亜哀挨愛曖悪握圧扱宛嵐安案暗以衣位囲医依委威為畏胃尉異移萎偉椅彙意違維慰遺緯域育一\n壱逸茨芋引印因咽姻員院淫陰飲隠韻右宇羽雨唄鬱畝浦運雲永泳英映栄営詠影鋭衛易疫益液駅\n悦越謁閲円延沿炎怨宴媛援園煙猿遠鉛塩演縁艶汚王凹央応往押旺欧殴桜翁奥横岡屋億憶臆虞\n乙俺卸音恩温穏下化火加可仮何花佳価果河苛科架夏家荷華菓貨渦過嫁暇禍靴寡歌箇稼課蚊牙\n瓦我画芽賀雅餓介回灰会快戒改怪拐悔海界皆械絵開階塊楷解潰壊懐諧貝外劾害崖涯街慨蓋該\n概骸垣柿各角拡革格核殻郭覚較隔閣確獲嚇穫学岳楽額顎掛潟括活喝渇割葛滑褐轄且株釜鎌刈\n干刊甘汗缶完肝官冠巻看陥乾勘患 ...\n...\n```\n\nパスを指定する:\n\n``` python\nfrom pathlib import Path\n\n\njoyo.load(Path('/tmp/abc'))\n```\n\n常用漢字一覧を更新する:\n\n``` python\njoyo.update()\n```\n\nパス名も指定できる:\n\n``` python\njoyo.update('/tmp/abc')\n```\n\n\nLICENSE\n-------\n\n[MIT](https://gitlab.com/yassu/jyoyou.py/-/blob/master/LICENSE)\n",
    'author': 'yassu',
    'author_email': 'yassu0320.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
