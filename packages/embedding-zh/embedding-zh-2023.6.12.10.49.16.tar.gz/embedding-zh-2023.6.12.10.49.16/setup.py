#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.iapp
# @File         : setup
# @Time         : 2019-06-17 16:12
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : https://note.qidong.name/2018/01/python-setup-requires/

import time
import pandas as pd
from pathlib import Path
from setuptools import find_packages, setup

# rename
DIR = Path(__file__).resolve().parent
package_name = DIR.name
version = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

get_requirements = lambda p='requirements.txt': pd.read_csv(p, comment='#', names=['name']).name.tolist()
extras_require = {v.name.split('_')[1][:-4]: get_requirements(v) for v in DIR.glob('requirements_*')}
extras_require['all'] = list(set(sum(extras_require.values(), [])))



setup(
    name=package_name,
    version=version,
    url=f'https://github.com/yuanjie-ai/{package_name}',
    keywords=['utils'],
    description=('description'),
    long_description_content_type="text/markdown",
    author='yuanjie',
    maintainer='yuanjie',
    author_email='313303303@qq.com',
    maintainer_email='313303303@qq.com',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    # package_data={'': ['*.*']},

    platforms=["all"],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
    ],

    python_requires='>=3.7',
    setup_requires=["pandas"],
    install_requires=get_requirements(),
    extras_require=extras_require,  # pip install -U meutils\[all\]

)
