# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaml_indent']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'configparser>=5.3.0,<6.0.0',
 'ruamel-yaml>=0.17.31,<0.18.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['yaml-indent = yaml_indent.yaml_indent:main']}

setup_kwargs = {
    'name': 'yaml-indent',
    'version': '0.1.3',
    'description': 'Tool for making consistent indentation',
    'long_description': "# YAML Indent\n\n`yaml-indent` is a Python script to re-indent YAML files according to configurable or default indentation rules. It uses the `ruamel.yaml` library for parsing and writing YAML.\n\n## Installation\n\nThe script requires Python 3.\n\n``` sh\npip install yaml-indent\n```\n\n## Usage\n\nYou can run `yaml-indent` from the command line with the following syntax:\n\n``` sh\nyaml-indent <input_file> [-o <output_file>] [-i]\n```\n\nWhere:\n\n- `<input_file>` is the path to the input YAML file to be re-indented.\n- `-o <output_file>` (optional) is the path to the output file where the indented YAML will be written.\n- `-i` (optional) if set, the input file will be edited in place.\n\nIf no output file is specified and `-i` is not set, the indented YAML will be printed to the standard output.\n\n## Configuration\n\n`yaml-indent` looks for a `.yaml_indent.ini` configuration file in the\nthe yaml files directory and all parent directories up to the home\ndirectory. The configuration file should be in the INI format and can\nspecify the `mapping`, `sequence`, and `offset` indentation values\nunder the `YAML` section.\n\nHere's an example:\n\n```ini\n[YAML]\nmapping=4\nsequence=4\noffset=0\n```\n## Contributing\n\nContributions to this project are welcome. If you find a bug or think\nof a feature that this utility could benefit from, please open an\nissue or submit a pull request.\n\n## Source Code\n\nThe source code for this project is hosted on GitHub. You can access\nit at [https://github.com/knobo/yaml-indent](https://github.com/knobo/yaml-indent).\n\n## License\n\nThis project is open source under the terms of the GPL License.\n\n",
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
