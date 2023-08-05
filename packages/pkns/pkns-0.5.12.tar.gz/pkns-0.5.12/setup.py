# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pkns']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'daemonocle>=1.2.3,<2.0.0',
 'dill>=0.3.3,<0.4.0',
 'pickle5>=0.0.11,<0.0.12',
 'pycryptodome>=3.10.1,<4.0.0',
 'sqlitedict==1.7.0']

entry_points = \
{'console_scripts': ['pkns = pkns.cli:main']}

setup_kwargs = {
    'name': 'pkns',
    'version': '0.5.12',
    'description': 'Public Key Name System Framework',
    'long_description': '\n# Public Key Name System Framework\n[![Made with Python3](https://img.shields.io/badge/Made%20With-Python3-blue)](https://www.python.org/) [![GitHub license](https://img.shields.io/badge/license-AGPLv3-purple.svg)](https://github.com/anubhav-narayan/PKNS/blob/master/LICENSE) [![PyPI](https://img.shields.io/pypi/v/pkns?color=green&label=version)]() [![Github status](https://img.shields.io/badge/status-Public%20Beta-green)\n](http://github.com/anubhav-narayan/PKNS) [![Made with](https://img.shields.io/badge/Built%20with-SQLite3%20|%20Click%20|%20Daemonocle%20|%20PyCryptodome-blue)](http://github.com/anubhav-narayan/PKNS)\\\nThis is the Public Key Name System Framework designed as a Public Key Exchange for both centralised and peer-to-peer services. It comes pre-built with useful and powerful CLI tools.\n## Installation\n### From source\nTo install from source use the following command, make sure you have `setuptools>=50.0.0`\n```bash\npython3 seutp.py install\n```\nTo install from PyPI\n```bash\npip3 install pkns\n```\n## Using the `PKNS_Table` API\nThe `PKNS_Table` API is the core for the PKNS Local Services found in the `pknscore`\n```python\nfrom pkns.pknscore import PKNS_Table\nnew_table = PKNS_Table(PATH_TO_A_TABLE_DIR)\n```\n `PATH_TO_A_TABLE` can be a path to an existing table directory or a new table directory, defaults to `~/.pkns`.\n The API provides all basic table operations.\n ## Using the `PKNS_Server` API\n The `PKNS_Server` API is the core of PKNS Network Services found in the  `pknscore`. It provides the correct server handling and configuration for a hosted PKNS Services. The PKNS service runs on the default port `6300` .  It is capable to handle multiple clients and process multiple requests and can be safely daemonized.\n ```python\n from pkns.pknscore import PKNS_Server\n server = PKNS_Server(IP_ADDR, PORT, PATH_TO_A_TABLE_DIR)\n ```\n `IP_ADDR` is the IP Address to use for the server, defaults to `0.0.0.0`,  `PORT` is the port to be used for the server, defaults to `6300`,  `PATH_TO_A_TABLE` can be a path to an existing table directory or a new table directory, defaults to `~/.pkns`.\n## Query Syntax\nPKNS Query is used for better integration of centralised servers. The query follows a fixed Syntax\n```\npkns://HOST_SERVER[:PORT][/PEERGROUP][/USER]\n```\n## CLI Tools\nCLI Tools help manage the PKNS Tables and Servers easily, they also include useful functions.\n###  Local Table Manager `tabman`\nManaging Local Tables\n```bash\n$ pkns tabman\nUsage: pkns tabman [OPTIONS] COMMAND [ARGS]...\n\n  PKNS Table Manager\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  add-peergroup     Add/Create a Peergroup\n  add-user          Add Users to a Peergroup\n  del-peergroup     Delete/Leave a Peergroup\n  del-user          Remove Users from a Peergroup\n  get-peergroup     Get Info of a Peergroup\n  get-user          Get Users Info from a Peergroup\n  rename-peergroup  Rename a Peergroup\n  rename-user       Rename a User from a Peergroup\n\n```\n### Server Manager `server`\nServer Utilities\n```bash\n$ pkns server\nUsage: pkns server [OPTIONS] COMMAND [ARGS]...\n\n  PKNS Server Manager\n\nOptions:\n  -i, --host TEXT     IP Address to bind  [default: 0.0.0.0]\n  -p, --port INTEGER  Port to bind  [default: 6300]\n  --help              Show this message and exit.\n\nCommands:\n  restart  Restart PKNS Server\n  start    Start the PKNS Server\n  status   PKNS Server Status\n  stop     Stop the PKNS Server\n\n```\n### Other utilities\n#### Ping\nPing a Local or Remote Server\n```bash\n$ pkns ping --help\nUsage: pkns ping [OPTIONS] [ADDRESS]\n\n  PKNS Ping\n\nOptions:\n  -n, --nop INTEGER  Number of Pings to send\n  --help             Show this message and exit.\n\n```\n#### Query\nQuery Local or Remote Server\n```bash\n$ pkns query --help\nUsage: pkns query [OPTIONS] QUERY\n\n  PKNS Query\n\nOptions:\n  --help  Show this message and exit.\n``` \n#### Sync\nSync to Local or Remote Server\n```bash\n$ pkns sync --help\nUsage: pkns sync [OPTIONS] [ADDRESS]\n\n  PKNS Sync\n\nOptions:\n  --help  Show this message and exit.\n```\n',
    'author': 'Anubhav Mattoo',
    'author_email': 'anubhavmattoo@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anubhav-narayan/PKNS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
