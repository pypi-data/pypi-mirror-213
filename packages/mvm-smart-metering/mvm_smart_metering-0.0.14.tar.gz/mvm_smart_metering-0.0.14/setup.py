# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mvm_smart_meter']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'pandas==2.0.2',
 'python-dotenv==1.0.0',
 'requestium==0.2.1',
 'requests>=2.28.2,<3.0.0',
 'webdriver-manager>=3.8.5,<4.0.0']

setup_kwargs = {
    'name': 'mvm-smart-metering',
    'version': '0.0.14',
    'description': 'Script for scraping mvm smart meter data',
    'long_description': '# MVM Smart Metering\nThis is a automation tool for collecting load curve from mvm smart metering site\n\n---\n\nInstallation:\n\n```bash\npip install mvm-smart-metering\n```\n\nor\n\n```bash\npoetry add mvm-smart-metering\n```\n\n\n\n[Documantion](https://ktomi96.github.io/mvm_smart_metering/)\n\n---\n\n\n\n\n',
    'author': 'ktomi96',
    'author_email': 'kokai.tamas.96@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
