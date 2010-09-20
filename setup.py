import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "nw-nwlogger",
    version = "0.1",
    url = 'http://github.com/un33k/nw-nwlogger',
    license = 'BSD',
    description = "An app to simplify logging in python for average users",
    long_description = read('README'),

    author = 'Val Lee',
    author_email = 'uneekvu@gmail.com',

    packages = find_packages('src'),
    package_dir = {'': 'src'},
    
    install_requires = ['setuptools'],

    classifiers = [
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
    ]
)
