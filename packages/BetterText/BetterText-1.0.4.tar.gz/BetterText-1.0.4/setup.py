from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.4'
DESCRIPTION = 'BetterText'
LONG_DESCRIPTION = 'BetterText'

# Setting up
setup(
    name="BetterText",
    version=VERSION,
    author="Hide Le Ouf",
    author_email="<lancbiche@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires='',
    keywords=['color', 'custom color', 'text color', 'text style', 'better text', 'rgb color'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
