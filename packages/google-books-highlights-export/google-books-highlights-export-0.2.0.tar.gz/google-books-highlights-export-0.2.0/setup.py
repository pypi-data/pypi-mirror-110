# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_books_highlights_export']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'google-api-python-client>=2.9.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.4.4,<0.5.0',
 'html5lib>=1.1,<2.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['google-books-highlights-export = '
                     'google_books_highlights_export:main']}

setup_kwargs = {
    'name': 'google-books-highlights-export',
    'version': '0.2.0',
    'description': 'Export your Google Play Books highlights from Google Drive',
    'long_description': None,
    'author': 'Andrew Magee',
    'author_email': 'amagee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amagee/google-books-highlights-export',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
