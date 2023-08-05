import sys
from pathlib import Path
import os
from setuptools import setup


def get_version():
    with open(os.path.join('src','pyved','VERSION')) as version_file:
        return version_file.read().strip()


sys.path.append('src')
# import pyved

# - fetch data from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

# read the contents of the README file


this_directory = Path(__file__).parent
long_desc = (this_directory / "README.md").read_text()

setup(
    name="pyved",

    author="moonb3ndr et al.",
    author_email="contact@kata.games",
    url="https://github.com/wkta/gamedev-pyved",

    long_description=long_desc,
    long_description_content_type='text/markdown',

    install_requires=required,

    package_dir={'': 'src'},
    packages=[
        "pyved",
    ],

    include_package_data=True,  # to be sure we get _sm_shelf/legacy.py, etc.

    description='experimental toolbox for game devs who use python',
    license='LGPL-3.0',
    version=str(get_version()),

    entry_points={
        'console_scripts': [
            'pyved = pyved.__main__:main'
        ]
    }
)
