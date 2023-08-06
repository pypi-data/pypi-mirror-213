# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ergani']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ergani',
    'version': '0.1.0',
    'description': "Python SDK for the Greek government's Ergani API",
    'long_description': '# Ergani Python SDK\n\nThis repository will host a Python SDK for interacting with the API of [Ergani](https://www.gov.gr/en/ipiresies/ergasia-kai-asphalise/apozemioseis-kai-parokhes/prosopopoiemene-plerophorese-misthotou-ergane).\n\nTBD',
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@withlogic.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
