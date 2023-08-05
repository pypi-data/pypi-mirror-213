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
3. py twine upload dist/*

'''
import os
from pathlib import Path
import setuptools

requires = [
    'tkinter',
    'pathlib',
]

scripts = [
    str(Path('5_card_draw','video_poker.py'))
]

#Package setuptools pypi install for local developer installs
setuptools.setup(
    name = '5_card_draw',
    version = os.getenv('PACKAGE_VERSION', '1.0.0'),
    description = 'Video Poker application for 5 Card Draw Poker',
    author = 'Richard Albee',
    author_email='Ralbee1@iwu.edu',
    packages = setuptools.find_packages(),
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
    url = "https://github.com/ralbee1/VideoPoker-5CardRedraw"
)
