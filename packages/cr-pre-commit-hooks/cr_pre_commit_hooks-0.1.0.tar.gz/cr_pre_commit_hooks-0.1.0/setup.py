# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cr_pre_commit_hooks']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.15,<0.16']

entry_points = \
{'console_scripts': ['check-docstrings = cr_pre_commit_hooks.docstrings:main']}

setup_kwargs = {
    'name': 'cr-pre-commit-hooks',
    'version': '0.1.0',
    'description': 'pre-commit hooks for ensuring consistency across our code base. Included are hooks which are not available elsewhere and also not super useful outside of a CR context.',
    'long_description': '# Climate Resource pre-commit hooks\n\n<!--- sec-begin-description -->\n\n[pre-commit](https://pre-commit.com/) hooks for ensuring consistency across our code\nbase. Included are hooks which are not available elsewhere and also not super useful\noutside of a CR context.\n\n<!--- sec-end-description -->\n\n## Installation\n\n<!--- sec-begin-installation -->\n\nClimate Resource pre-commit hooks can be installed with pip:\n\n```bash\npip install cr-pre-commit-hooks\n```\n\n<!--- sec-end-installation -->\n\n### For developers\n\n<!--- sec-begin-installation-dev -->\n\nFor development, we rely on [poetry](https://python-poetry.org) for all our\ndependency management. To get started, you will need to make sure that poetry\nis installed\n([instructions here](https://python-poetry.org/docs/#installing-with-the-official-installer),\nwe found that pipx and pip worked better to install on a Mac).\n\nFor all of work, we use our `Makefile`.\nYou can read the instructions out and run the commands by hand if you wish,\nbut we generally discourage this because it can be error prone.\nIn order to create your environment, run `make virtual-environment`.\n\nIf there are any issues, the messages from the `Makefile` should guide you\nthrough. If not, please raise an issue in the [issue tracker][issue_tracker].\n\nFor the rest of our developer docs, please see [](development-reference).\n\n[issue_tracker]: https://gitlab.com/climate-resource/cr-pre-commit-hooks/issues\n\n<!--- sec-end-installation-dev -->\n',
    'author': 'Mika Pflüger',
    'author_email': 'mika.pflueger@climate-resource.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
