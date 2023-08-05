# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webpageinfo', 'webpageinfo.config']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<5',
 'httpx>=0,<1',
 'pdfminer.six>=20220524,<20220525',
 'pillow>=9,<10',
 'splinter[selenium4]>=0,<1']

setup_kwargs = {
    'name': 'webpageinfo',
    'version': '2022.5.27',
    'description': 'Web page information (title, content, tags…)',
    'long_description': '# WebPageInfo\n\nWeb page information (title, content, tags…)\n\nInternal tool, no public documentation…\n',
    'author': 'Vincent Poulailleau',
    'author_email': 'vpoulailleau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vpoulailleau/webpageinfo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
