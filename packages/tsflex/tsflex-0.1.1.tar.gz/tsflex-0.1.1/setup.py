# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsflex',
 'tsflex.chunking',
 'tsflex.features',
 'tsflex.pipeline',
 'tsflex.processing',
 'tsflex.utils']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.3,<0.4.0',
 'fastparquet>=0.6.3,<0.7.0',
 'numpy>=1.19.0,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pathos>=0.2.7,<0.3.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'tsflex',
    'version': '0.1.1',
    'description': 'Toolkit for flexible operations on time-series data',
    'long_description': '# <p align="center"><img alt="tsflex" src="./docs/_static/logo.png" height="100"></p>\n\n*tsflex* stands for: _**flex**ible **t**ime-**s**eries operations_<br>\n\nIt is a `time-series first` toolkit for **processing & feature extraction**, making few assumptions about input data. \n\n* [example notebooks](examples/)\n\n## Table of contents\n  - [Installation](#installation)\n  - [Usage](#usage)\n    - [Series processing](#series-processing)\n    - [Feature extraction](#feature-extraction)\n  - [Documentation](#documentation)\n\n\n## Installation\n\nIf you are using **pip**, just execute the following command:\n\n```sh\npip install tsflex\n```\n\n## Usage\n\n_tsflex_ is built to be intuitive, so we encourage you to copy-paste this code and toy with some parameters!\n\n\n### Series processing\n\n`:WIP:`\n\n### Feature extraction\n\n```python\nimport pandas as pd; import scipy.stats as ss; import numpy as np\nfrom tsflex.features import FeatureDescriptor, FeatureCollection, NumpyFuncWrapper\n\n# 1. -------- Get your time-indexed data --------\nseries_size = 10_000\nseries_name="lux"\n\ndata = pd.Series(\n    data=np.random.random(series_size), \n    index=pd.date_range("2021-07-01", freq="1h", periods=series_size)\n).rename(series_name)\n# -- 1.1 drop some data, as we don\'t make frequency assumptions\ndata = data.drop(np.random.choice(data.index, 200, replace=False))\n\n\n# 2 -------- Construct your feature collection --------\nfc = FeatureCollection(\n    feature_descriptors=[\n        FeatureDescriptor(\n            function=NumpyFuncWrapper(func=ss.skew, output_names="skew"),\n            series_name=series_name, \n            window="1day", stride="6hours"\n        )\n    ]\n)\n# -- 2.1. Add multiple features to your feature collection\nfc.add(FeatureDescriptor(np.min, series_name, \'2days\', \'1day\'))\n\n\n# 3 -------- Calculate features --------\nfc.calculate(data=data)\n```\n\n## Documentation\n\nTo see the documentation locally, install [pdoc](https://github.com/pdoc3/pdoc) and execute the succeeding command from this folder location.\n\n```sh\npdoc3 --template-dir docs/pdoc_template/ --http :8181 tsflex\n```\n\n<br>\n\n---\n\n<p align="center">\n👤 <i>Jonas Van Der Donckt, Jeroen Van Der Donckt, Emiel Deprost</i>\n</p>\n\n\n',
    'author': 'Jonas Van Der Donckt, Jeroen Van Der Donckt, Emiel Deprost',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tsflex/tsflex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
