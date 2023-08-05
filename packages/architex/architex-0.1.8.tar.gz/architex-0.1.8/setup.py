# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['architex']

package_data = \
{'': ['*']}

install_requires = \
['colorama==0.4.4',
 'crossplane>=0.5.8,<0.6.0',
 'diagrams>=0.23.3,<0.24.0',
 'pytest==6.2.4',
 'pyyaml>=5.0,<6.0',
 'shellingham==1.4.0',
 'typer==0.3.2']

setup_kwargs = {
    'name': 'architex',
    'version': '0.1.8',
    'description': 'Draw your software architecture diagram automagically',
    'long_description': 'A package to auto draw your software architecture diagram from your source code.\n\nCurrent limitation :\nYour source code should be consist of docker compose (required) and nginx (optional) configuration file.\n',
    'author': 'Miko',
    'author_email': 'jherjati@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
