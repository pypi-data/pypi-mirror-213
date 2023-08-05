# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enalog']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'enalog',
    'version': '0.2.1',
    'description': 'Python package for sending events to EnaLog',
    'long_description': "# enalog-py\n\nEnaLog Python SDK\n\n### Usage\n\n```python\nfrom enalog import push\n\npush_event(api_token='dummy_api_token', event={\n    'project': 'enalog'\n    'name': 'user-subscribed',\n    'description': 'User has subscribed to EnaLog',\n    'push': False,\n    'icon': '💰',\n    'tags': ['app': 'EnaLog'],\n    'meta': {'user_id': 123},\n    'channels': {'slack': '<slack-channel-name>'}\n})\n```\n",
    'author': 'Sam Newby',
    'author_email': 'sam.newby19@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
