# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysmo', 'pysmo.core', 'pysmo.core.sac', 'pysmo.tools', 'pysmo.tools.noise']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pyproj>=3.0.0,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'scipy>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'pysmo',
    'version': '0.8.2',
    'description': 'Python module to read/write/manipulate SAC (Seismic Analysis Code) files',
    'long_description': "\n![Test Status](https://github.com/pysmo/pysmo/actions/workflows/run-tests.yml/badge.svg)\n![Build Status](https://github.com/pysmo/pysmo/actions/workflows/build.yml/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/pysmo/badge/?version=latest)](https://pysmo.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/pysmo/pysmo/branch/master/graph/badge.svg?token=ZsHTBN4rxF)](https://codecov.io/gh/pysmo/pysmo)\n[![PyPI](https://img.shields.io/pypi/v/pysmo)](https://pypi.org/project/pysmo/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysmo)\n\nPysmo\n=====\n\nPython package to read/write/manipulate SAC (Seismic Analysis Code) files.\n\n\nQuickstart\n----------\nTo install the stable version of pysmo run the following command in a terminal:\n\n```shell\n$ pip install pysmo\n```\n\nPre-release versions of pysmo can be installed by running:\n\n```shell\n$ pip install pysmo --pre\n```\n\nFinally, to install the current ``master`` branch directly from Github run:\n\n```shell\n$ pip install git+https://github.com/pysmo/pysmo\n```\n\nPysmo can then be used in a python script or the python shell directly:\n\n\n```python\n>>> from pysmo import SacIO\n>>> seismogram = SacIO.from_file('file.sac')\n>>> print(seismogram.delta)\n0.02500000037252903\n>>> print(seismogram.data)\n[-2.987490077543953e-08, -2.983458813332618e-08, ...\n>>> help(seismogram)\nHelp on SacIO in module pysmo.core.sac.sacio object:\n\n...\n```\nDocumentation\n-------------\n\nThe complete pysmo documentation is available at https://pysmo.readthedocs.io/\n\nContributors\n------------\n\n- Helio Tejedor\n",
    'author': 'Simon M. Lloyd',
    'author_email': 'simon@slloyd.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
