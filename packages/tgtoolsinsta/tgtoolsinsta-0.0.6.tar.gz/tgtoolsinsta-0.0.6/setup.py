from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.6'
DESCRIPTION = 'INSTAGRAM ID SCRAPER '
LONG_DESCRIPTION = 'A PYTHON LIBRARY THAT HELPS YOU TO SCRAPE INSTAGRAM USER-ID'

# Setting up
setup(
    name="tgtoolsinsta",
    version=VERSION,
    author="T G",
    author_email="mail2tgtools@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests',],
    keywords=['Instagram','userid'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)