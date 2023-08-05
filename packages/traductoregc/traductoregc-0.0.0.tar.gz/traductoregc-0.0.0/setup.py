# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traductoregc', 'traductoregc.matematicas']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'traductoregc',
    'version': '0.0.0',
    'description': 'Traductor de palabras',
    'long_description': None,
    'author': 'Edison Gaibor',
    'author_email': 'edisongaiborconde@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
