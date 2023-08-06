# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prefab_cloud_python']

package_data = \
{'': ['*']}

modules = \
['prefab_pb2', 'prefab_pb2_grpc']
install_requires = \
['grpcio-tools>=1.51.3,<2.0.0',
 'grpcio>=1.51.3,<2.0.0',
 'mmh3>=3.0.0,<4.0.0',
 'pytest>=7.2.1,<8.0.0',
 'pyyaml>=6.0.0,<7.0.0',
 'sseclient-py>=1.7.2,<2.0.0',
 'structlog>=22.3,<23.0',
 'timecop>=0.5.0dev,<0.6.0',
 'urllib3>=2.0,<3.0']

setup_kwargs = {
    'name': 'prefab-cloud-python',
    'version': '0.3.0',
    'description': 'Python client for Prefab Feature Flags, Dynamic log levels, and Config as a Service: https://www.prefab.cloud',
    'long_description': '# prefab-cloud-python\n\nPython client for prefab.cloud, providing Config, FeatureFlags as a Service\n\n**Note: This library is under active development and not quite ready for production usage**\n\n[Sign up to be notified when this library releases](https://forms.gle/2qsjMFvjGnkTnA9T8)\n\n## Example usage\n\n```python\nfrom prefab_cloud_python import Client, Options\n\noptions = Options(\n    prefab_api_key="your-prefab-api-key"\n)\n\ncontext = {\n  "user": {\n    "team_id": 432,\n    "id": 123,\n    "subscription_level": \'pro\',\n    "email": "alice@example.com"\n  }\n}\n\nclient = Client(options)\n\nresult = client.enabled("my-first-feature-flag", context=context)\n\nprint("my-first-feature-flag is:", result)\n```\n\nSee full documentation https://docs.prefab.cloud/docs/python-sdk/python\n',
    'author': 'Michael Berkowitz',
    'author_email': 'michael.berkowitz@gmail.com',
    'maintainer': 'Michael Berkowitz',
    'maintainer_email': 'michael.berkowitz@gmail.com',
    'url': 'https://www.prefab.cloud',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
