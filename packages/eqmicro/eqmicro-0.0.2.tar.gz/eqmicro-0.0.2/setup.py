from setuptools import setup, find_packages

setup(
    name="eqmicro",
    version="0.0.2",  # 0.0.x release for test. current: 0.0.2
    keywords=["eqmicro", "micro", "eqauto"],
    description="python microservice",
    long_description="easy and quick microservice",
    license="MIT",

    url="https://github.com/eqauto/eqmicro.git",
    author="eqauto",
    author_email="eqauto@yeah.net",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)

"""
项目打包
python setup.py bdist_egg           # 生成类似 eqlink-0.0.1-py2.7.egg，支持 easy_install 
# 使用此方式
python setup.py sdist bdist_wheel   # 生成类似 eqlink-0.0.1.tar.gz，支持 pip
# twine 需要安装（pip install twine）
twine upload dist/*
"""
