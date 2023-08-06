# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepsearch',
 'deepsearch.artifacts',
 'deepsearch.artifacts.cli',
 'deepsearch.core',
 'deepsearch.core.cli',
 'deepsearch.core.client',
 'deepsearch.core.util',
 'deepsearch.cps',
 'deepsearch.cps.apis',
 'deepsearch.cps.apis.kg',
 'deepsearch.cps.apis.kg.create',
 'deepsearch.cps.apis.kg.create.api',
 'deepsearch.cps.apis.kg.create.models',
 'deepsearch.cps.apis.kg.query',
 'deepsearch.cps.apis.kg.query.api',
 'deepsearch.cps.apis.kg.query.models',
 'deepsearch.cps.apis.public',
 'deepsearch.cps.apis.public.api',
 'deepsearch.cps.apis.public.models',
 'deepsearch.cps.apis.user',
 'deepsearch.cps.apis.user.api',
 'deepsearch.cps.apis.user.models',
 'deepsearch.cps.cli',
 'deepsearch.cps.client',
 'deepsearch.cps.client.builders',
 'deepsearch.cps.client.components',
 'deepsearch.cps.client.queries',
 'deepsearch.cps.client.queries.query_tasks',
 'deepsearch.cps.data_indices',
 'deepsearch.cps.kg',
 'deepsearch.cps.kg.workflow',
 'deepsearch.cps.queries',
 'deepsearch.documents',
 'deepsearch.documents.cli',
 'deepsearch.documents.core',
 'deepsearch.model',
 'deepsearch.model.base',
 'deepsearch.model.examples',
 'deepsearch.model.examples.dummy_nlp_annotator',
 'deepsearch.model.examples.dummy_qa_generator',
 'deepsearch.model.examples.simple_geo_nlp_annotator',
 'deepsearch.model.examples.simple_geo_nlp_annotator.entities',
 'deepsearch.model.examples.simple_geo_nlp_annotator.entities.common',
 'deepsearch.model.examples.simple_geo_nlp_annotator.relationships',
 'deepsearch.model.examples.simple_geo_nlp_annotator.relationships.common',
 'deepsearch.model.kinds',
 'deepsearch.model.kinds.nlp',
 'deepsearch.model.kinds.qagen',
 'deepsearch.model.server',
 'deepsearch.plugins',
 'deepsearch.query',
 'deepsearch.query.cli']

package_data = \
{'': ['*'],
 'deepsearch.artifacts': ['.resources/*'],
 'deepsearch.model.examples.simple_geo_nlp_annotator': ['resources/*']}

install_requires = \
['certifi>=2021.10.8,<2022.0.0',
 'platformdirs>=3.5.1,<4.0.0',
 'pluggy>=1.0.0,<2.0.0',
 'pydantic>=1.10.8,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'six>=1.16.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.64.0,<5.0.0',
 'typer>=0.9.0,<0.10.0',
 'urllib3>=1.26.8,<2.0.0']

extras_require = \
{'all': ['fastapi>=0.95.1,<0.96.0',
         'uvicorn>=0.21.1,<0.22.0',
         'anyio>=3.6.2,<4.0.0',
         'starlette>=0.26.1,<0.27.0'],
 'api': ['fastapi>=0.95.1,<0.96.0',
         'uvicorn>=0.21.1,<0.22.0',
         'anyio>=3.6.2,<4.0.0',
         'starlette>=0.26.1,<0.27.0']}

entry_points = \
{'console_scripts': ['deepsearch = deepsearch.cli:app']}

setup_kwargs = {
    'name': 'deepsearch-toolkit',
    'version': '0.18.0',
    'description': 'Interact with the Deep Search platform for new knowledge explorations and discoveries',
    'long_description': '# Deep Search Toolkit\n\n[![PyPI version](https://img.shields.io/pypi/v/deepsearch-toolkit)](https://pypi.org/project/deepsearch-toolkit/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/deepsearch-toolkit)](https://pypi.org/project/deepsearch-toolkit/)\n[![License MIT](https://img.shields.io/github/license/ds4sd/deepsearch-toolkit)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Docs](https://img.shields.io/badge/website-live-brightgreen)](https://ds4sd.github.io/deepsearch-toolkit/)\n[![Downloads](https://static.pepy.tech/badge/deepsearch-toolkit)](https://pepy.tech/project/deepsearch-toolkit)\n\n\n*Interact with the Deep Search platform for new knowledge explorations and discoveries*\n\n\nThe Deep Search Toolkit is a Python SDK allowing a user to interact with the Deep Search platform. The toolkit provides easy-to-use functionalities for several common processes such as document conversion, graph creation and querying.\n\n\n[Learn about IBM Deep Search](https://ds4sd.github.io/)\n\n\n## Quick links\n\n- [Documentation](https://ds4sd.github.io/deepsearch-toolkit)\n- [Deep Search Examples](https://github.com/ds4sd/deepsearch-examples)\n\n\n## Install\n\nTo set up, just install `deepsearch-toolkit` with your packaging tool.\n\nWith [`poetry`](https://python-poetry.org):\n```console\npoetry add deepsearch-toolkit\n```\n\nWith `pip`:\n```console\npip install deepsearch-toolkit\n```\n\n### Extras\nOptional functionality can be installed as package "extras". To install all extras, use\n`deepsearch-toolkit[all]` with your packaging tool.\n\n### Install as toolkit developer\nIf you are a Deep Search Toolkit developer, set up as follows:\n```console\npoetry install --all-extras\n```\n\n### Requirements\n\nPython 3.8+\n\n## Start using the toolkit\n\n### Login to Deep Search\nFor details, check the [authentication docs](https://ds4sd.github.io/deepsearch-toolkit/getting_started/#authentication).\n```console\ndeepsearch login\n```\n\n### Convert a document\nFor details, check the [document conversion docs](https://ds4sd.github.io/deepsearch-toolkit/guide/convert_doc).\n```console\ndeepsearch documents convert -p 1234567890abcdefghijklmnopqrstvwyz123456 -u https://arxiv.org/pdf/2206.00785.pdf\n```\n\nThe output should look like:\n```\nSubmitting input:     : 100%|██████████████████████████████| 1/1 [00:01<00:00,  1.52s/it]\nConverting input:     : 100%|██████████████████████████████| 1/1 [00:33<00:00, 33.80s/it]\nDownloading result:   : 100%|██████████████████████████████| 1/1 [00:01<00:00,  1.11s/it]\nTotal online documents             1\nSuccessfully converted documents   1\n```\n\n\n## Get help and support\n\nPlease feel free to connect with us using the [discussion section](https://github.com/DS4SD/deepsearch-toolkit/discussions).\n\n\n## Contributing\n\nPlease read [Contributing to Deep Search Toolkit](./CONTRIBUTING.md) for details.\n\n\n## References\n\nIf you use `Deep Search` in your projects, please consider citing the following:\n\n```bib\n@software{Deep Search Toolkit,\nauthor = {Deep Search Team},\nmonth = {6},\ntitle = {{Deep Search Toolkit}},\nurl = {https://github.com/DS4SD/deepsearch-toolkit},\nversion = {main},\nyear = {2022}\n}\n```\n\n## License\n\nThe `Deep Search Toolkit` codebase is under MIT license.\nFor individual model usage, please refer to the model licenses found in the original packages.\n',
    'author': 'Michele Dolfi',
    'author_email': 'dol@zurich.ibm.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ds4sd.github.io/deepsearch-toolkit/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
