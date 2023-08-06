from setuptools import setup,Extension
from pybind11 import get_include
import platform,sys
def readme():
    with open('README.md','r') as file:
        return file.read()
if platform.system()!='Windows':
    raise OSError("Please build in Windows!")
else:
    setup(
        name='mciplayer',
        version='1.0.0',
        description='A simple audio player/recorder using MCI',
        long_description_content_type='text/markdown',
        ext_modules=[
            Extension('mciplayer._mciwnd',sources=['py_mciwnd.cpp'],include_dirs=[get_include()])
        ],
        packages=['mciplayer'],long_description=readme()
    )
