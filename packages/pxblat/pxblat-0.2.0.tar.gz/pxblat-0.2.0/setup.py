# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pxblat', 'pxblat.cli', 'pxblat.extc', 'pxblat.server', 'pxblat.toolkit']

package_data = \
{'': ['*'],
 'pxblat.extc': ['bindings/*',
                 'bindings/binder/*',
                 'include/*',
                 'include/aux/*',
                 'include/core/*',
                 'include/net/*',
                 'src/*',
                 'src/aux/*',
                 'src/core/*',
                 'src/net/*']}

install_requires = \
['biopython>=1.81,<2.0',
 'deprecated>=1.2.13,<2.0.0',
 'loguru>=0.7.0,<0.8.0',
 'mashumaro>=3.7,<4.0',
 'numpy>=1.24.3,<2.0.0',
 'pybind11>=2.10.4,<3.0.0',
 'pysimdjson>=5.0.2,<6.0.0',
 'rich>=13.3.5,<14.0.0',
 'setuptools>=67.7.2,<68.0.0',
 'typer>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['pxblat = pxblat.cli.cli:app']}

setup_kwargs = {
    'name': 'pxblat',
    'version': '0.2.0',
    'description': 'A native python binding for blat suit',
    'long_description': '# <img src="https://raw.githubusercontent.com/cauliyang/pxblat/main/docs/_static/logo.png" alt="logo" height=100> **PxBLAT** [![social](https://img.shields.io/github/stars/cauliyang/pxblat?style=social)](https://github.com/cauliyang/pxblat/stargazers)\n\n_An Efficient and Ergonomics Python Binding Library for BLAT_\n\n[![python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)](https://www.python.org/)\n[![c++](https://img.shields.io/badge/C++-00599C.svg?style=for-the-badge&logo=C++&logoColor=white)](https://en.cppreference.com/w/)\n[![c](https://img.shields.io/badge/C-A8B9CC.svg?style=for-the-badge&logo=C&logoColor=black)](https://www.gnu.org/software/gnu-c-manual/)\n[![pypi](https://img.shields.io/pypi/v/pxblat.svg?style=for-the-badge)](https://pypi.org/project/pxblat/)\n[![pyversion](https://img.shields.io/pypi/pyversions/pxblat?style=for-the-badge)](https://pypi.org/project/pxblat/)\n[![license](https://img.shields.io/pypi/l/pxblat?style=for-the-badge)](https://opensource.org/licenses/mit)\n[![precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)\n[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json&style=for-the-badge)](https://github.com/charliermarsh/ruff)\n[![download](https://img.shields.io/pypi/dm/pxblat?style=for-the-badge)](https://pypi.org/project/pxblat/)\n[![Codecov](https://img.shields.io/codecov/c/github/cauliyang/pxblat/main?style=for-the-badge)](https://app.codecov.io/gh/cauliyang/pxblat)\n[![docs](https://img.shields.io/readthedocs/pxblat?style=for-the-badge)](https://pxblat.readthedocs.io/en/latest/)\n[![release](https://img.shields.io/github/release-date/cauliyang/pxblat?style=for-the-badge)](https://github.com/cauliyang/pxblat/releases)\n[![open-issue](https://img.shields.io/github/issues-raw/cauliyang/pxblat?style=for-the-badge)](https://github.com/cauliyang/pxblat/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc)\n[![close-issue](https://img.shields.io/github/issues-closed-raw/cauliyang/pxblat?style=for-the-badge)][close-issue]\n[![activity](https://img.shields.io/github/commit-activity/m/cauliyang/pxblat?style=for-the-badge)][repo]\n[![lastcommit](https://img.shields.io/github/last-commit/cauliyang/pxblat?style=for-the-badge)][repo]\n[![opull](https://img.shields.io/github/issues-pr-raw/cauliyang/pxblat?style=for-the-badge)][opull]\n[![tests](https://github.com/cauliyang/pxblat/actions/workflows/tests.yml/badge.svg?style=for-the-badge)](https://github.com/cauliyang/pxblat/actions/workflows/tests.yml)\n[![all contributors](https://img.shields.io/github/all-contributors/cauliyang/pxblat?style=for-the-badge)](#contributors)\n\n[repo]: https://github.com/cauliyang/pxblat\n[close-issue]: https://github.com/cauliyang/pxblat/issues?q=is%3Aissue+sort%3Aupdated-desc+is%3Aclosed\n[opull]: https://github.com/cauliyang/pxblat/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc\n\n## 📚 **Table of Contents**\n\n- [📚 Table of Contents](#-table-of-contents)\n- [🔮 Features](#-features)\n- [📎 Citation](#-citation)\n- [📆 To-do](#-to-do)\n- [🏎💨 Getting Started](#-getting-started)\n- [🤝 Contributing](#-contributing)\n- [\U0001faaa License](#-license)\n- [🙏 Acknowledgments](#-acknowledgments)\n\n## 🔮 **Features**\n\n**Zero System Calls**: Avoids system calls, leading to a smoother, quicker operation.<br>\n**Ergonomics**: With an ergonomic design, `PxBLAT` aims for a seamless user experience.<br>\n**No External Dependencies**: `PxBLAT` operates independently without any external dependencies.<br>\n**Self-Monitoring**: No need to trawl through log files; `PxBLAT` monitors its status internally.<br>\n**Robust Validation**: Extensively tested to ensure reliable performance and superior stability as BLAT.<br>\n**Format-Agnostic:** `PxBLAT` doesn\'t require you to worry about file formats.<br>\n**In-Memory Processing**: `PxBLAT` discards the need for intermediate files by doing all its operations in memory, ensuring speed and efficiency.<br>\n\n## 📎 **Citation**\n\nPxBLAT is scientific software, with a published paper in the [Journal].\nCheck the [published] to read the paper.\n\n## 📆 **To-do**\n\n- [x] parser gfclient result\n- [x] parse gfserver query result\n- [x] benchmarking multi connection and original version\n- [x] test result with original version\n- [x] fix build.py to build ssl, hts, maybe libuv when install with pip\n- [ ] add tool to conda channel\n- [x] add tool to pip\n- [x] change abort to throw exceptions\n- [x] implement twobit2fa\n- [ ] implement psl2sam\n\n## 🚀 **Getting Started**\n\nThe very first step in starting your journey with `PxBLAT` is to install the tool.\nTo do this, there are two options shown as below:\n\n- PyPI\n\n```bash\npip install pxblat\n```\n\n- CONDA\n\n```bash\nconda install pxblat\n```\n\nCongratulations! You\'ve successfully installed `PxBLAT` on your local machine.\nIf you have some issues, please check the [document](https://pxblat.readthedocs.io/en/latest/) first before opening a issue.\n\n### 🤖 **Using pxblat**\n\n```bash\npxblat -h\n```\n\nPlease see the [document](https://pxblat.readthedocs.io/en/latest/) for details.\n\n## 🤝 **Contributing**\n\nContributions are always welcome! Please follow these steps:\n\n1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.\n2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.\n3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).\n\n```bash\ngit checkout -b new-feature-branch\n```\n\n4. Take changes to the project\'s codebase.\n5. Install the latest package\n\n```bash\npoetry install\n```\n\n6. Test your changes\n\n```bash\npytest -vlsx test\n```\n\n7. Commit your changes to your local branch with a clear commit message that explains the changes you\'ve made.\n\n```bash\ngit commit -m \'Implemented new feature.\'\n```\n\n8. Push your changes to your forked repository on GitHub using the following command\n\n```bash\ngit push origin new-feature-branch\n```\n\nCreate a pull request to the original repository.\nOpen a new pull request to the original project repository. In the pull request, describe the changes you\'ve made and why they\'re necessary.\nThe project maintainers will review your changes and provide feedback or merge them into the main branch.\n\n## \U0001faaa **License**\n\nThis project is licensed under the [MIT](https://opensource.org/licenses/mit) License. See the [LICENSE](https://github.com/cauliyang/pxblat/blob/main/LICENSE) file for additional info.\nThe license of [BLAT](http://genome.ucsc.edu/goldenPath/help/blatSpec.html) is [here](https://genome.ucsc.edu/license/).\n\n## **Contributors**\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tbody>\n    <tr>\n      <td align="center" valign="top" width="14.28%"><a href="https://yangyangli.top"><img src="https://avatars.githubusercontent.com/u/38903141?v=4?s=100" width="100px;" alt="yangliz5"/><br /><sub><b>yangliz5</b></sub></a><br /><a href="#maintenance-cauliyang" title="Maintenance">🚧</a></td>\n    </tr>\n  </tbody>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\n## 🙏 **Acknowledgments**\n\n- [UCSC](https://github.com/ucscGenomeBrowser/kent)\n- [pybind11](https://github.com/pybind/pybind11/tree/stable)\n\n<!-- github-only -->\n',
    'author': 'Yangyang Li',
    'author_email': 'yangyang.li@northwestern.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
