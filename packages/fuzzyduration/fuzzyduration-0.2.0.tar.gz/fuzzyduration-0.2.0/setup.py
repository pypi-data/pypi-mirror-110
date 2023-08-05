# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzyduration']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fuzzyduration',
    'version': '0.2.0',
    'description': 'returns the number of seconds as the approx. largest unit of time.',
    'long_description': '# Fuzzy Duration\n\nA simple package to convert a number of seconds to the approximate duration of the largest time unit.\n\n## install\n\n```\npython3 -m pip install fuzzyduration --user\n```\n\n## Usage\n\n```python\nfrom fuzzyduration import fuzzyDuration\n\nsecs = 60 * 60 * 24 * 1 + 1234\n\nresult = fuzzyDuration(secs)\n\nprint(result) # "1 day"\n\nsecs = secs * 8 * 2\n\nprint(result) # "2 weeks"\n\nsecs = secs * 60\n\nprint(result) # "2 years"\n```\n',
    'author': 'ccdale',
    'author_email': 'chris.charles.allison+fuzzy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
