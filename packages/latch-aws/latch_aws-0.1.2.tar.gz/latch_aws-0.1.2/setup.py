# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latch_aws']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore[s3]>=2.4.2,<3.0.0',
 'latch-data-validation>=0.1.3,<0.2.0',
 'latch-o11y>=0.1.4,<0.2.0',
 'opentelemetry-sdk>=1.15.0,<2.0.0',
 'types-aiobotocore[s3]>=2.4.2,<3.0.0']

setup_kwargs = {
    'name': 'latch-aws',
    'version': '0.1.2',
    'description': 'Traced and managed aws resources',
    'long_description': '# python-aws\n',
    'author': 'Max Smolin',
    'author_email': 'max@latch.bio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
