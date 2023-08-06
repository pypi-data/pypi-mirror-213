#!/usr/bin/env python
from io import open
from setuptools import setup, find_packages
# from distutils.core import setup
# setup(name="dfkv", version="0.0.6", description="test to install module", author="someone", py_modules=['dfkv.common'])
setup(
    name='dfkv',
    version='0.0.9',
    description='a expand for dict',
    long_description='expand dict, can use a.b, can set value more than 1-level a.b.c.d="xyz"',
    author='fred deng',
    author_email='dfgeoff@qq.com',
    license='Apache License 2.0',
    url='https://gitee.com/hifong45/dkv.git',
    download_url='https://gitee.com/hifong45/dkv/master.zip',
    packages=find_packages(exclude=["examples", "project", "tests", "*.tests", "*.tests.*"]),  # 必填
    # package_dir={'': 'src'},  # 必填
    install_requires=[]
)
# 本地测试时，使用： rd /s /q dist && python setup.py sdist && pip uninstall -y dfkv && pip install dist\dfkv-0.0.9.tar.gz
# 要上传时，用：rd /s /q dist && python setup.py sdist && twine upload dist/*
# 指定用标准中心库： pip install -i https://pypi.Python.org/simple/ dfkv
# 2023-01-28 16:16:52.993077