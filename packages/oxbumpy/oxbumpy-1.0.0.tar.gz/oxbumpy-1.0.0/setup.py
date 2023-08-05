from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "1.0.0"
DESCRIPTION = "A tool for extracting, analysing, simulating, and predicting Oxford bumps racing"

setup(
    name="oxbumpy",
    version=VERSION,
    author="Henry Ginn",
    author_email="<henryginn137@gmail.com>",
    description=DESCRIPTION,
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    install_requires=[],
    keywords=["python", "oxford", "bumps", "rowing", "fantasy", "simulation"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
