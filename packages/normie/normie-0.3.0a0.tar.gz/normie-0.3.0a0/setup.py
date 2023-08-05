# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['normie']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=56.0.0,<57.0.0']

entry_points = \
{'console_scripts': ['doctest = tools.run_tests:run_doctest',
                     'test = tools.run_tests:test']}

setup_kwargs = {
    'name': 'normie',
    'version': '0.3.0a0',
    'description': 'Accurate and efficient normal distribution statistics.',
    'long_description': '# normie - Python package for normal distribution functions\n\n## Examples of use\n\n```\n>>> from normie import cdf, invcdf\n>>> cdf(2.0)\n0.9772498607635498\n>>> invcdf(0.5)\n0.0\n\n```\n\n',
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': 'Jack Grahl',
    'maintainer_email': 'jack.grahl@gmail.com',
    'url': 'https://github.com/jwg4/normie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
