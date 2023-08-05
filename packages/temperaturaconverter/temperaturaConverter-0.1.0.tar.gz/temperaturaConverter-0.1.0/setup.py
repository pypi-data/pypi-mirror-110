# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temperaturaconverter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['temperaturaConverter = '
                     'temperaturaconverter.temperaturaConverter:F_to_K, '
                     'C_to_R, C_to_F']}

setup_kwargs = {
    'name': 'temperaturaconverter',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'chjuca',
    'author_email': 'chjuca@utpl.edu.ec',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
