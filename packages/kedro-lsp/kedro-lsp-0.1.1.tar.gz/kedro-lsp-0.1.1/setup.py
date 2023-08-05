# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kedro_lsp']

package_data = \
{'': ['*']}

install_requires = \
['kedro>=0.17.3,<0.18.0', 'pygls>=0.10.3,<0.11.0']

entry_points = \
{'console_scripts': ['kedro-lsp = kedro_lsp.cli:cli']}

setup_kwargs = {
    'name': 'kedro-lsp',
    'version': '0.1.1',
    'description': 'Kedro Language Server',
    'long_description': '# kedro-lsp\n\nA [Language Server](https://microsoft.github.io/language-server-protocol/) for the latest version(s) of [Kedro](https://kedro.readthedocs.io/en/latest/). It provides features to enable IDE support for Kedro. For example, you can jump to dataset and parameter definition when constructing the pipeline.\n\n![](./assets/demo.gif)\n\n**Note**: This is pre-alpha software.\n\n## Features\n\n* [x] Provide dataset and parameter definition when constructing the pipeline.\n\n> **Note**: I need your help! If you think this project is a good idea, please submit features request via Github Issue.\n\n## Compatibility\n\nKedro Language Server aims to be compatible with Kedro 0.17.x and above. Currently it is restricted to 0.17.3 and above during pre-alpha phase.\n\n## Installation\n\n```shell\npip install kedro-lsp\n```\n\n## Usage\n\n### Standlone\n\n```\nusage: kedro-lsp [-h] [--version] [--tcp] [--host HOST] [--port PORT] [--log-file LOG_FILE] [-v]\n\nKedro Language Server: an LSP wrapper for Kedro.\n\noptional arguments:\n  -h, --help           show this help message and exit\n  --version            display version information and exit\n  --tcp                use TCP server instead of stdio\n  --host HOST          host for TCP server (default 127.0.0.1)\n  --port PORT          port for TCP server (default 2087)\n  --log-file LOG_FILE  redirect logs to the given file instead of writing to stderr\n  -v, --verbose        increase verbosity of log output\n\nExamples:\n    Run from stdio: kedro-lsp\n```\n\n### Visual Studio Code\n\nTo use it with visual studio code, install the Kedro extension from Visual Studio Code Marketplace.\n\n### Pycharm\n\nTBD\n\n## Todos\n\n* [ ] Provide diagnostic when there is a typo in dataset or parameter name in the pipeline.\n* [ ] Be Kedro environment-aware\n\n## License\n\nMIT\n',
    'author': 'Lim Hoang',
    'author_email': 'limdauto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kedro-Zero-to-Hero/kedro-lsp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.9',
}


setup(**setup_kwargs)
