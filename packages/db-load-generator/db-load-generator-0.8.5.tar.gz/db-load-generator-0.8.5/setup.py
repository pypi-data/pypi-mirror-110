# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbload',
 'dbload.resources',
 'dbload.tests',
 'dbload.tests.context',
 'dbload.tests.parser',
 'dbload.tests.query',
 'dbload.tests.return_random',
 'dbload.tests.scenario']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.1.2,<9.0.0',
 'JPype1>=1.2.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'ilexconf>=0.9.6,<0.10.0',
 'loguru>=0.5.3,<0.6.0',
 'mapz>=1.1.28,<2.0.0',
 'prettytable>=2.1.0,<3.0.0']

extras_require = \
{'dramatiq': ['APScheduler>=3.7.0,<4.0.0', 'dramatiq[rabbitmq]>=1.11.0,<2.0.0']}

entry_points = \
{'console_scripts': ['dbload = dbload.cli:main']}

setup_kwargs = {
    'name': 'db-load-generator',
    'version': '0.8.5',
    'description': 'Database load generator.',
    'long_description': '# db-load-generator\n\n`db-load-generator` is a Python framework and toolbox for generating artificial database loads with as little code as necessary.\nIt uses Java and JDBC drivers to connect to the databases.\n\n<p>\n    <a href="https://pypi.org/project/db-load-generator/"><img alt="PyPI" src="https://img.shields.io/pypi/v/db-load-generator?color=blue&logo=pypi"></a>\n    <a href="https://pypi.org/project/db-load-generator/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/db-load-generator?color=blue&logo=pypi"></a>\n    <a href="https://github.com/dynatrace-oss/db-load-generator/actions/workflows/build-test-release.yml"><img alt="Build Status" src="https://img.shields.io/github/workflow/status/dynatrace-oss/db-load-generator/Build%20Test%20Release?logo=github" /></a>\n    <a href="https://dbload.org"><img src="https://img.shields.io/github/workflow/status/dynatrace-oss/db-load-generator/Build%20Docs?label=docs&logo=github" alt="Documentation Build Status" /></a>\n    <a href="https://github.com/dynatrace-oss/db-load-generator/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/dynatrace-oss/db-load-generator"></a>\n</p>\n\n## Getting Started\n\nNew to `db-load-generator`? Checkout our official [Getting Started](https://db-load-generator.readthedocs.io/) guide.\n\n\n## Requirements\n\n* Python 3.9 or above.\n* Java 8 or above.\n* JDBC driver for your database.\n\n## Features\n\n* Test connection to the database using `dbload test`\n* Execute a query using `dbload execute`\n* Configure db-load-generator via\n  * command line arguments\n  * environment variables\n  * default config file `dbload.json`\n  * custom path config file\n* Print current parsed configuration using `dbload show settings`\n* Use decorators from `dbload` library to create scenarios and queries\n* Write annotated SQL queries in the `.sql` file and feed them using `dbload --sql myfile.sql`\n* Show current parsed queries using `dbload show queries`\n* Run any defined query using `dbload query`\n* Write full-fledged complex simulation scenarios using `dbload` library\n* Show current parsed scenarios using `dbload show scenarios`\n* Run any defined scenarios using `dbload scenario`\n* Use predefined simulations for popular databases using `dbload --predefined <db-name> ACTION`\n* Run db-load-generator as a background worker using [dramatiq](https://dramatiq.io)\n  * ensure there is a RabbitMQ running as a message broker\n  * runs scenarios as service workers `dbload worker`\n  * enqueue executions into broker using `dbload send <scenario name or actor name>`\n  * start beats/scheduler process using `dbload scheduler`\n\n## Development & Contributions\n\nContributions are welcome!\nIf you are interested in contributing to the project please read our [Code of Conduct](CODE_OF_CONDUCT.md).\n\n## License\n\n[Apache Version 2.0](LICENSE)\n',
    'author': 'Vagiz Duseev',
    'author_email': 'vagiz.duseev@dynatrace.com',
    'maintainer': 'Vagiz Duseev',
    'maintainer_email': 'vagiz.duseev@dynatrace.com',
    'url': 'https://github.com/dynatrace-oss/db-load-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
