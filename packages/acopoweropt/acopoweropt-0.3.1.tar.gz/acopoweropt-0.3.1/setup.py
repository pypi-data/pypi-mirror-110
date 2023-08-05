# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acopoweropt']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.4,<6.0.0',
 'cvxopt>=1.2.6,<2.0.0',
 'imageio>=2.9.0,<3.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'acopoweropt',
    'version': '0.3.1',
    'description': 'Ant Colony Power Systems Optimizer',
    'long_description': '[![PyPI version](https://badge.fury.io/py/acopoweropt.svg)](https://badge.fury.io/py/acopoweropt)\n\n# Ant Colony Power Systems Optimizer\n\nThis library aims to provide a tool to obtain an optimal dispach of a Power System comprised of Thermal Generation Units. The approach combines the Ant Colony Optimizer with a non-linear solver provided by CVXOPT.\n\n> This is an under development library\n\n## Installation instructions\n\n### PyPi\nA pre-built binary wheel package can be installed using pip:\n```sh\npip install acopoweropt\n```\n\n### Poetry\nPoetry is a tool for dependency management and packaging in Python. `acopoweropt` can be installed in a poetry managed project:\n```sh\npoetry add acopoweropt\n```\n\n## Usage\nFrom a domain perspective, there should be a complete decoupling between an Ant Colony and a Power System, after all ants do not have knowledge of power systems. This approach, although more elegant, is far from trivial to be implemented, mainly because the __enviroment__ where the ants would look for food gets deeply entangled with the domain. For example, the modeling of pheromone matrix for the traveler salesman might not be adequate for a Power Systems Unit Commitment problem.\n\nFor that reason, the initial approach was to create two main _Entities_: A `Power System` and a `PowerColony`, where the first must be a Power System which can be solved by a mathematical method and the second should be an Ant Colony initialized to seek optimal results of a Power System problem.\n\nSince the dispatch of "multi operative zone" Thermal Generation Units (TGUs) bring non-linearities to the formulation, obtaining a global optimal financial dispach of the system is not a trivial task. The Ant Colony algorithm came in hand as a tool to iteractively seek a global optimal result without having to rely on brute computational force.\n\n### Defining Systems\nThe systems configuration should be defined in the [`systems.json`](systems.json) file. In the example provided, 3 systems where defined: \'s10\', \'s15\' and \'s40\', the names were chosen for convention and will be used by the `PowerSystem` class to initialize the desired configuration.\n\n\n#### Example\n\nThe code below samples a possible configuration which can be used to operate the system and solves this configuration.\n\n```python\nfrom acopoweropt import system\n\n# Instance a PowerSystem class from a configuration file where \'s10` defines a system configuration\nPSystem = system.PowerSystem(name=\'s10\')\n\n# Randomly selects a possible system operation (there are cases where more than a single unit can be operated in diferent configurations)\noperation = PSystem.sample_operation()\n\n# Solve the Economic Dispatch of the units of a specific configuration of the system, in this case, let\'s use the previously sampled one:\nsolution = PSystem.solve(operation=operation)\n\n# Prints total financial cost of the operation\nprint("Total Financial Cost: {}".format(solution.get(\'Ft\')))\n\n# Prints the operation with its power dispach values\nprint(solution.get(\'operation\'))\n```\n\nAnother option is to bring your own sequence of operative zones (1 for each TGU) and build the operation data from it:\n\n```python\nfrom acopoweropt import system\n\n# Intance a PowerSystem class from a configuration file where \'s10` defines a system configuration\nPSystem = system.PowerSystem(name=\'s10\')\n\n# Define a sequence of operative zones for each of the 10 TGUs\nopzs = [2, 3, 1, 2, 1, 1, 3, 1, 1, 3]\n\n# Build a configuration that represents such sequence of operative zones\noperation = PSystem.get_operation(operative_zones=opzs)\n\n# Solve the Economic Dispatch of the specific configuration:\nsolution = PSystem.solve(operation=operation)\n\n# Prints total financial cost of the operation\nprint("Total Financial Cost: {}".format(solution.get(\'Ft\')))\n\n# Prints the operation with its power dispach values\nprint(solution.get(\'operation\'))\n```\n\n### Defining Power Colonies\nAn Ant Colony should seek for a global optimal solution or "the optimal source of food". The algorithm was proposed by Marco Dorigo, check [Wiki](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms) for more details.\n\n#### Example\n\nThe code below initializes a PowerColony with a desired PowerSystem as the "environment" for the ants to seek their food. Once instantiated, the PowerColony immediately unleashes their ants for a first seek for solutions, therefore `PowerColony.paths` and `PowerColony.pheromone` can be observed.\n\n```python\nfrom acopoweropt import colony, system\n\nPSystem = system.PowerSystem(name=\'s15\')\nPColony = colony.PowerColony(n_ants=100,\n                            pheromone_evp_rate={\'worst\': 0.75, \'mean\': 0.25, \'best\': 0.05},\n                            power_system=PSystem)\n```\n\nNow a PowerColony can seek for optimal sources of food:\n```python\nPColony.seek(max_iter=20, power_system=PSystem, show_progress=True)\n\nax = PColony.paths.groupby(\'iteration\').distance.min().plot(y=\'distance\')\n\nPColony.create_pheromone_movie(duration=0.25)\n```\n\n## License\n\nSee the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).',
    'author': 'Ettore Aquino',
    'author_email': 'ettore@ettoreaquino.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ettoreaquino/acopoweropt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
