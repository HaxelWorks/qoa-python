from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop

import subprocess
import sys

class PreInstallCommand(install):
    """Pre-installation for installation mode."""
    def run(self):
        install.run(self)
        subprocess.check_call([sys.executable, "ffi_builder.py"])

class PreDevelopCommand(develop):
    """Pre-installation for development mode."""
    def run(self):
        develop.run(self)
        subprocess.check_call([sys.executable, "ffi_builder.py"])
        
setup(
    name='qoa',
    version='0.1.0',
    packages=['qoa'],
    setup_requires=[
        'cffi>=1.16.0',
    ],
    install_requires=[
        'cffi>=1.16.0',
        'numpy>=1.26.0',
    ],
    cmdclass={
        'install': PreInstallCommand,
        'develop': PreDevelopCommand,
    }
)