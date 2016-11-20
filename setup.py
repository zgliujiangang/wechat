# Fix for older setuptools
import re
import os

from setuptools import setup, find_packages


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
	with open(fpath(fname)) as fd:
		return fd.read()


file_text = read(fpath('wechat_sdk/__init__.py'))



def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    name='wechat_sdk',
    version=grep('__version__'),
    url='https://github.com/zgliujiangang/wechat',
    license='',
    author=grep('__author__'),
    author_email=grep('__email__'),
    description='Simple interface framework for wechat',
    long_description="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests',
        'poster'
    ]
)