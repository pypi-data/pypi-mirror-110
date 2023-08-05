# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_forms']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.13,<3.0']

setup_kwargs = {
    'name': 'aiogram-forms',
    'version': '0.1.0',
    'description': 'Forms for aiogram',
    'long_description': '# aiogram-forms\n\n## Introduction\n`aiogram-forms` is an addition for `aiogram` which allows you to create different forms and process user input step by step easily.\n\n## Installation\n```bash\npip install aiogram-forms\n```\n\n## Usage\nCreate form you need by subclassing `aiogram_forms.forms.Form`. Fields can be added with `aiogram_forms.fields.Field` \n```python\nfrom aiogram_forms import forms, fields\n\nclass UserForm(forms.Form):\n    """User profile data form"""\n    name = fields.StringField(\'Name\')\n    language = fields.StringField(\'Language\', choices=(\'English\', \'Russian\', \'Chinese\'))\n    email = fields.EmailField(\'Email\')\n```\n\n## Code of Conduct\n\n## History\nAll notable changes to this project will be documented in [CHANGELOG](CHANGELOG.md) file.\n',
    'author': 'Ivan Borisenko',
    'author_email': 'i.13g10n@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/13g10n/aiogram-forms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
