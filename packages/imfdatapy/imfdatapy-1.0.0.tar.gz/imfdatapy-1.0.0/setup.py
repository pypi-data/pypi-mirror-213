# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imfdatapy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.6', 'pandas>=1.3.5', 'requests>=2.23.0']

setup_kwargs = {
    'name': 'imfdatapy',
    'version': '1.0.0',
    'description': 'A package for data discovery and extraction from the IMF!',
    'long_description': '# imfdatapy\n\nA package for data discovery and extraction from the International Monetary Fund (IMF)!\nThis repository contains Python source code and Jupyter notebooks with examples on how to extract data from the IMF.\n\n## Installation\n\n```bash\n    $ pip install imfdatapy\n```\n\n## Usage\n\n`imfdatapy` can be used to search through and extract data as follows. The examples below show how to search through the IFS (International Financial Statistics) and BOP (Balance of Payments) using ```serach_terms``` and download all the data with matching economic indicator names.\n\n```python\nfrom imfdatapy.imf import *\nifs = IFS(search_terms=["gross domestic product, real"], countries=["US"], period=\'Q\',\nstart_date="2000", end_date="2022")\ndf = ifs.download_data()\n\nbop = BOP(search_terms=["current account, total, credit"], countries=["US"], period=\'Q\',\nstart_date="2000", end_date="2022")\ndf = bop.download_data()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a [Code of Conduct](conduct.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`imfdatapy` was created by Sou-Cheng T. Choi and Irina Klein, Illinois Institute of Technology. It is licensed under the terms of the Apache License, v2.0.\n\nWith regard to the terms for using IMF data, please refer to IMF\'s [Copyright and Usage](https://www.imf.org/external/terms.htm) and pay special attention to the \nsection _SPECIAL TERMS AND CONDITIONS PERTAINING TO THE USE OF DATA_.  \n\n\n## Credits\n\n`imfdatapy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).',
    'author': 'Irina Klein, Sou-Cheng T. Choi',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.15,<3.11',
}


setup(**setup_kwargs)
