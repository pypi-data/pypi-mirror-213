from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.1'
DESCRIPTION = 'pyfire is a package that simplifies querying with Pyrebase,\
    making interactions with Firebase databases effortless.'
PACKAGE_NAME = 'pyfiredb'
AUTHOR = 'Camilo Andrés Rodríguez'
EMAIL = 'andres.roh@gmail.com'
GITHUB_URL = 'https://github.com/andresroh/pyfire'

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    license='MIT',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB_URL,
    keywords=['python', 'alegra', 'alegra.com'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
