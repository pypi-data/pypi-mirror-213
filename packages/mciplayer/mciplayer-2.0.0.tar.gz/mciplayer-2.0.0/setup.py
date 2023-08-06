from setuptools import setup,Extension
from pybind11 import get_include
import platform,sys
def readme():
    with open('README.md','r') as file:
        return file.read()
if platform.system()!='Windows': # Must be a Windows operating system.
    raise OSError("Please build in Windows!")
else:
    setup(
        name='mciplayer',
        version='2.0.0',
        description='A simple audio player/recorder using MCI',
        long_description_content_type='text/markdown',
        ext_modules=[
            Extension('mciplayer._mciwnd',sources=['py_mciwnd.cpp'],include_dirs=[get_include()],language='c++'),
            Extension('mciplayer._mciwnd_unicode',sources=['py_mciwnd_unicode.cpp'],include_dirs=[get_include()],language='c++')
        ],
        packages=['mciplayer'],long_description=readme(),
        entry_points={
            'console_scripts':[
                'play_demo=mciplayer:_play_demo',
                'record_demo=mciplayer:_record_demo'
            ]
        }
    )
