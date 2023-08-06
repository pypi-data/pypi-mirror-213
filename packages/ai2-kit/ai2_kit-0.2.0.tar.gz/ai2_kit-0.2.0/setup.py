# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ai2_kit',
 'ai2_kit.algorithm',
 'ai2_kit.core',
 'ai2_kit.dflow',
 'ai2_kit.domain',
 'ai2_kit.tools',
 'ai2_kit.workflow']

package_data = \
{'': ['*']}

install_requires = \
['ase>=3.22.1,<4.0.0',
 'cloudpickle>=2.2.0,<3.0.0',
 'cp2k-input-tools>=0.8.2,<0.9.0',
 'dpdata>=0.2.13,<0.3.0',
 'fabric>=2.7.1,<3.0.0',
 'fire>=0.4.0,<0.5.0',
 'invoke>=1.7.3,<2.0.0',
 'mdanalysis>=2.4.3,<3.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pymatgen>=2023.2.22,<2024.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'shortuuid>=1.0.11,<2.0.0']

entry_points = \
{'console_scripts': ['ai2-kit = ai2_kit.main:main']}

setup_kwargs = {
    'name': 'ai2-kit',
    'version': '0.2.0',
    'description': '',
    'long_description': '# ai<sup>2</sup>-kit\n\nA toolkit featured ***a**rtificial **i**ntelligence × **a**b **i**nitio* for computational chemistry research.\n\n*Please be advised that `ai2-kit` is still under heavy development and you should expect things to change often. We encourage people to play and explore with `ai2-kit`, and stay tuned with us for more features to come.*\n\n\n## Feature Highlights\n* Collection of tools to facilitate the development of automated workflows for computational chemistry research.\n* Utilities to execute and manage jobs in local or remote HPC job scheduler.\n* Utilities to simplified automated workflows development with reusable components. \n\n## Installation\n\nYou can use the following command to install `ai2-kit`:\n\n```bash\npip install ai2-kit  \n\nai2-kit --help\n```\n\nIf you want to run `ai2-kit` from source, you can run the following commands in the project folder:\n\n```bash\npip install poetry\npoetry install\n\n./ai2-kit --help\n```\n\n## Manuals\n\n* [Proton Transfer Analysis Toolkit](doc/manual/proton-transfer.md)\n* [CLL MLP Training Workflow](doc/manual/cll-workflow.md)\n* [FEP MLP Training Workflow](doc/manual/fep-workflow.md)\n\n## Tutorials\n\n## Notebooks\n',
    'author': 'weihong.xu',
    'author_email': 'xuweihong.cn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
