# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eotdl',
 'eotdl.access',
 'eotdl.access.sentinelhub',
 'eotdl.auth',
 'eotdl.commands',
 'eotdl.curation',
 'eotdl.curation.stac',
 'eotdl.datasets',
 'eotdl.src',
 'eotdl.src.errors',
 'eotdl.src.repos',
 'eotdl.src.usecases',
 'eotdl.src.usecases.auth',
 'eotdl.src.usecases.datasets',
 'eotdl.tools',
 'eotdl.tools.sen12floods']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.6,<2.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.65.0,<5.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['eotdl = eotdl.cli:app']}

setup_kwargs = {
    'name': 'eotdl',
    'version': '2023.6.14.post8',
    'description': 'Earth Observation Training Data Lab',
    'long_description': '# eotdl \n\nThis is the main library and CLI for EOTDL.\n\n',
    'author': 'EarthPulse',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
