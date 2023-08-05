# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyral_django_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'cyral-django-wrapper',
    'version': '0.1.22',
    'description': 'Enriches your Django database queries with user identity information',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
