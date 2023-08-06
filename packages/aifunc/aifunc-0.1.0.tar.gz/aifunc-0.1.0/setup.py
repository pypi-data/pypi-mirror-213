# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aifunc']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.8,<0.28.0']

setup_kwargs = {
    'name': 'aifunc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
