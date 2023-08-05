# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traductorsqb', 'traductorsqb.matematicas']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'translate==3.5.0']

entry_points = \
{'console_scripts': ['traductorsqb = traductorsqb.__main__:main']}

setup_kwargs = {
    'name': 'traductorsqb',
    'version': '0.0.2',
    'description': 'Traductor de palabras',
    'long_description': '# Traductor\n\nPrograma para traducir palabras de Ingles a Español.\n\n## Instalación\n\nDesde testpypi\n~~~\npip install ..... \n~~~\n\n\nDesde pypi\n~~~\npip install traductorsqb\n~~~\n\n## Forma de uso\n\n~~~\ntraductorsqb "hello"\nhello -> hola\n~~~',
    'author': 'Santiago Quiñones',
    'author_email': 'lsquinones@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lsantiago/package_name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
