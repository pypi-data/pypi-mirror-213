# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biochatter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'biochatter',
    'version': '0.0.0',
    'description': 'Backend library for conversational AI in biomedicine',
    'long_description': '# biochatter\nThis repository will become a backend library for the connection of biomedical applications to conversational AI. Check back soon.\n',
    'author': 'Sebastian Lobentanzer',
    'author_email': 'sebastian.lobentanzer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
