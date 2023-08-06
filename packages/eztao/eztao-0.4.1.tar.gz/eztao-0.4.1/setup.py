# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['eztao', 'eztao.carma', 'eztao.ts', 'eztao.viz']

package_data = \
{'': ['*']}

install_requires = \
['celerite>=0.3.0',
 'emcee>=3.0.0',
 'importlib-metadata>=2.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'numba>=0.51.0',
 'scipy>=1.5']

setup_kwargs = {
    'name': 'eztao',
    'version': '0.4.1',
    'description': 'A toolkit for Active Galactic Nuclei (AGN) time-series analysis.',
    'long_description': '![tests](https://github.com/ywx649999311/EzTao/workflows/tests/badge.svg)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ywx649999311/EzTao/v0.4.1?filepath=docs/notebooks)\n[![Documentation Status](https://readthedocs.org/projects/eztao/badge/?version=latest)](https://eztao.readthedocs.io/en/latest/)\n<a href="https://ascl.net/2201.001"><img src="https://img.shields.io/badge/ascl-2201.001-blue.svg?colorB=262255" alt="ascl:2201.001" /></a>\n# EzTao (易道)\n**EzTao** is a toolkit for conducting AGN time-series/variability analysis, mainly utilizing the continuous-time auto-regressive moving average model (CARMA)\n\n## Installation\n<!--- ```\npip install eztao\n```\nor (from master)--->\n```\npip install git+https://github.com/ywx649999311/EzTao.git\n```\n### Dependencies\n>```\n>python = "^3.7"\n>celerite = ">= 0.3.0"\n>matplotlib = "^3.3.0"\n>scipy = "> 1.5.0"\n>numba = ">= 0.51.0"\n>emcee = ">=3.0.0"\n>```\n\n## Quick Examples\nLet\'s first simulate a DRW/CARMA(1,0) process with a variance of 0.3^2 and a relaxation timescale of 100 days. This time series will have a total of 200 data points and span 10 years.\n```python\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom eztao.carma import DRW_term\nfrom eztao.ts import gpSimRand\n\n# define a DRW kernel & and simulate a process\namp = 0.2\ntau = 100\nDRW_kernel = DRW_term(np.log(amp), np.log(tau))\nt, y, yerr = gpSimRand(DRW_kernel, 10, 365*10, 200)\n\n# now, plot it\nfig, ax = plt.subplots(1,1, dpi=150, figsize=(8,3))\nax.errorbar(t, y, yerr, fmt=\'.\')\n...\n```\n![drw_sim](include/drw_sim.png)\n\nWe can fit the simulated time series to the DRW model and see how well we can recover the input parameters.\n```python\nfrom eztao.ts import drw_fit\n\nbest_fit = drw_fit(t, y, yerr)\nprint(f\'Best-fit DRW parameters: {best_fit}\')\n```\n```shell\nBest-fit DRW parameters: [0.17356983 88.36262467]\n```\n\nHow does the power spectrum density (PSD) compare?\n```python\nfrom eztao.carma import gp_psd\n\n# get psd functions\ntrue_psd = gp_psd(DRW_kernel)\nbest_psd = gp_psd(DRW_term(*np.log(best_fit)))\n\n# plot\nfig, ax = plt.subplots(1,1, dpi=150, figsize=(6,3))\nfreq = np.logspace(-5, 2)\nax.plot(freq, true_psd(freq), label=\'Input PSD\')\nax.plot(freq, best_psd(freq), label=\'Best-fit PSD\')\n...\n```\n![drw_psd](include/drw_psd.png)\n\n__Note:__ How well the input and best-fit PSD match is up to how good the best-fit parameters are, which is highly influenced by the quality of the input time series. \n\nFor more examples, please check out the [online documentation](https://eztao.readthedocs.io/en/latest/) or run the tutorial notebooks at ->\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ywx649999311/EzTao/v0.4.0?filepath=docs/notebooks).\n\n## Development\n`poetry` is used to solve dependencies and to build/publish this package. Below shows how setup the environment for development (assuming you already have `poetry` installed on your machine). _**Warning:**_ `poetry` is having issue installing `llvmlite = 0.34.0` (used for `eztao = ^0.4.0`) under Python 3.9. The issue disappears for Python 3.8.\n\n1. Clone this repository, and enter the repository folder.\n2. Create a python virtual environment and activate it (the virtual environment name must be \'.venv\'). \n    ```\n    python -m venv .venv\n    source .venv/bin/activate\n    ```\n3. Install dependencies and **EzTao** in editable mode.\n   ```\n   poetry install\n   ```\n\nNow you should be ready to start adding new features. Be sure to checkout the normal practice regarding how to use `poetry` on its website. When you are ready to push, also make sure the poetry.lock file is checked-in if any dependency has changed. \n\n## Citation\nWe are working on a paper to describe the full implementation of **EzTao**. In the meantime, if you find **EzTao** useful for your research, please consider acknowledging **EzTao** using the following:\n\n```\n@MISC{Yu2022,\n       author = {{Yu}, Weixiang and {Richards}, Gordon T.},\n        title = "{EzTao: Easier CARMA Modeling}",\n     keywords = {Software},\n howpublished = {Astrophysics Source Code Library, record ascl:2201.001},\n         year = 2022,\n        month = jan,\n          eid = {ascl:2201.001},\n        pages = {ascl:2201.001},\narchivePrefix = {ascl},\n       eprint = {2201.001},\n       adsurl = {https://ui.adsabs.harvard.edu/abs/2022ascl.soft01001Y},\n      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n}\n```\n\n',
    'author': 'Weixiang Yu',
    'author_email': 'wy73@drexel.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ywx649999311/EzTao',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
