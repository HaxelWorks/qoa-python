from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="qoa",
    version="0.1.0",
    packages=["qoa"],
    description="A library for reading and writing QOA files",
    long_description=long_description,
    url="https://github.com/HaxelWorks/qoa-python",
    author="Axel Roijers",
    author_email="haxelworks@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Topic :: File Formats",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: System :: Archiving :: Compression",
        "License :: OSI Approved :: MIT License",
    ],
    setup_requires=[
        "cffi>=1.16.0",
    ],
    install_requires=[
        "cffi>=1.16.0",
        "numpy>=1.26.0",
    ],
    cffi_modules=[
        "qoa/ffi_builder.py:ffibuilder",
    ],
)
