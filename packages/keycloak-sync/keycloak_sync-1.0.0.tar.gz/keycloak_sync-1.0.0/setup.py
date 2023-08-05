# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keycloak_sync', 'keycloak_sync.model']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'coloredlogs>=14.0,<15.0',
 'google-cloud-storage>=1.34.0,<2.0.0',
 'numpy==1.18.0',
 'pandas>=1.1.4,<2.0.0',
 'python-keycloak>=0.23.0,<0.24.0']

entry_points = \
{'console_scripts': ['kcctl = keycloak_sync.kcctl:kcctl']}

setup_kwargs = {
    'name': 'keycloak-sync',
    'version': '1.0.0',
    'description': 'keycloak cli tool',
    'long_description': "# Keycloak_sync\n\n[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)\n\nSync users with keycloak by providing a csv file.\n\n## Features\n\n- Sync users with csv files\n- Export users to csv files\n- Delete users from csv files\n- Sync users from Google Object Stroage\n\n## Tech\n\nKeycloak_sync uses a number of open source projects to work properly:\n\n- [python-keycloak]\n- [pandas]\n- [numpy]\n- [PyYAML]\n- [Cerberus]\n- [coloredlogs]\n- [click]\n- [colorama]\n- [google-cloud-storage]\n\nAnd of course Keycloak_sync itself is open source with a [public repository](https://github.com/NOLANKANGYI/keyclaok_sync)\non GitHub.\n\n## Installation\n\nKeycloak_sync requires [python](https://python.org/) v3.8+ to run.\n\nInstall the dependencies and devDependencies and start the cli.\n\n```sh\ncd keycloak_sync\npoetry install\npoetry run entrypoint.py --help\n```\n\n## CLI\n\n```sh\npip install keycloak_sync\n\nkcctl --version\nkcctl --help\nkcctl sync --help\nkcctl export --help\nkcctl delete --help\n```\n\n### Sync\n\n```shell\nKEYCLOAK_SERVER_URL='https://keycloak.com/auth/' \\\nKEYCLOAK_REALM_NAME='keycloak-realm' \\\nKEYCLOAK_CLIENT_ID='keycloak-api' \\\nKEYCLOAK_CLIENT_SECRET='**********' \\\nCSV_FILE_TEMPLATE='~/template.yaml' \\\nCSV_FILE_NAME='~/users.csv' \\\nkcctl sync\n```\n\n### Delete\n\n```shell\nKEYCLOAK_SERVER_URL='https://keycloak.com/auth/' \\\nKEYCLOAK_REALM_NAME='keycloak-realm' \\\nKEYCLOAK_CLIENT_ID='keycloak-api' \\\nKEYCLOAK_CLIENT_SECRET='**********' \\\nCSV_FILE_TEMPLATE='~/template.yaml' \\\nkcctl delete\n```\n\n### Export\n\n```shell\nKEYCLOAK_SERVER_URL='https://keycloak.com/auth/' \\\nKEYCLOAK_REALM_NAME='keycloak-realm' \\\nKEYCLOAK_CLIENT_ID='keycloak-api' \\\nKEYCLOAK_CLIENT_SECRET='**********' \\\nCSV_FILE_TEMPLATE='~/template.yaml' \\\nCSV_FILE_NAME='~/users.csv' \\\nkcctl export\n```\n\n## Docker\n\nKeycloak_sync is very easy to install and deploy in a Docker container.\n\nBy default, the Docker will expose port 8080, so change this within the\nDockerfile if necessary. When ready, simply use the Dockerfile to\nbuild the image.\n\n```sh\ncd keycloak_sync\ndocker build -t <youruser>/Keycloak_sync:${package.version} .\n```\n",
    'author': 'Kangyi LI',
    'author_email': 'nolankangyi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
