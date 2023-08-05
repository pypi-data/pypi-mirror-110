# encoding: utf-8
"""
@author: liuwz
@time: 2021/6/17 4:18 下午
@file: setup.py.py
@desc: 
"""

from setuptools import setup, find_packages
setup(
    name='tcrCli',
    version='1.0',
    author="tcr-001181",
    description="This is a sample cli for tcr",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'plumbum'
    ],
    entry_points='''
        [console_scripts]
        tcrcli = tcr.main:TcrCli
    ''',

)