# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtmodel', 'dtmodel.bases', 'dtmodel.enums', 'dtmodel.models']

package_data = \
{'': ['*']}

install_requires = \
['bcrypt>=4.0.1,<5.0.0', 'dtfield>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'dtmodel',
    'version': '0.1.1',
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
