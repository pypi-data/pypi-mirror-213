# -*- coding: utf-8 -*-

from setuptools import setup, dist
from setuptools.command.install import install
import os

with open("../newtag/newtag", "r") as f:
    newtag = f.read().strip()

# Initialiser la variable VERSION
VERSION = newtag.replace("v", "")

class BinaryDistribution(dist.Distribution):
    def has_ext_modules(foo):
        return True

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        if not os.path.isdir(self.install_scripts):
            os.makedirs(self.install_scripts)
        package_dir = os.path.dirname(os.path.abspath(__file__))
        binary_dir = os.path.join(package_dir, "bin");
        binary = "mainlibprotein"
        source = os.path.join(binary_dir, binary)
        target = os.path.join(self.install_scripts, binary)
        if os.path.isfile(target):
            os.remove(target)
        self.copy_file(source, target)

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    README = f.read()

setup(
    name='libprotein',
    package_data={
        "libprotein": ["_libprotein.so", "_libprotein.dylib", "_libprotein.dll"],
        '': ['banner512x125.png']
    },
    version=VERSION,
    description="This module allows to parse existing data for qualifying a protein sequence in order to assess the sequence knowledge available in various databases.",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/TeletcheaLab/libprotein',
    author='Matthieu E :: Hamady BA :: Sébastien Téletchéa',
    author_email='stephane.teletchea@univ-nantes.fr',
    include_package_data=True,
    distclass=BinaryDistribution,
    cmdclass={'install': PostInstallCommand},
    download_url="https://github.com/TeletcheaLab/libprotein/archive/refs/tags/v"+VERSION+".tar.gz",
    packages=['libprotein'],
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C++',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='protein post-translational modification, protein domain',
    project_urls={
        'GitLab': 'https://gitlab.univ-nantes.fr/teletchea-s/libprotein',
        'Github': 'https://github.com/TeletcheaLab/libprotein'
    },
)