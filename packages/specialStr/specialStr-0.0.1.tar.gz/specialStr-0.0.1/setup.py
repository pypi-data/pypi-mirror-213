# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name = 'specialStr',
    version = '0.0.1',
    keywords = ['string'],
    description = 'Manage strings more easily',
    long_description = open("README.rst","r",encoding="utf-8").read(),
    author = 'kuankuan',
    author_email = '2163826131@qq.com',
    url="https://kuankuan2007.gitee.io/docs/do-folder/",
    install_requires = [
        "typing-extensions"
    ],
    packages = ['specialStr'],
    
    license = 'Mulan PSL v2',
    platforms=[
        "windows",
        "linux",
        "macos"
    ] ,
    classifiers = [
        "Natural Language :: English",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)'
    ]
)
