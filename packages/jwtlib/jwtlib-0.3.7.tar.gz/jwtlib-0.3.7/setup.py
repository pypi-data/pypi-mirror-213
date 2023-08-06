# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jwtlib']

package_data = \
{'': ['*']}

install_requires = \
['pyjwt>=2.4.0']

setup_kwargs = {
    'name': 'jwtlib',
    'version': '0.3.7',
    'description': 'A little helper library to streamline working with JWT in python',
    'long_description': '###########\njwtlib\n###########\n\n.. readme_inclusion_marker\n\n\nDev setup\n~~~~~~~~~\n\nInitialize local repository\n---------------------------\n\n.. code-block:: bash\n\n    $ poetry install\n    $ poetry shell                          # Open shell within the virtualenv\n\n\nAvailable commands\n------------------\n\n.. code-block:: bash\n\n    $ peltak --help     # Show the list of available commands\n    $ peltak test       # Run tests\n    $ peltak check      # Run code checks\n    $ peltak docs       # Build documentation using Sphinx\n\n\nRelease new version\n-------------------\n\nWhile on master branch, you can release the current state of it by running\n\n.. code-block:: bash\n\n    peltak release create               # Create a patch release\n    peltak release create -t patch      # Create a patch release\n    peltak release create -t minor      # Create a minor release\n    peltak release create -t major      # Create a major release\n',
    'author': 'Mateusz Klos',
    'author_email': 'novopl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://novopl.github.com/jwtlib',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
