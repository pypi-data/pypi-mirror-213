# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coresets', 'coresets.algorithms', 'coresets.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.14,<2.0', 'scikit-learn>=1.0,<2.0']

setup_kwargs = {
    'name': 'coresets',
    'version': '0.2.0',
    'description': 'Coreset generation for k-Means and (Bayesian) Gaussian mixture models',
    'long_description': 'Coresets\n--------\nThis library contains the implementation coreset generation for k-Means and (Bayesian) Gaussian mixture models.\nIt also offers the extended versions of the corresponding algorithms that support weighted data sets.\n\nTo get started, take a look at:\n>examples/intro.ipynb\n\n(this is a fork of https://github.com/zalanborsos/coresets, intended to fix installation issues + publish to pypi)\n\nSetup\n-------\n1. Install [poetry](https://python-poetry.org/docs/).\n2.\n```shell\npoetry build\npoetry install\n```\n\nRunning tests\n-------------\nIn project root run:\n```shell\npoetry run pytest\n```\n\n\nReferences\n---------\nThe implementation of the library is based on the following works:\n>Bachem, O., Lucic, M., & Krause, A. (2017). Practical coreset constructions for machine learning. arXiv preprint arXiv:1703.06476.\n\n> Bachem, O., Lucic, M., & Krause, A. (2017). Scalable and distributed clustering via lightweight coresets. arXiv preprint arXiv:1702.08248.\n\n>Lucic, M., Faulkner, M., Krause, A., & Feldman, D. (2018). Training Gaussian Mixture Models at Scale via Coresets. Journal of Machine Learning Research, 18, Art-No.\n\n> Borsos, Z., Bachem, O., & Krause, A. Variational Inference for DPGMM with Coresets. (2017). Advances in Approximate Bayesian Inference\n\n\nPublishing a new version\n------------------------\n```shell\nrm -rf build dist\npoetry build\nmv \n',
    'author': 'Zalán Borsos',
    'author_email': 'zalan.borsos@inf.ethz.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ashtuchkin/coresets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
