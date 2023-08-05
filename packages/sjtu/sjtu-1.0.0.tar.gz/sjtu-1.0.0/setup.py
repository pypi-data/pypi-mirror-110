from __future__ import print_function
from setuptools import setup, find_packages
import sys
setup(
    name="sjtu",
    version="1.0.0",
    author="sjtu·jiaer",
    author_email="546957533@qq.com",
    description="深圳市welab的工作-特殊项目",
    long_description=open("README.txt",encoding="utf8").read(),


    # url="https://github.com/",
    packages=find_packages(),
    package_data={  # "zhulong.hunan":["profile"]
    },
    install_requires=[
        "pandas >= 0.13",
        "numpy",
        "selenium",
        "xlsxwriter",
        "xlrd",
        "sqlalchemy",
        "gzqzl",
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
)