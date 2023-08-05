# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaml_indent']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['yaml-indent = yaml_indent.yaml_indent:main']}

setup_kwargs = {
    'name': 'yaml-indent',
    'version': '0.1.0',
    'description': '',
    'long_description': '# YAML Indent\n## Overview\n\nyaml-indent is a Python utility for formatting YAML files with correct\nindentation. It reads in a YAML file, processes it, and outputs a new\nYAML file with proper indentation, making the file more readable and\nmanageable.\n\n## How it Works\n\nThe utility makes use of the PyYAML library to parse the input YAML\nfile, and re-dumps the YAML data into the output file with correct\nindentation.\n\n## Installation\n\nTo use this utility, you must have Python 3 installed on your\nsystem. Additionally, you need to install the PyYAML library. You can\ninstall it using pip:\n\n``` sh\npip install yaml-indent\n```\n\nYou can then clone this repository to your local machine.\n\n## Usage\n\nTo use this utility, you need to run the Python script yaml_indent.py\nwith two arguments: the input YAML file and the output YAML file. \n\nHere is an example:\n\n``` sh\npython input.yaml output.yaml\n```\n\nIn this command, input.yaml is the YAML file you want to format and\noutput.yaml is the file where the formatted YAML will be written. If\noutput.yaml already exists, it will be overwritten.\n\n## Contributing\n\nContributions to this project are welcome. If you find a bug or think\nof a feature that this utility could benefit from, please open an\nissue or submit a pull request.\n\n## License\n\nThis project is open source under the terms of the GPL License.\n\n',
    'author': 'Knut Olav Bøhmer',
    'author_email': 'bohmer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
