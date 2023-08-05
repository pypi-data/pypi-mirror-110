# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vox_logstash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vox-logstash',
    'version': '0.1.0',
    'description': 'python logs integration with logstash',
    'long_description': None,
    'author': 'Jhonatan Teixeira',
    'author_email': 'jhonatan.teixeira@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
