from distutils.core import  setup
import setuptools
packages = ['yolov5-5']# 唯一的包名，自己取名
setup(name='bk-yolov5',
	version='1.0',
	author='bkkj',
    packages=packages,
    package_dir={'requests': 'requests'},)
