# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fal_serverless',
 'fal_serverless.auth',
 'fal_serverless.console',
 'fal_serverless.exceptions',
 'fal_serverless.logging']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=4.1.0,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'datadog-api-client==2.12.0',
 'dill==0.3.5.1',
 'grpc-interceptor>=0.15.0,<0.16.0',
 'grpcio>=1.50.0,<2.0.0',
 'isolate-proto>=0.0.30,<0.0.31',
 'isolate[build]>=0.12.2,<1.0',
 'opentelemetry-api>=1.15.0,<2.0.0',
 'opentelemetry-sdk>=1.15.0,<2.0.0',
 'packaging>=21.3',
 'pathspec>=0.11.1,<0.12.0',
 'portalocker>=2.7.0,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=13.3.2,<14.0.0',
 'structlog>=22.3.0,<23.0.0',
 'typing-extensions==4.4']

extras_require = \
{':python_version < "3.10"': ['importlib-metadata>=4.4']}

entry_points = \
{'console_scripts': ['fal-serverless = fal_serverless.cli:cli']}

setup_kwargs = {
    'name': 'fal-serverless',
    'version': '0.6.34',
    'description': 'fal Serverless is an easy-to-use Serverless Python Framework',
    'long_description': '# fal-serverless\n\nLibrary to run, serve or schedule your Python functions in the cloud with any machine type you may need.\n\nCheck out to the [docs](https://docs.fal.ai/fal-serverless/quickstart) for more details.\n',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
