# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deepbench',
 'deepbench.astro_object',
 'deepbench.collection',
 'deepbench.image',
 'deepbench.physics_object',
 'deepbench.shape_generator']

package_data = \
{'': ['*'], 'deepbench': ['settings/*']}

install_requires = \
['astropy>=5.2.2,<6.0.0',
 'autograd>=1.5,<2.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.3,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'scikit-image>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'deepbench',
    'version': '0.1.1',
    'description': 'Physics Benchmark Dataset Generator',
    'long_description': '![GitHub Workflow Status](https://img.shields.io/github/workflow/status/deepskies/DeepBench/build-bench)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/deeepskies/DeepBench/test-bench?label=test)\n[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n [![PyPI version](https://badge.fury.io/py/deepbench.svg)](https://badge.fury.io/py/deepbench)\n\n\n\n# DeepBench\n\n### What is it?\nSimulation library for very simple simulations to *benchmark* machine learning algorithms.\n![DeepBench Logo](docs/repository_support/DeepSkies_Logos_DeepBench.png)\n\n\n### Why do we need it? Why is it useful?\n1. There are very universally recognized scientifically meaningful benchmark data sets, or methods with which to generate them.\n2. A very simple data set will have objects, patterns, and signals that are intuitively quanitifiable and will be fast to generate.\n3. A very simple data set will be a great testing ground for new networks and for newcomers to practice with the technology.\n\n\n## Requirements\n1. python 3.x\n\n\n### Install \n\n`pip install deepbench`\n\n### Install from Source\n\n\n## General Features\n1. very fast to generate\n2. Mimics in a very basic / toy way what is in astro images\n3. Be fully controllable parametrically\n\n![DeepBench Logo](docs/repository_support/DeepBench.png)\n\n### Included Simulations \n\n1. Astronomy Objects - simple astronomical object simulation \n- Galaxy, Spiral Galaxy, Star\n\n2. Shapes - simple 2D geometric shapes \n- Rectangle, Regular Polygon, Arc, Line, Ellipse\n\n3. Physics Objects - simple physics simulations \n- Neutonian Pendulum, Hamiltonian Pendulum\n\n## Example\n\nStandalone: \n```\n\n```\n\nFine-Grained Control: \n```\n\n```\n\n\n## Original Development Team\n1. Craig Brechmos\n2. Renee Hlozek\n3. Brian Nord\n\n\n## How to contribute\nI\'m really glad you\'re reading this, because we need volunteer developers to help this project come to fruition.\n\n### Testing\n\n### Submitting changes\n\nPlease send a [GitHub Pull Request to simplephysicaliage](https://github.com/deepskies/SimplePhysicalImage/pull/new/master) with a clear list of what you\'ve done (read more about [pull requests](http://help.github.com/pull-requests/)). When you send a pull request, we will love you forever if you include examples. We can always use more test coverage. Please follow our coding conventions (below) and make sure all of your commits are atomic (one feature per commit).\n\nAlways write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:\n\n    $ git commit -m "A brief summary of the commit\n    > \n    > A paragraph describing what changed and its impact."\n\n### Coding conventions\n\nStart reading our code and you\'ll get the hang of it. We optimize for readability:\n\n  * We indent using tabs\n  * We ALWAYS put spaces after list items and method parameters (`[1, 2, 3]`, not `[1,2,3]`), around operators (`x += 1`, not `x+=1`), and around hash arrows.\n  * This is open source software. Consider the people who will read your code, and make it look nice for them. It\'s sort of like driving a car: Perhaps you love doing donuts when you\'re alone, but with passengers the goal is to make the ride as smooth as possible.\n\n',
    'author': 'Ashia Lewis',
    'author_email': 'pantagruelspendulum@protonmail.com',
    'maintainer': 'Ashia Lewis',
    'maintainer_email': 'pantagruelspendulum@protonmail.com',
    'url': 'https://github.com/deepskies/DeepBenchmark',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
