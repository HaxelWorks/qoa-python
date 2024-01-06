from setuptools import setup

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
    cffi_modules=[
        'qoa/ffi_builder.py:ffibuilder',
    ],
)