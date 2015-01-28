#!/usr/bin/env python

import os.path as op

from setuptools import setup


def read(filename):
    """Reads a readme file. Used to fill the `long_description`.
    
    :param filename: Name of the readme file
    :type filename: str or unicode
    :returns: Content of the file
    :rtype: unicode
    
    """
    with open(op.join(op.dirname(__file__), filename), 'r') as handler:
        content = handler.read()
        handler.close()
    return content

setup(
    name = 'Steno',
    version = '0.1b3',
    description = ('An application that helps people learning a foreign '
                   'language to train listening skills.'),
    long_description = read('README.rst'),
    author = 'Anton Konyshev',
    author_email = 'anton.konyshev@gmail.com',
    url = 'https://github.com/antonkonyshev/steno/',
    packages = ['steno', 'steno.test'],
    install_requires = [
        'wxPython>=2.8.12.1',
        'pysrt>=1.0.1',
        'google_translate_api>=0.3',
    ],
    package_data = {
        'steno': ['resources/img/*.png', 'resources/html/*.html'],
    },
    license = 'wxWidgets Library License (LGPL derivative)',
    keywords = 'language listening trainer learning education',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Multimedia :: Video :: Display',
    ],
    entry_points={
        'gui_scripts': [
            'steno = steno.steno:main',
        ],
    }
)