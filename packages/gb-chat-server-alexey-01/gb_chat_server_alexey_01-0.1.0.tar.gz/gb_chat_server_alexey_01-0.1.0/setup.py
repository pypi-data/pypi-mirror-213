# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['server', 'server.log']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=5.1.0,<6.0.0',
 'cx-freeze>=6.15.1,<7.0.0',
 'pyqt5-tools>=5.15.9.3.3,<6.0.0.0.0',
 'pyqt5>=5.15.9,<6.0.0',
 'pyyaml>=6.0,<7.0',
 'sphinx>=7.0.1,<8.0.0',
 'sqlalchemy==1.4.46',
 'tabulate>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'gb-chat-server-alexey-01',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Messenger\n\nУчебный проект\n\n## Стек\n\n- Python > 3.7\n- VSCode\n- SQLite 3\n\n## Лицензия\n\nMIT',
    'author': 'Alexey Ryzhkov',
    'author_email': 'aler32@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
