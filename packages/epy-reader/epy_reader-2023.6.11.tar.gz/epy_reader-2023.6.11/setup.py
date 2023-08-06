# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['epy_reader',
 'epy_reader.ebooks',
 'epy_reader.speakers',
 'epy_reader.tools',
 'epy_reader.tools.KindleUnpack']

package_data = \
{'': ['*']}

extras_require = \
{':platform_system == "Windows"': ['windows-curses']}

entry_points = \
{'console_scripts': ['epy = epy_reader.__main__:main']}

setup_kwargs = {
    'name': 'epy-reader',
    'version': '2023.6.11',
    'description': 'TUI Ebook Reader',
    'long_description': '# `$ epy`\n\n[![Downloads](https://static.pepy.tech/personalized-badge/epy-reader?period=month&units=none&left_color=grey&right_color=brightgreen&left_text=downloads/month)](https://pepy.tech/project/epy-reader)\n\n<a href=\'https://ko-fi.com/P5P4IDCX2\' target=\'_blank\'><img height=\'36\' style=\'border:0px;height:36px;\' src=\'https://storage.ko-fi.com/cdn/kofi2.png?v=3\' border=\'0\' alt=\'Buy Me a Coffee at ko-fi.com\' /></a>\n\n![screenshot](https://raw.githubusercontent.com/wustho/epy/master/screenshot.png)\n\nCLI Ebook Reader.\n\nThis is just a fork of [epr](https://github.com/wustho/epr) with these extra features:\n\n- Supported formats:\n  - Epub (.epub, .epub3)\n  - FictionBook (.fb2)\n  - Mobi (.mobi)\n  - AZW3 (.azw, .azw3)\n  - [URL](#url-support)\n- Reading progress percentage\n- Bookmarks\n- External dictionary integration (`sdcv`, `dict` or `wkdict`)\n- Inline formats: **bold** and _italic_ (depend on terminal and font capability. Italic only supported in python>=3.7)\n- Text-to-Speech (with additional setup, read [below](#text-to-speech))\n- [Double Spread](#double-spread)\n- Seamless (disabled by default, read [below](#reading-tips-using-epy))\n\n## Installation\n\n- Via PyPI (Linux and Mac OS)\n\n  ```shell\n  pip3 install epy-reader\n  ```\n\n- Via Pip+Git\n\n  ```shell\n  pip3 install git+https://github.com/wustho/epy\n  ```\n\n- Via AUR\n\n  ```shell\n  yay -S epy-ereader-git\n  ```\n\n- Windows Binary\n\n  Standalone binary for Windows is available at [release page](https://github.com/wustho/epy/releases).\n\n## Usage\n- `epy /path/to/your/book/book.epub` (Remember to make sure your book\'s title doesn\'t contain any spaces)\n- **c** Switching the color profile\n- **Shift + h** Previous chapter\n- **Shift + l** Next chapter\n- **Shift + g** Skip to the end of the chapter\n- **g** Skip to the beginning of the chapter\n- **Shift + m** Show metadata of the book\n- **t** Table of contents\n- **/** Search\n- **b** Add bookmark\n- **Shift + b** Show bookmarks\n- **q** Quit\n- **-** Shrink the text\n- **+** Enlarge the text\n- **o** Open an image\n- **s** Show or hide progress\n\n## Color profiles\nIn the config file you will see the following section.\n   ```\n    "DarkColorFG": 47,\n    "DarkColorBG": 235,\n    "LightColorFG": 238,\n    "LightColorBG": 253,\n   ```\n\nChange the values by using this image. (Make sure to ignore zeros at the beginning, it won\'t launch otherwise.)\n![image](https://user-images.githubusercontent.com/108401269/198876974-c8420de1-b256-42fd-9a09-3a69c5019608.png)\n\n## Reading Tips Using Epy\n\nWhen reading using `epy` you might occasionally find triple asteriks `***`.\nThat means you reach the end of some section in your ebook\nand the next line (right after those three asteriks, which is in new section)\nwill start at the top of the page.\nThis might be disorienting, so the best way to get seamless reading experience\nis by using next-page control (`space`, `l` or `Right`)\ninstead of next-line control (`j` or `Down`).\n\nIf you really want to get seamless reading experience, you can set `SeamlessBetweenChapters`\nto `true` in configuration file. But it has its drawback with more memory usage, that\'s why\nit\'s disabled by default.\n\n## Configuration File\n\nConfig file is available in json format which is located at:\n\n- Linux and Mac OS: `~/.config/epy/configuration.json` or `~/.epy/configuration.json`\n- Windows: `%USERPROFILE%\\.epy\\configuration.json`\n\n## URL Support\n\nYou can read online books like: short stories, fan fiction, etc. using `epy` with an url as cli argument.\nPretty useful when you want to read with less distraction.\n`epy` will also remember your reading progress online.\n\neg. You can read [Moby Dick from gutenberg](https://www.gutenberg.org/files/2701/2701-h/2701-h.htm)\ndirectly with:\n\n```shell\n$ epy https://www.gutenberg.org/files/2701/2701-h/2701-h.htm\n```\n\nBut note that `epy` will never be a web browser, it\'s simply a TUI program to read\nyour favorite fiction stories in the comfort of a terminal.\nSo please do not expect for web browser features to be implemented in `epy`.\n\n## Using Mouse\n\nAlthough mouse support is useful when running `epy` on Termux Android, it’s disabled by default\nsince most people find it intrusive when using `epy` in desktop.\nBut you can enable it by setting `MouseSupport` to `true` in config file.\n\n| Key | Action |\n| --- | --- |\n| `Left Click` (right side of screen) | next page |\n| `Left Click` (left side of screen) | prev page |\n| `Right Click` | ToC |\n| `Scroll Up` | scroll up |\n| `Scroll Down` | scroll down |\n| `Ctrl` + `Scroll Up` | increase text width |\n| `Ctrl` + `Scroll Down` | decrease text width |\n\n## Text-to-Speech\n\nTo get Text-to-Speech (TTS) support, external TTS engine is necessary.\n\nList of supported engines:\n\n- `mimic`\n- `pico2wave`\n- `gtts-mpv` (requires both [gTTS](https://pypi.org/project/gTTS) and [MPV](https://www.mpv.io))\n\n## Dictionary\n\nTo use "Define Word" you will have to install an external dictionary cli program (`sdcv`, `dict` or `wkdict`). After you\'ve done that, it is recommended to manually modify the configuration.json file, and set your desired dictionary there, so everything works properly.\n\nAfter that you will be able to find definition of word by pressing `d`, and aprompt will appear to let you type in word to define.\n\n## Double Spread\n\nDouble spread is intended to mimic the behaviour of real book,\nso line scrolling navigation will act as scrolling page and textwidth is not adjustable.\n\n## Changelog\n\n- `v2021.10.23`: Major refactoring which harness a lot of new stuff in `python>=3.7`\n  and `epy` won\'t be backward compatible with older python version and older configuration.\n\n- `v2022.1.8`: Change in configuration and reading states schema that is not backward compatible.\n  So if error is encountered, deleting the configuration and states file might fix the issue.\n\n- `v2022.1.15`: Early implementation of URL support, table of contents isn\'t available for now.\n\n- `v2022.1.23`: Library implementation: ability to switch ebook from reading history\n  inside epy (default key: `R`).\n\n- `v2022.2.5`: Fix process.join() issue for unstarted process.\n\n- `v2022.10.2`: Major breakdown `epy.py` module into package structure for easier development.\n',
    'author': 'Benawi Adha',
    'author_email': 'benawiadha@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wustho/epy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
