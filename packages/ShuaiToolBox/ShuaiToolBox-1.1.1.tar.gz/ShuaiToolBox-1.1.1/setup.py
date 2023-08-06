from distutils.core import  setup
import setuptools
packages = ['ShuaiToolBox']
setup(name='ShuaiToolBox',
	version='1.1.1',
	author='ShuaiZheng',
    packages=setuptools.find_packages(), 
    package_dir={'requests': 'requests'},)
