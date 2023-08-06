# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_select']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.14.0']

setup_kwargs = {
    'name': 'textual-select',
    'version': '0.3.4',
    'description': 'A select widget (aka dropdown) for Textual.',
    'long_description': '# Textual: Select\n\nIMPORTANT: Since version 0.24.0 Textual implemented a native dropdown. I strongly\nrecommend to use the native version. This repository will slowly die. More information\nat the [Blog Post about Select control](https://textual.textualize.io/blog/2023/05/08/textual-0240-adds-a-select-control/).\n\nA simple select widget (aka dropdown) for [textual](https://github.com/Textualize/textual) with an optional search field.\n\n![select_focus](https://user-images.githubusercontent.com/922559/209305346-6b8971b1-7a3a-4424-bdf8-c439b9d74e28.png)\n\n![select_open](https://user-images.githubusercontent.com/922559/209305349-84f39432-b1e4-405e-8854-a8d7a33230ae.png)\n\n![select_search](https://user-images.githubusercontent.com/922559/209305352-9ad2e7c1-9dc6-435f-b1bd-8dba5f5b2642.png)\n\n\n## Usage\n\n```python\nfrom textual_select import Select\n\ndropdown_data = [\n    {"value": 0, "text": "Pick-Up"},\n    {"value": 1, "text": "SUV"},\n    {"value": 2, "text": "Hatchback"},\n    {"value": 3, "text": "Crossover"},\n    {"value": 4, "text": "Convertible"},\n    {"value": 5, "text": "Sedan"},\n    {"value": 6, "text": "Sports Car"},\n    {"value": 7, "text": "Coupe"},\n    {"value": 8, "text": "Minivan"}\n]\n\nSelect(\n    placeholder="please select",\n    items=dropdown_data,\n    list_mount="#main_container"\n)\n```\n\n## Installation\n\n```bash\npip install textual-select\n```\n\nRequires textual 0.11.0 or later.\n\n## Limitations\n\nThis textual widget is in early stage and has some limitations:\n\n* It needs a specific mount point (`list_mount`) where the dropdown list\n  shall appear. This is needed because the container widget with the select\n  itself could be too small. Maybe in future versions this will no longer\n  needed.\n* It can only open below, not above: Make sure to reserve space below the\n  dropdown.\n* The dropdown list has a fixed height of 5 entries. This will be configurable\n  in future versions.\n\n## Similar Widgets\n\n* If you are looking for an autocomplete, please refer to\n  [textual-autocomplete](https://github.com/darrenburns/textual-autocomplete)\n  by Darren Burns.\n',
    'author': 'Mischa Schindowski',
    'author_email': 'mschindowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mitosch/textual-select',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
