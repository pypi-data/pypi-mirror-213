# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fixieai',
 'fixieai.agents',
 'fixieai.cli',
 'fixieai.cli.agent',
 'fixieai.cli.auth',
 'fixieai.cli.session',
 'fixieai.client']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.13,<2.0.0',
 'Pillow',
 'PyJWT[crypto]>=2.6.0,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'fastapi>=0.89.1,<0.90.0',
 'gql[requests]>=3.4.1,<4.0.0',
 'oauth2-client>=1.3.0,<2.0.0',
 'packaging>=23.0,<24.0',
 'prompt-toolkit',
 'pydantic>=1.10.8',
 'python-dotenv>=1.0.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'types-Deprecated>=1.2.9.2,<2.0.0.0',
 'uvicorn[standard]>=0.20.0,<0.21.0',
 'validators>=0.20.0,<0.21.0',
 'watchfiles>=0.19.0,<0.20.0',
 'wrapt>=1.15.0,<2.0.0']

entry_points = \
{'console_scripts': ['fixie = fixieai.cli.cli:fixie',
                     'fixieai = fixieai.cli.cli:fixie']}

setup_kwargs = {
    'name': 'fixieai',
    'version': '1.0.0',
    'description': 'SDK for the Fixie.ai platform. See: https://fixie.ai',
    'long_description': 'None',
    'author': 'Fixie.ai Team',
    'author_email': 'hello@fixie.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
