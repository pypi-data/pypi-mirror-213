import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="hasiihelper",
    version="0.2.1",
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Humberto`s Helper Classes',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/hasiihelper",
    package_data={
        'hasiihelper':  ['py.typed'],
    },

    packages=[
        'hasiihelper',
    ],
    install_requires=['Deprecated~=1.2.14'],
)
