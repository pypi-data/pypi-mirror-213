# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asp_chef_cli']

package_data = \
{'': ['*']}

install_requires = \
['dumbo-utils>=0.1.9,<0.2.0',
 'pytest-playwright>=0.3.3,<0.4.0',
 'rich>=13.4.1,<14.0.0',
 'typer>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'asp-chef-cli',
    'version': '0.1.2',
    'description': 'A simple CLI to run ASP Chef recipes',
    'long_description': '# ASP Chef Headless\n\nA simple CLI to run ASP Chef in headless mode.\n\n\n## Install\n\nThe suggested way is via pip:\n```bash\n$ pip install asp-chef-cli\n$ playwright install\n```\n\nDocker is another option (for headless mode):\n```bash\n$ docker run malvi/asp-chef-headless\n```\n\n\n\n\n## Usage\n\nRun with one of the following commands:\n```bash\n$ docker run malvi/asp-chef-headless --help\n$ python -m asp_chef_cli --help\n```\n\nAdd the recipe (an ASP Chef sharable URL) with the option `--url` (quote the URL as it contains characters like # that breaks bash and other terminals).\nThe headless mode can be activated with the flag `--headless` (always active in the docker image).\nPossibly change the default browser used by playwright with the option `--browser`.\nFinally, give a command to execute:\n* `run` simply runs the recipe as it is;\n* `run-with` runs the recipe with the input replaced by the one specified either with the option `--input` or via the prompt.\n\nThe flag `--help` can be specified after a command to get a list of arguments for that command.\n\n\n## Examples\n\nLet us consider [this simple recipe](https://asp-chef.alviano.net/#eJxtkNuOgjAQhl+plNUsl4srUKIQEXu6s+Ch2CIJIpan33bdRC/2ajKnf/75DibtRBt69QLNiUGSbkfJyawRsFAUqqFKMEBNpxl5TNz1YvzXC7w6ee5xHfUV3PWoTRWDauRbq+X3ck82MpfpJf/ePXhZGS6Bn+mltyo3MGvYLS8Z5AsAGVzOuN5AppGtr+Vqkd6rGBtGi07AD6dRchIZBk+nkgQXbr0gOUrhh2BPgqEyaH4w6VTHwfjuldFwFMlF5m1hauL8ZVfhV69cn9We1Ff3w7r5Gu1dW38op4famy/8tOcJGH5vtfjGNDaouRo3x4iaOF2/aT1ZURhNFGZ30Wag0pFlW0z/8vNDw0nRMRgBxwup4Mh0NPGSAep9OgaW5flOIR4YdD8XRxuHOsbDizkOjtgLfgC4qpvc%21) with no input and guessing the atom `world`.\nThe recipe can be run headless by giving the following command:\n```bash\n$ python -m asp_chef_cli --headless --browser=chromium --url="https://asp-chef.alviano.net/#eJxtkNuOgjAQhl+plNUsl4srUKIQEXu6s+Ch2CIJIpan33bdRC/2ajKnf/75DibtRBt69QLNiUGSbkfJyawRsFAUqqFKMEBNpxl5TNz1YvzXC7w6ee5xHfUV3PWoTRWDauRbq+X3ck82MpfpJf/ePXhZGS6Bn+mltyo3MGvYLS8Z5AsAGVzOuN5AppGtr+Vqkd6rGBtGi07AD6dRchIZBk+nkgQXbr0gOUrhh2BPgqEyaH4w6VTHwfjuldFwFMlF5m1hauL8ZVfhV69cn9We1Ff3w7r5Gu1dW38op4famy/8tOcJGH5vtfjGNDaouRo3x4iaOF2/aT1ZURhNFGZ30Wag0pFlW0z/8vNDw0nRMRgBxwup4Mh0NPGSAep9OgaW5flOIR4YdD8XRxuHOsbDizkOjtgLfgC4qpvc%21" run\nEMPTY MODEL\n§\nworld.\n```\n\nIt is possible to specify a different input as follows:\n```bash\n$ python -m asp_chef_headless --headless --browser=chromium --url="https://asp-chef.alviano.net/#eJxtkNuOgjAQhl+plNUsl4srUKIQEXu6s+Ch2CIJIpan33bdRC/2ajKnf/75DibtRBt69QLNiUGSbkfJyawRsFAUqqFKMEBNpxl5TNz1YvzXC7w6ee5xHfUV3PWoTRWDauRbq+X3ck82MpfpJf/ePXhZGS6Bn+mltyo3MGvYLS8Z5AsAGVzOuN5AppGtr+Vqkd6rGBtGi07AD6dRchIZBk+nkgQXbr0gOUrhh2BPgqEyaH4w6VTHwfjuldFwFMlF5m1hauL8ZVfhV69cn9We1Ff3w7r5Gu1dW38op4famy/8tOcJGH5vtfjGNDaouRo3x4iaOF2/aT1ZURhNFGZ30Wag0pFlW0z/8vNDw0nRMRgBxwup4Mh0NPGSAep9OgaW5flOIR4YdD8XRxuHOsbDizkOjtgLfgC4qpvc%21" run-with --input "hello."\nhello.\n§\nhello.\nworld.\n```',
    'author': 'Mario Alviano',
    'author_email': 'mario.alviano@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
