import io
import os
import re

from setuptools import find_packages
from setuptools import setup, Distribution
from version import get_git_version

def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

try:
    import multiprocessing
except ImportError:
    pass

setup(
    name="RoxiLib",
    url="https://github.com/wavingroup/allinclusive_API",
    license='MIT',

    author="Wavin T&I",
    author_email="support@wavin.com",

    description="Python API for Roxi lib",
    
    long_description=read("README.md"),
    long_description_content_type="text/markdown",

    packages=['RoxiLib'],
    package_data={'': ['*.dll', '*.h']}, #package DLL and Header files
    version=get_git_version(),

    #install_requires=['pymodbus>=3.1.0'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
