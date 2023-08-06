# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['actuator']

package_data = \
{'': ['*']}

install_requires = \
['types-tzlocal>=4.2.2.2,<5.0.0.0',
 'tzlocal>=4.2,<5.0',
 'volttron>=10.0.rc0,<11.0']

entry_points = \
{'console_scripts': ['volttron-actuator = actuator.agent:main']}

setup_kwargs = {
    'name': 'volttron-actuator',
    'version': '0.1.1a6',
    'description': 'The Actuator Agent is used to manage write access to devices. Other agents may request scheduled times, called Tasks, to interact with one or more devices.',
    'long_description': '# volttron-actuator\n\n![Eclipse VOLTTRON 10.0.4rc](https://img.shields.io/badge/Eclipse%20VOLTTRON-10.0.4rc-red.svg)\n![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)\n![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)\n[![Passing?](https://github.com/eclipse-volttron/volttron-actuator/actions/workflows/run-tests.yml/badge.svg)](https://github.com/VOLTTRON/volttron-actuator/actions/workflows/run-tests.yml)\n[![pypi version](https://img.shields.io/pypi/v/volttron-actuator.svg)](https://pypi.org/project/volttron-actuator/)\n\n\nThe Actuator Agent is used to manage write access to devices. Other agents may request scheduled times, called Tasks, to interact with one or more devices.\n\n## Requirements\n\n* python >= 3.10\n* volttron >= 10.0\n* tzlocal >= 4.2\n* types-tzlocal >= 4.2.2.2\n\n## Documentation\n\nMore detailed documentation can be found on [ReadTheDocs](https://volttron.readthedocs.io/en/modular/). The RST source\nof the documentation for this component is located in the "docs" directory of this repository.\n\n## Installation\n\nBefore installing, VOLTTRON should be installed and running.  Its virtual environment should be active.\nInformation on how to install of the VOLTTRON platform can be found\n[here](https://github.com/eclipse-volttron/volttron-core).\n\nInstall and start the volttron-actuator.\n\n```shell\nvctl install volttron-actuator --agent-config <path to agent config> --start\n```\n\nView the status of the installed agent\n\n```shell\nvctl status\n```\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n',
    'author': 'Mark Bonicillo',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/VOLTTRON/volttron-actuator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
