# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repo_cli',
 'repo_cli.Maverick',
 'repo_cli.Maverick.Templates',
 'repo_cli.Maverick.mistune_plugins']

package_data = \
{'': ['*'],
 'repo_cli': ['default_dir/*',
              'default_dir/test_src/*',
              'default_dir/test_src/assets/*',
              'default_dir/test_src/static/*',
              'default_dir/test_src/static/bg/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'Pillow>=8.2.0,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'Pygments>=2.9.0,<3.0.0',
 'chardet>=4.0.0,<5.0.0',
 'click>=7.0,<8.0',
 'feedgen>=0.9.0,<0.10.0',
 'mistune==2.0.0a4',
 'moment>=0.12.1,<0.13.0']

entry_points = \
{'console_scripts': ['repo-cli = repo_cli.entry:main']}

setup_kwargs = {
    'name': 'repo-cli',
    'version': '0.0.1.8',
    'description': 'standard tooling for repo project.',
    'long_description': '# repo-cli\nstandard tooling for repo project.\n\n## note\n\nThe project is under development, please do not install and use it for now.',
    'author': 'RyomaHan',
    'author_email': 'ryomahan1996@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ryomahan/repo-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
