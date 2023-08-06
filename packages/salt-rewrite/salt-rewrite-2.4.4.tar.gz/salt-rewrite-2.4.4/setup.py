# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['saltrewrite',
 'saltrewrite.imports',
 'saltrewrite.salt',
 'saltrewrite.testsuite']

package_data = \
{'': ['*']}

install_requires = \
['bowler>=0.9.0', 'fissix>=21.6,<22.0']

entry_points = \
{'console_scripts': ['salt-rewrite = saltrewrite.__main__:rewrite']}

setup_kwargs = {
    'name': 'salt-rewrite',
    'version': '2.4.4',
    'description': 'A set of Bowler code to rewrite parts of Salt',
    'long_description': None,
    'author': 'Pedro Algarvio',
    'author_email': 'pedro@algarvio.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
