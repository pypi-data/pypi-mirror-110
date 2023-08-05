# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miditeach', 'miditeach.views']

package_data = \
{'': ['*'], 'miditeach': ['assets/images/*', 'assets/sounds/*', 'stats/*']}

install_requires = \
['arcade>=2.5.7,<3.0.0', 'mido>=1.2.10,<2.0.0', 'python-rtmidi>=1.4.9,<2.0.0']

entry_points = \
{'console_scripts': ['miditeach = miditeach.miditeach:main']}

setup_kwargs = {
    'name': 'miditeach',
    'version': '0.6',
    'description': '',
    'long_description': None,
    'author': 'Alexis LOUIS',
    'author_email': 'alelouis.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
