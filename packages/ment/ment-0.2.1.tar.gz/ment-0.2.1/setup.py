# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ment']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['m = ment.main:main']}

setup_kwargs = {
    'name': 'ment',
    'version': '0.2.1',
    'description': 'python library to write daily log in markdown quickly and to synthesize daily logs based on category',
    'long_description': '# ment\n\n## what is this?\n\n`ment` is a tool to\n\n- write daily logs in markdown quickly\n- synthesize daily logs based on category\n\n    Synthesizing daily logs is like sorting loose-leaf notebook.\n\n\n## installation\n\n```sh\npip install ment\n```\n\n## usage\n\n### start editting\n\n```sh\nm\n```\n\nType `m<Enter>`.\n\nDefault,it means `vim ~/ment_dir/<todays_date>/diary.md`\nIf you want to switch editor, look [configuration](#configuration)\n\n\n### synthesize by tag\n\n```sh\nm synthe <tag_name>\n```\n\nThen, it extracts contents followed by "# <tag_name>" from daily logs,\nand outputs `~/ment_dir/synthe/<tag_name>/synthe_<tag_name>.md`.\n\nIf you want to list tags,`m list`.\n\nTo synthesize recent 7days document,`m week`.\nIt outputs `~/ment_dir/synthe/week/synthe_week.md`.\n\nTo read synthesized documents,`m read <tag_name>`.\n\n### configuration\n\nIf you want to change editor and directory, please set environment variable.\n\n```sh\nexport MENT_DIR="/path/to/documents" \nexport MENT_EDITOR="your editor"\n```\n\nDefault,MENT_DIR is `~/ment_dir/`\n\n### directory structure\n\n```text\n~/ment_dir/\n├── 2021-03-27\n│\xa0\xa0 └── diary.md\n├── 2021-03-28\n│\xa0\xa0 └── diary.md\n├── 2021-03-29\n│\xa0\xa0 └── diary.md\n├── 2021-03-30\n│\xa0\xa0 └── diary.md\n└── synthe\n    ├── tag1\n    │\xa0\xa0 └── synthe_tag1.md\n    ├── tag2\n    │\xa0\xa0 └── synthe_tag2.md\n    ├── tag3\n    │\xa0\xa0 └── synthe_tag3.md\n    └── weeks.md\n\n```\n\n\n### completion\n\nbash-completion file for `ment` is `bash_completion_for_ment`.\n\n\n```sh\ncat bash_completion_for_ment >>  ~/.bash_completion\nsource ~/.bashrc\n```\n\n',
    'author': 'kawagh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kawagh/ment',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
