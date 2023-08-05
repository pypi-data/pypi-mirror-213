# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = ['client']

package_data = {'': ['*']}

install_requires = ['scramjet-client-utils>=1.1.0']

setup_kwargs = {
    'name': 'scramjet-api-client',
    'version': '1.1.0',
    'description': '',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'author': 'Scramjet',
    'author_email': 'open-source@scramjet.org',
    'url': 'https://github.com/scramjetorg/api-client-python/tree/main/client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
