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
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'yassu',
    'author_email': 'yassu0320.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
