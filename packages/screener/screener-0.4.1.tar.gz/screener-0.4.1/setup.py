# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['screener', 'screener.parser', 'screener.reader']

package_data = \
{'': ['*']}

install_requires = \
['EbookLib>=0.18,<0.19', 'beautifulsoup4>=4.12.2,<5.0.0', 'mobi>=0.3.3,<0.4.0']

entry_points = \
{'console_scripts': ['screener = screener.__main__:main']}

setup_kwargs = {
    'name': 'screener',
    'version': '0.4.1',
    'description': 'Check e-book files for security and privacy issues.',
    'long_description': '# Screener\n\nCheck e-book files for security and privacy issues.\n\n## Motivation\n\nE-books are great, but the common file formats have security and privacy issues. Most use web browser technologies like HTML, CSS, and JavaScript. Therefore, e-books are vulnerable to security and privacy issues that already exist on the web.\n\nScreener aims to check e-book files for these issues so that you can read with peace of mind!\n\n## Features\n\n- Check e-book files for JavaScript tags.\n- Check e-book files for images with external sources to prevent tracking.\n- Supports `.epub`, `.mobi`, and `.azw3` files.\n\n## Get started\n\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes.\n\n### Prerequisites\n\nScreener requires [Python](https://www.python.org/about/gettingstarted/) (version 3.10 or newer).\n\n### Installing\n\nScreener is available on [PyPI](https://pypi.org/project/screener/). To install, run:\n\n```bash\npip install screener\n```\n\n#### Development installation\n\nTo install Screener for development, ensure you have [Poetry](https://python-poetry.org/) clone the repository and run:\n\n```bash\npoetry install\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nAt present, this project is in early development and needs extra security and privacy checks and wider file format support more than anything else.\n\nPlease make sure to update tests as appropriate.\n\n## Versioning\n\nThis project uses [SemVer](http://semver.org/) for versioning.\n\n## Authors\n\nScreener was created by Tom Kuson ([@tjkuson](https://github.com/tjkuson)).\n\n## Licence\n\nScreener is released under the [LGPL version 3](LICENCE).\n',
    'author': 'Tom Kuson',
    'author_email': 'mail@tjkuson.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tjkuson/screener/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
