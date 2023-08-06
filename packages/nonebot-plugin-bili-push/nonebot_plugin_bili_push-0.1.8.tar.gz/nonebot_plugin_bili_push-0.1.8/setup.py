#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages


# def get_install_requires():
#     reqs = [
#         'pillow>=9.5.0',
#         'httpx>=0.24.1',
#         'h2>=4.1.0',
#         'nonebot2>=2.0.0',
#         'nonebot_adapter_onebot>=2.2.3',
#         'nonebot_plugin_apscheduler>=0.2.0'
#     ]
#     return reqs

def get_install_requires():
    reqs = [
        'pillow>=9.5.0',
        'requests>=2.31.0',
        'nonebot2>=2.0.0',
        'nonebot_adapter_onebot>=2.2.3',
        'nonebot_plugin_apscheduler>=0.2.0'
    ]
    return reqs


setup(name='nonebot_plugin_bili_push',
      version='0.1.8',
      description='nonebot2 plugin',
      author='SuperGuGuGu',
      author_email='13680478000@163.com',
      url='https://github.com/SuperGuGuGu/nonebot_plugin_bili_push',
      packages=find_packages(),
      python_requires=">=3.8",
      install_requires=get_install_requires(),
      package_data={'': ['*.csv', '*.txt', '.toml']},
      include_package_data=True
      )
