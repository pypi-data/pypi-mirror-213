# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src', 'pandoc_pdf_utils': 'src/pandoc_pdf_utils'}

packages = \
['pandoc_pdf', 'pandoc_pdf_utils']

package_data = \
{'': ['*'], 'pandoc_pdf_utils': ['default_config/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['pandoc_pdf = pandoc_pdf.main:pandoc_pdf']}

setup_kwargs = {
    'name': 'pandoc-pdf',
    'version': '0.1.12',
    'description': 'Command to generate pdf easily with pandoc.',
    'long_description': 'None',
    'author': 'rai',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
