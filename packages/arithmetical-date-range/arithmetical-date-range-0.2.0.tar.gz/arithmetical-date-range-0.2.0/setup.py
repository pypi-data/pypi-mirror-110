# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['arithmetical_date_range']
setup_kwargs = {
    'name': 'arithmetical-date-range',
    'version': '0.2.0',
    'description': 'Add an subtract date ranges',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
