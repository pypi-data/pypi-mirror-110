# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsflex',
 'tsflex.chunking',
 'tsflex.features',
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
    'version': '0.1.0',
    'description': 'Toolkit for flexible operations on time-series data',
    'long_description': '# <p align="center"><img alt="tsflex" src="./docs/_static/logo.png" height="100"></p>\n\n*tsflex* stands for: _**flex**ible **t**ime-**s**eries operations_<br>\n\nIt is a `time-series first` toolkit for **processing & feature extraction**, making few assumptions about input data. \n\n* [example notebooks](examples/)\n\n## Table of contents\n  - [Installation](#installation)\n  - [Usage](#usage)\n    - [Series processing](#series-processing)\n    - [Feature extraction](#feature-extraction-1)\n  - [Documentation](#documentation)\n\n\n## Installation\n\n`:WIP: - not yet published to pypi`\n\n```sh\npip install tsflex\n```\n\n## Advantages of tsflex\n\n*tsflex* has multiple selling points, for example\n\n`todo: create links to example benchmarking notebooks`\n\n* it is efficient\n  * execution time -> multiprocessing / vectorized\n  * memory -> view based operations\n* it is flexible:  \n  **feature extraction**:\n     * multiple series, signal & stride combinations are possible\n     * no frequency requirements, just a datetime index\n* it has logging capabilities to improve feature extraction speed.  \n* it is field & unit tested\n* it has a comprehensive documentation\n* it is compatible with sklearn (w.i.p. for gridsearch integration), pandas and numpy\n\n## Usage\n\n### Series processing\n\n```python\nimport pandas as pd\nimport scipy.stats\nimport numpy as np\n\nfrom tsflex.processing import SeriesProcessor, SeriesPipeline\n\n\n```\n\n\n### Feature extraction\n\nThe only data assumptions made by tsflex are:\n* the data has a `pd.DatetimeIndex` & this index is `monotonically_increasing`\n* the data\'s series names must be unique\n\n\n```python\nimport pandas as pd\nimport scipy.stats\nimport numpy as np\n\nfrom tsflex.features import FeatureDescriptor, FeatureCollection\n\n# 1. Construct the collection in which you add all your features\nfc = FeatureCollection(\n    feature_descriptors=[\n        FeatureDescriptor(\n            function=scipy.stats.skew,\n            series_name="myseries",\n            window="1day",\n            stride="6hours"\n        )\n    ]\n)\n# -- 1.1 Add another feature to the feature collection\nfc.add(FeatureDescriptor(np.min, \'myseries\', \'2days\', \'1day\'))\n\n# 2. Get your time-indexed data\ndata = pd.Series(\n    data=np.random.random(10_000), \n    index=pd.date_range("2021-07-01", freq="1h", periods=10_000),\n).rename(\'myseries\')\n# -- 2.1 drop some data, as we don\'t make frequency assumptions\ndata = data.drop(np.random.choice(data.index, 200, replace=False))\n\n# 3. Calculate the feature on some data\nfc.calculate(data=data, n_jobs=1, return_df=True)\n# which outputs: a pd.DataFrame with content:\n```\n|      index               |   **myseries__skew__w=1D_s=12h**  |    **myseries__amin__w=2D_s=1D** |\n|:--------------------|-------------------------------:|------------------------------:|\n| 2021-07-02 00:00:00 |                     -0.0607221 |                   nan         |\n| 2021-07-02 12:00:00 |                     -0.142407  |                   nan         |\n| 2021-07-03 00:00:00 |                     -0.283447  |                     0.042413  |\n| 2021-07-03 12:00:00 |                     -0.353314  |                   nan         |\n| 2021-07-04 00:00:00 |                     -0.188953  |                     0.0011865 |\n| 2021-07-04 12:00:00 |                      0.259685  |                   nan         |\n| 2021-07-05 00:00:00 |                      0.726858  |                     0.0011865 |\n| ... |                      ...  |                     ... |\n\n\n## Documentation\n\n`:WIP:`\n\nToo see the documentation locally, install [pdoc](https://github.com/pdoc3/pdoc) and execute the succeeding command from this folder location.\n\n```sh\npdoc3 --template-dir docs/pdoc_template/ --http :8181 tsflex\n```\n\n<br>\n\n\n\n---\n<p align="center">\n👤 <i>Jonas Van Der Donckt, Jeroen Van Der Donckt, Emiel Deprost</i>\n</p>\n\n\n',
    'author': 'Emiel Deprost',
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
