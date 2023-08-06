# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygus', 'pygus.gus', 'pygus.impacts']

package_data = \
{'': ['*'], 'pygus.gus': ['inputs/*', 'outputs/*']}

install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0',
 'ipython>=7.27.0,<8.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'mesa>=0.8.9,<0.9.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'portray>=1.7.0,<2.0.0',
 'pytest>=7.1.2,<8.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'termcolor>=2.1.1,<3.0.0',
 'utm>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'pygus',
    'version': '2.0.1',
    'description': 'Green Urban Scenarios - A digital twin representation, simulation of urban forests and their impact analysis.',
    'long_description': '[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Versions](https://img.shields.io/pypi/pyversions/pygus)]()\n\n\n\n# gus\n![GUS-IMAGE](https://miro.medium.com/max/1400/1*fMM7rnq1RJCh-nFBGLUvyA.png)\n\nGreen Urban Scenarios - A digital twin representation, simulation of urban forests and their impact analysis.\n\n## Getting Started\nVisit the GUS [website documentation](https://lucidmindsai.github.io/gus/) for help with installing GUS, code documentation, and a [basic tutorial](https://github.com/lucidmindsai/gus/blob/main/notebooks/Tutorial.ipynb) to get you started. \n\n## Install from PyPi\nWe publish GUS as `pyGus` package in PyPi. Dependencies can be found in the .toml file on the GUS GitHub page. Even though installation with Poetry is possible, the most stable installation can be done via pip.\n\n```\n$ pip install pygus\n```\n\nFor further instructions and code documentation, visit [GUS Code Documentation](https://lucidmindsai.github.io/gus/)\n\n### Who maintains GUS?\nThe GUS is currently developed and maintained by [Lucidminds](https://lucidminds.ai/) and [Dark Matter Labs](https://darkmatterlabs.org/) members as part of their joint project [TreesAI](https://treesasinfrastructure.com/#/).\n\n### Notes\n* The GUS is open for PRs.\n* PRs will be reviewed by the current maintainers of the project.\n* Extensive development guidelines will be provided soon.\n* To report bugs, fixes, and questions, please use the [GitHub issues](https://github.com/lucidmindsai/gus/issues).',
    'author': 'Bulent Ozel',
    'author_email': 'bulent@lucidminds.ai',
    'maintainer': 'Oguzhan Yayla',
    'maintainer_email': 'oguzhan@lucidminds.ai',
    'url': 'https://github.com/lucidmindsai/gus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
