# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memfault_cli']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7,<9',
 'chardet<5.0',
 'mflt-build-id==0.0.5',
 'more_itertools>=8.0.2,<9.0.0',
 'pyaxmlparser>=0.3.24,<0.4.0',
 'pyelftools>=0.26,<=0.29',
 'pyserial>=3.5,<4.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.44.1,<5.0.0',
 'urllib3>=1.26.7']

extras_require = \
{':python_version < "3.7"': ['dataclasses==0.8'],
 ':python_version < "3.8"': ['importlib-metadata==4.8.3']}

entry_points = \
{'console_scripts': ['memfault = memfault_cli.cli:main']}

setup_kwargs = {
    'name': 'memfault-cli',
    'version': '0.18.0',
    'description': 'Memfault CLI tool',
    'long_description': "# Memfault CLI tool\n\nThis package contains the `memfault` CLI tool.\n\nThe purpose of the tool is to make integration with Memfault from other systems,\nlike continuous integration servers, as easy as possible.\n\nInstall the tool and run `memfault --help` for more info!\n\n## Changes\n\n### 0.18.0\n\n- Add new `extra-metadata` option to `upload-ota-payload` to attach custom\n  metadata to that OTA release. The metadata will be returned from Memfault\n  Cloud when fetching the latest Android OTA release.\n- Continue uploading the entire folder of symbols even if any single upload\n  fails due to the symbol file being too large.\n\n### 0.17.0\n\n- Add new `console` command to read SDK exported chunks via a serial port and\n  automatically upload to Memfault.\n\n### 0.16.0\n\n- Add support for uploading Android debug symbols from alternative build\n  systems.\n\n### 0.15.3\n\n- Warn if a non-slug string is passed to the `--project` or `--org` arguments\n\n### 0.15.2\n\n- Don't truncate help output from `click` when the `CI` environment variable is\n  set, for consistent output formatting\n\n### 0.15.1\n\n- Fix some compatibility issues for python3.6 + python3.7\n\n### 0.15.0\n\n- 💥 Breaking change: update the `upload-yocto-symbols` subcommand to take two\n  image paths as required arguments; one for the root filesystem image, and\n  another for the debug filesystem image. Versions 0.14.0 and lower used to take\n  a guess at the path of the debug filesystem image from the value passed to the\n  `--image` param. To avoid confusion and to support all configurations, the\n  Memfault CLI no longer does any guessing and now takes two separate params:\n  `--image` and `--dbg-image`\n\n### 0.14.0\n\n- ✨ Update the `post-chunk` subcommand to split uploads into batches of 500\n  chunks per upload, to avoid timing out when uploading very large chunk logs\n\n### 0.13.0\n\n- 💥 Breaking change: Renamed subcommand `upload-debug-data-recording` to\n  `custom-data-recording`\n\n### 0.12.0\n\n- ✨ Added subcommand `upload-debug-data-recording` for uploading debug data\n  files\n\n### 0.11.0\n\n- ✨ Enable support for Yocto Dunfell based projects (previously supported\n  Kirkstone only)\n\n### 0.10.0\n\n- ✨ Upload-yocto-symbols now uploads additional symbol files\n\n### 0.9.0\n\n- ✨ Expanded support for .elf uploading with the upload-yocto-symbols\n  subcommand\n\n### 0.8.0\n\n- ✨ Initial support for upload-yocto-symbols subcommand\n\n### 0.7.0\n\n- 🐛 Updated to correctly only use the GNU build-id `.note` section\n",
    'author': 'Memfault Inc',
    'author_email': 'hello@memfault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://docs.memfault.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
