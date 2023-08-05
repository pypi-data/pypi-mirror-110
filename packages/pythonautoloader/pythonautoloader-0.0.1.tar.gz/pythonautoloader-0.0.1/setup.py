from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A simple auto python setup from command line'
LONG_DESCRIPTION = 'A simple auto python setup from command line, when you run the command it will make a full dirrectory and example code'

setup(
    name="pythonautoloader",
    version=VERSION,
    author="Landen Fisher",
    author_email="landen6002@hotmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
