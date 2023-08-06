# -*- coding: utf-8 -*-
# @Time    : 2023/6/12-11:39
# @Author  : 灯下客
# @Email   :
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='easy-config-py',
    version='0.0.3',
    packages=['easy_config'],
    install_requires=['anyconfig'],
    license='MIT',
    description='',
    author='cookieGeGe',
    author_email='zhang1114570651@gmail.com',
    keywords=['easy', 'config', 'addict', 'anyconfig'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cookieGeGe/py_easy_config",
    include_package_data=True,
    python_requires='>=3.6',
    platforms='any',
)
