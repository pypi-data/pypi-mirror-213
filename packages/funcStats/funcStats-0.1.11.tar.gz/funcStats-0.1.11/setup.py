import os.path

from setuptools import setup, find_packages
from pathlib import Path
from config import LONG_DESCRIPTION
this_directory = Path(__file__).parent

VERSION = '0.1.11'
DESCRIPTION = 'A module that helps to evaluate functions when some tests are needed'

setup(
    name="funcStats",
    version=VERSION,
    author="Elemental (Tom Neto)",
    author_email="<info@elemental.run>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['datetime'],
    keywords=['python', 'functions', 'cronometer', 'crono', 'meter', 'evaluate functions'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
