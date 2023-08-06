# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['superinvoke',
 'superinvoke.collections',
 'superinvoke.extensions',
 'superinvoke.objects']

package_data = \
{'': ['*']}

install_requires = \
['download==0.3.5', 'neoxelox-invoke==2.0.0', 'rich==12.5.1']

setup_kwargs = {
    'name': 'superinvoke',
    'version': '1.0.2',
    'description': 'An Invoke wrapper with extra handy features.',
    'long_description': '# superinvoke\n\nAn Invoke wrapper with extra handy features.\n\nTODO: EXPLAIN\n',
    'author': 'Alex',
    'author_email': 'alex@neoxelox.com',
    'maintainer': 'Alex',
    'maintainer_email': 'alex@neoxelox.com',
    'url': 'https://github.com/neoxelox/superinvoke',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
