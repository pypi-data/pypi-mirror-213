# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlcvzoo_tracker']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20',
 'filterpy>=1.4',
 'mlcvzoo_base>=5.1,<6.0',
 'numpy>=1.19.2,!=1.19.5',
 'opencv-contrib-python>=4.5,!=4.5.5.64',
 'opencv-python>=4.5,!=4.5.5.64',
 'related-mltoolbox>=1.0,<2.0',
 'yaml-config-builder>=8']

setup_kwargs = {
    'name': 'mlcvzoo-tracker',
    'version': '0.1.1',
    'description': 'MLCVZoo Tracker Package',
    'long_description': '# MLCVZoo Tracker\n\nThe MLCVZoo is an SDK for simplifying the usage of various (machine learning driven)\ncomputer vision algorithms. The package **mlcvzoo_tracker** contains tools for tracking detected objects.\n\nFurther information about the MLCVZoo can be found [here](../README.md).\n\n## Install\n`\npip install mlcvzoo-tracker\n`\n\n## Technology stack\n\n- Python\n',
    'author': 'Maximilian Otten',
    'author_email': 'maximilian.otten@iml.fraunhofer.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.openlogisticsfoundation.org/silicon-economy/base/ml-toolbox/mlcvzoo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
