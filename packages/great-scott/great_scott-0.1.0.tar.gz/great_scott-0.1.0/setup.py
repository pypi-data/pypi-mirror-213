# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['great_scott']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['great-scott = great_scott.__main__:main']}

setup_kwargs = {
    'name': 'great-scott',
    'version': '0.1.0',
    'description': 'Automatically reverses Django migrations when changing git branches',
    'long_description': '<div align="center">\n\n# great-scott\n\n`great-scott` is a tool that can automatically reverse migrations in a Django project, when switching between different GIT branches.\n\n[Installation](#installation) •\n[Usage](#usage) •\n[Removing GIT hooks](#removing-git-hooks)\n\n![doc](img/doc.jpeg)\n\n</div>\n\n\n## Installation\n\n`great-scott` can be installed in 2 easy steps:\n\n1. **Install the tool**\n \n   I recommend installing via [pipx](https://github.com/pypa/pipx):\n   ```sh\n   pipx install great-scott\n   ```\n\n   Alternatively, having the project\'s virtual-env activated, you can of course install the tool directly into virtual-env:\n   ```sh\n   python -m pip install great-scott\n   ```\n\n2. **Setup GIT hooks**\n\n   After successful installation, while in the GIT-managed project folder and with virtual-env activated, execute:\n   ```sh\n   great-scott install\n   ```\n\n\n## Usage\n\nReversing migrations should simply work when the GIT branch is changed:\n\n```sh\n$ git checkout mig-test\nSwitched to branch \'main\'\n👀 Looking for migrations to reverse on mig-test...\n⚠️ reversing migrations for importer (up to 0015)\n⚠️ reversing migrations for permissions (up to 0018)\n⚠️ reversing migrations for subscriptions (up to 0044)\nI have reversed migrations for 3 apps!\n```\n\n👉 If you use GIT integration in any of the popular IDEs, such as PyCharm or VSCode, don\'t forget to properly configure the appropriate python environment there so that automatic reversing of migrations is possible.\n\n\n## Removing GIT hooks\n\nTo remove the GIT hooks, execute the command (while in the project directory and with virtual-env activated):\n```sh\ngreat-scott uninstall\n```\n',
    'author': 'Marcin Górecki',
    'author_email': 'marcin.gorecki@hey.com',
    'maintainer': 'Marcin Górecki',
    'maintainer_email': 'marcin.gorecki@hey.com',
    'url': 'https://github.com/goreckim/great-scott',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
