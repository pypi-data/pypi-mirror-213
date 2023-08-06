# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mappr', 'mappr.integrations']

package_data = \
{'': ['*']}

install_requires = \
['peltak-changelog>=0.0.4,<0.0.5', 'peltak-todos>=0.0.10,<0.0.11']

setup_kwargs = {
    'name': 'mappr',
    'version': '0.3.5',
    'description': '',
    'long_description': None,
    'author': 'Mateusz Klos',
    'author_email': 'novopl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://novopl.github.io/mappr',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
