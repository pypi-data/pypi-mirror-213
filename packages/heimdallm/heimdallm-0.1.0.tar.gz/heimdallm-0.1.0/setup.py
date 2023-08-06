# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heimdallm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'heimdallm',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Andrew Moffat',
    'author_email': 'arwmoffat@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
