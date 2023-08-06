# setup.py
from setuptools import setup, find_packages

setup(
    name="devcheck",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'devcheck = devcheck.main:main'
        ]
    },
    python_requires='>=3.6',
)
