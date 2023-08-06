# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bl_seth']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bl-seth',
    'version': '0.2.0',
    'description': 'Setting management library',
    'long_description': '# Seth\n\nA setting management library. By grouping all your application settings in one class,\nit\'s easier to document.\n\nFirst, define a class for your settings. It must be a `dataclass` (or even better,\na frozen `dataclass`) and inherit from `seth.Settings`.\n\n```python\nfrom dataclasses import dataclass\nfrom typing import Optional\n\nfrom bl_seth import Settings\n\n@dataclass\nclass MySettings(Settings):\n    MANDATORY: str\n    "A mandatory string."\n    \n    DEFAULT: str = "default"\n    """A string that defaults to \'"default"\'."""\n\n    INTEGER: int = 1\n    "An integer that defaults to \'1\'."\n\n    OPTIONAL: Optional[str] = None\n    "An optional value."\n```\n\nThen instantiate it using its `from_dict` class method. Most probably, the dictionary\nis built from the environment.\n\n```python\nimport os\n\nsettings = MySettings.from_dict(os.environ)\n```\n\nYou can now directly access its attributes.\n\n```python\nsettings.DEFAULT == "default"\nsettings.OPTIONAL is None\n```\n',
    'author': 'Tanguy Le Carrour',
    'author_email': 'tanguy@bioneland.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.easter-eggs.org/bioneland/bl-seth',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
