# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poet', 'poet.poet', 'poet.tests']

package_data = \
{'': ['*']}

install_requires = \
['binance>=0.3,<0.4',
 'coda>=0.1.0,<0.2.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.20.3,<2.0.0']

setup_kwargs = {
    'name': 'crypto-project',
    'version': '0.1.0',
    'description': 'Crypto production',
    'long_description': None,
    'author': 'Melo & Deemz',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
