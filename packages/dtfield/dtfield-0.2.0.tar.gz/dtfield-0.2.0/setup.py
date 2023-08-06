# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtfield', 'dtfield.parse']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.6,<2.0.0',
 'anyio>=3.7.0,<4.0.0',
 'dtbase>=0.0.4,<0.0.5',
 'typing-extensions>=4.6.3,<5.0.0',
 'uvicorn>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'dtfield',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
