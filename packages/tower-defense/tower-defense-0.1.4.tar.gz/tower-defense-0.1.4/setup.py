# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tower_defense']

package_data = \
{'': ['*'], 'tower_defense': ['Resources/*']}

install_requires = \
['pygame>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['tower-defense = tower_defense.main:app']}

setup_kwargs = {
    'name': 'tower-defense',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Ying Liqian',
    'author_email': 'jamesylq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
