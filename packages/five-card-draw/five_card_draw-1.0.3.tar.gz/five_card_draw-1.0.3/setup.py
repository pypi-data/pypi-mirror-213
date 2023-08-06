'''Setup file for building a pip for a module.

Local Install Process:

Build Pip Distributable: py -m build --wheel from the /PythonTools/ directory with this setup.py in it. Then install from the .whl file.
INSTRUCTIONS FOR BUILDING A PIP https://pip.pypa.io/en/stable/cli/pip_wheel/
OR
Developer Install: "py -m pip install -e ." from this folder.

Publish a Pip Version to PyPi:
0. Create an account https://pypi.org/account/register/
1. Install Prequisites: py -m pip install --upgrade pip setuptools wheel twine build
2. py setup.py sdist bdist_wheel
3. py -m twine upload dist/*

'''
import os
from pathlib import Path
import setuptools

requires = [
    'tk',
    'pathlib'
]
scripts = [
    #str(Path('src/5_card_draw','five_card_draw.py'))
]

#Package setuptools pypi install for local developer installs
setuptools.setup(
    name = 'five_card_draw',
    version = os.getenv('PACKAGE_VERSION', '1.0.3'),
    description = '5 Card Draw Video Poker application',
    author = 'Richard Albee',
    author_email='Ralbee1@iwu.edu',
    packages=setuptools.find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "five_card_draw": ["*.txt"],
        "five_card_draw.data": ["*.png"]
    },
    include_package_data=True,
    install_requires = requires,
    scripts = scripts,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires = '>=3.8',
    url = "https://github.com/ralbee1/5_card_draw"
)
