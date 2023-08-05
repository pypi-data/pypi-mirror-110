# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yippi']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx[docs]>=4.0.2,<5.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'pyrate-limiter>=2.3.4,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'sphinx-rtd-theme[docs]>=0.5.2,<0.6.0',
 'sphinxcontrib-napoleon[docs]>=0.7,<0.8']

setup_kwargs = {
    'name': 'yippi',
    'version': '0.2.0.1',
    'description': 'An (a)sync e621 API wrapper for Python.',
    'long_description': '========\nOverview\n========\n\nAn (a)sync e621 API wrapper library.\n\n* Free software: GNU Lesser General Public License v3 (LGPLv3)\n\nInstallation\n============\n\n::\n\n    pip install yippi\n\nYou can also install the in-development version with::\n\n    pip install git+ssh://git@github.com/rorre/yippi.git@master\n\nQuickstart\n==========\n\nSync\n----\n\n::\n\n    >>> import requests\n    >>> from yippi import YippiClient\n    >>>\n    >>> session = requests.Session()\n    >>> client = YippiClient("MyProject", "1.0", "MyUsernameOnE621", session)\n    >>> posts = client.posts("m/m zeta-haru rating:s") # or ["m/m", "zeta-haru", "rating-s"], both works.\n    [Post(id=1383235), Post(id=514753), Post(id=514638), Post(id=356347), Post(id=355044)]\n    >>> posts[0].tags\n    {\'artist\': [\'zeta-haru\'],\n     \'character\': [\'daniel_segja\', \'joel_mustard\'],\n     \'copyright\': [\'patreon\'],\n     \'general\': [\'5_fingers\', ..., \'spooning\'],\n     \'invalid\': [],\n     \'lore\': [],\n     \'meta\': [\'comic\'],\n     \'species\': [\'bird_dog\', ... ]}\n\nAsync\n-----\n\n::\n\n    >>> import aiohttp\n    >>> from yippi import AsyncYippiClient\n    >>>\n    >>> session = aiohttp.ClientSession()\n    >>> client = AsyncYippiClient("MyProject", "1.0", "MyUsernameOnE621", session)\n    >>> posts = await client.posts("m/m zeta-haru rating:s") # or ["m/m", "zeta-haru", "rating-s"], both works.\n    [Post(id=1383235), Post(id=514753), Post(id=514638), Post(id=356347), Post(id=355044)]\n    >>> posts[0].tags\n    {\'artist\': [\'zeta-haru\'],\n     \'character\': [\'daniel_segja\', \'joel_mustard\'],\n     \'copyright\': [\'patreon\'],\n     \'general\': [\'5_fingers\', ..., \'spooning\'],\n     \'invalid\': [],\n     \'lore\': [],\n     \'meta\': [\'comic\'],\n     \'species\': [\'bird_dog\', ... ]}\n\nExamples are available in `examples directory <https://github.com/rorre/Yippi/tree/master/examples>`_.\n    \nDocumentation\n=============\n\nDocumentation is available on readthedocs: https://yippi.readthedocs.io/\n\n\nDevelopment\n===========\n\nTo run the all tests run::\n\n    tox\n\nNote, to combine the coverage data from all the tox environments run:\n\n.. list-table::\n    :widths: 10 90\n    :stub-columns: 1\n\n    - - Windows\n      - ::\n\n            set PYTEST_ADDOPTS=--cov-append\n            tox\n\n    - - Other\n      - ::\n\n            PYTEST_ADDOPTS=--cov-append tox\n',
    'author': 'Rendy Arya Kemal',
    'author_email': 'rendyarya22@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rorre/Yippi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
