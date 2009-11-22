"""
This is a setup.py script generated by py2applet
It has been modified by the author to include more standard distutil info.

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['src/start.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

setup(
    name='PsyQ',
    version='0.8',
    description='Question Oriented Psychology Experiment Program',
    author='Bryan Head',
    author_email='bryan.head@gmail.com',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
