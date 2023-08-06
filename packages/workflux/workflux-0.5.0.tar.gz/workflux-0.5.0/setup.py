#!/usr/bin/env python3
import os
from setuptools import find_packages, setup

SETUP_DIR = os.path.dirname(__file__)
with open(os.path.join(SETUP_DIR, 'README.md')) as file:
    readme = file.read()

setup(
    name='workflux',
    version='0.5.0',    
    description='A platform-agnostic, cloud-ready framework for simplified deployment of the Common Workflow Language using a graphical web interface',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/CompEpigen/workflUX',
    download_url="https://github.com/CompEpigen/workflUX",
    author='Kersten Henrik Breuer',
    author_email='k.breuer@dkfz.de',
    license='Apache 2.0',
    include_package_data=True,
    packages=find_packages(exclude=("tests",)),
    entry_points={
        "console_scripts": [
            "workflux=workflux.__main__:main",
        ]
    },
    extras_require={
        'testing': [
            'pytest',
        ],
    },
    install_requires=[
        'werkzeug',
        'flask',
        'flask_wtf',
        'flask-login',
        'flask-sqlalchemy',
        'pyexcel',
        'pyexcel-io',
        'pyexcel-ods',
        'pyexcel-ods3',
        'pyexcel-xls',
        'pyexcel-xlsx<=0.5.7',
        'PyYAML>=5.1',
        'pexpect',
        'janis-pipelines',
        'cwltool==3.0.20201203173111',
        'psutil',
        'miniwdl>=0.0.5',
        'requests',
        'path<13.2.0',
        'schema-salad>=7.0.20200811075006',
        'trs-cli>=0.3.1',
        'pydantic',
        "cwlformat<=2020.5.19"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX', 
        'Operating System :: POSIX :: Linux',    
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 8.1', 
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: System :: Distributed Computing',
    ]
)
