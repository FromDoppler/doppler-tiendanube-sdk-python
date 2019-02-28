# -*- coding: utf-8 -*-
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'tiendanube',
    packages = [
        'tiendanube',
        'tiendanube.resources',
    ],
    version = '1.2',
    description = '',
    license = 'MIT',
    long_description = read('README.rst'),
    url = 'https://github.com/catalanojuan/tiendanube-python',
    download_url = 'https://github.com/catalanojuan/tiendanube-python/tarball/1.1',


    author = 'Juan Catalano',
    author_email = 'catalanojuan@gmail.com',

    install_requires = [
        "argparse==1.2.1",
        "munch==2.3.2",
        "furl==2.0.0",
        "ipython==7.2.0",
        "mock==1.0.1",
        "orderedmultidict==1.0",
        "py==1.4.15",
        "pytz==2018.9",
        "requests==2.21.0",
    ],

    classifiers = (
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
