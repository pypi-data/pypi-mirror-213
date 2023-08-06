# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['iricore']

package_data = \
{'': ['*'],
 'iricore': ['data/data16/ccir/*',
             'data/data16/igrf/*',
             'data/data16/index/*',
             'data/data16/mcsat/*',
             'data/data16/ursi/*',
             'data/data20/ccir/*',
             'data/data20/igrf/*',
             'data/data20/index/*',
             'data/data20/mcsat/*',
             'data/data20/ursi/*',
             'iri2016/*',
             'iri2020/*']}

install_requires = \
['fortranformat>=1.2.2,<2.0.0', 'numpy>=1.22,<2.0', 'pymap3d>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'iricore',
    'version': '1.4.5',
    'description': '',
    'long_description': '# iricore\nA Python interface to IRI-2016 and IRI-2020 using `ctypes` communication.\n\n**Important!** Because this package is mainly used for the [MIST experiment](http://www.physics.mcgill.ca/mist/), \nthe `iricore` cuts off calculation of unnecessary atmospheric parameters available in IRI-2016, leaving only electron density\nand electron temperature. All other parameters can be restored on demand (please contact me).\n\n## Installation\n\nThis package proved to work under Linux only (due to compilation difficulties in Windows). \nIf you are using Windows - consider installing [WSL](https://docs.microsoft.com/en-us/windows/wsl/install).\n\n### Prerequisites\n- CMAKE\n```\nsudo apt instal cmake\n```\n\n- Fortran compiler, e.g. `gfortran`\n```\nsudo apt isntall gfortran\n```\n\n### Installing package\nNow you can simply install it via `pip`:\n\n```\npython3 -m pip install iricore\n```\n\n## Data files\n`IRI2016` model depends on [data files](http://irimodel.org/indices/) which are regularly updated.\n`iricore` does not autoupdate those, but provides tool for quick update. You can run from terminal\n```\npython3 -c "import iricore; iricore.update()"\n```\n\nor add\n\n```\nimport iricore\niricore.update()\n```\nto any Python script.\n\n## Usage\nFor usage examples see `examples/`.',
    'author': 'Vadym Bidula',
    'author_email': 'vadym.bidula@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
