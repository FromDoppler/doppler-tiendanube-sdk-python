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
    version = '1.2.2',
    description = '',
    license = 'MIT',
    long_description = read('README.rst'),
    url = 'https://github.com/catalanojuan/tiendanube-python',
    download_url = 'https://github.com/catalanojuan/tiendanube-python/tarball/1.1',


    author = 'Juan Catalano',
    author_email = 'catalanojuan@gmail.com',

    install_requires = [
        "argparse==1.4.0",
        "munch==4.0.0",
        "furl==2.1.3",
        "ipython==8.25.0",
        "mock==5.1.0",
        "orderedmultidict==1.0.1",
        "py==1.11.0",
        "pytz==2024.1",
        "requests==2.31.0",
    ],

    classifiers = (
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
    ),
)
