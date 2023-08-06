# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gwlad']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gwlad',
    'version': '0.0.0',
    'description': '',
    'long_description': '# gwlad\n\nGwlad! Gwlad!\n\n<br />\n\nModelling UK geography through the heights.\n',
    'author': 'ellsphillips',
    'author_email': 'elliott.phillips.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
