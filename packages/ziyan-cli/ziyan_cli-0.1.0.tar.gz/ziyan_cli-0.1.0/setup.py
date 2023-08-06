# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ziyan_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ziyan-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ziyan wu',
    'author_email': 'ziyanwu93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
