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
    'version': '0.3.5',
    'description': 'A little helper library to streamline working with JWT in python',
    'long_description': '###########\njwtlib\n###########\n\n.. readme_inclusion_marker\n\n\nDev setup\n~~~~~~~~~\n\nInitialize local repository\n---------------------------\n\n.. code-block:: bash\n\n    $ pipenv install -d                     # Install all dependencies\n    $ pipenv run python setup.py develop    # Setup the pkg for local development\n    $ pipenv shell                          # Open shell within the virtualenv\n\n\nAvailable commands\n------------------\n\n.. code-block:: bash\n\n    $ peltak --help     # Show the list of available commands\n    $ peltak test       # Run tests\n    $ peltak lint       # Run code checks\n    $ peltak docs       # Build documentation using Sphinx\n\n\nRelease new version\n-------------------\n\n.. note:: Before releasing, make sure your changes are part of the develop branch.\n\n.. code-block:: bash\n\n    $ peltak release start\n    $ peltak git push\n    [ Create PR on GitHub and merge it ]\n    $ peltak release merged\n',
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
