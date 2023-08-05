#!/usr/bin/env python
# coding=utf-8
import setuptools
with open("README.md", 'r',encoding='UTF-8') as f:
    long_description=f.read()
setuptools.setup(
    name="pip_case",
    version='1.0',
    author="许焕燃",
    author_email='527077832@qq.com',
    description="这是一个pip上传自定义包的测试包",
    long_description=long_description,#详细描述
    long_description_content_type="text/markdown",#详细描述的格式
    # url="https://ssl.xxx.org/redmine/projects/RedisRun", #模块的github地址
    package=setuptools.find_packages(),
    classifiers=[# 程序的所属分类列表
         "Development Status :: 3 - Alpha",
         "Topic :: Utilities",
         "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    install_requires=[# 依赖包
        'pillow'
    ],
    python_requires='>=3'
)
