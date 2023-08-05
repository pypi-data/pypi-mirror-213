#!/usr/bin/env python3
# coding=utf-8

from setuptools import setup

version = '1.2.4'

setup(
    name='callmebot',
    packages=['callmebot'],
    package_data={"callmebot": ["__init__.pyi", "py.typed"]},
    install_requires=[
        'requests',
        'typer',
        'rich',
        'html2text',
    ],
    version=version,
    description='CallMeBot Python Client',
    long_description='CallMeBot Python Client',
    author='Jordi Petit',
    author_email='jpetit@cs.upc.edu',
    url='https://github.com/jutge-org/callmebot',
    download_url='https://github.com/jutge-org/callmebot/tarball/{}'.format(version),
    keywords=['callmebot'],
    license='Apache',
    zip_safe=False,
    include_package_data=True,
    setup_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'callmebot=callmebot:cmd.main',
        ]
    },
    scripts=[
    ]
)
