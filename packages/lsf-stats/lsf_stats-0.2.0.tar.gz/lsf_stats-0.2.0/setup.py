# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lsf_stats']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'humanize>=3.9.0,<4.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pyskim==0.1.3',
 'seaborn>=0.11.1,<0.12.0',
 'tqdm>=4.61.1,<5.0.0']

entry_points = \
{'console_scripts': ['lsf_stats = lsf_stats:cli']}

setup_kwargs = {
    'name': 'lsf-stats',
    'version': '0.2.0',
    'description': 'Summarize LSF job properties by parsing log files.',
    'long_description': '# lsf_stats\n\n[![PyPI](https://img.shields.io/pypi/v/lsf_stats.svg?style=flat)](https://pypi.python.org/pypi/lsf_stats)\n[![Tests](https://github.com/kpj/lsf_stats/workflows/Tests/badge.svg)](https://github.com/kpj/lsf_stats/actions)\n\nSummarize LSF job properties by parsing log files.\n\n\n## Installation\n\n```python\n$ pip install lsf_stats\n```\n\n\n## Usage\n\n```bash\n$ lsf_stats --help\nUsage: lsf_stats [OPTIONS] COMMAND [ARGS]...\n\n  Summarize LSF job properties by parsing log files.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  gather     Aggregate information from log files in single dataframe.\n  summarize  Summarize and visualize aggregated information.\n```\n',
    'author': 'kpj',
    'author_email': 'kim.philipp.jablonski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpj/lsf_stats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
