# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biliarchiver', 'biliarchiver.utils']

package_data = \
{'': ['*']}

install_requires = \
['bilix==0.18.3', 'danmakuc>=0.3.6,<0.4.0', 'internetarchive>=3.5.0,<4.0.0']

entry_points = \
{'console_scripts': ['bili_archive_bvids = '
                     'biliarchiver:bili_archive_bvids.main',
                     'bili_get_bvids = biliarchiver:bili_get_bvids.main',
                     'bili_upload = biliarchiver:bili_upload.main']}

setup_kwargs = {
    'name': 'biliarchiver',
    'version': '0.0.15',
    'description': '',
    'long_description': '# biliarchiver\n\n## 基于 bilix 的 BiliBili 存档工具\n\n~~ IA iteam identifier 格式兼容 tubeup ~~。  \n现在不兼容了，Tubeup 不适合存 B 站视频，它的 identifier 设计不科学，大规模存档必定会撞车。\n\n目前，我可能随时 commit 乱飞且动不动就 git push -f 这个仓库。（为了在我的 vps 和本地之间同步代码）\n\nuserscript.js 还没适配新换的 identifier 格式。\n',
    'author': 'yzqzss',
    'author_email': 'yzqzss@yandex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
