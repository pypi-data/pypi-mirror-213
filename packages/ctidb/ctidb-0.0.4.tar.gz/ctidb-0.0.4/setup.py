import os
import re
from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)

with open(os.path.join(ROOT, "README.rst"), "rb") as fd:
    README = fd.read().decode("utf8")

with open(os.path.join(ROOT, "ctidb", "__init__.py"), "rb") as fd:
    ctidb_text = fd.read().decode("utf8")
    LICENSE = (
        re.compile(r".*__license__ = \"(.*?)\"", re.S).match(ctidb_text).group(1)
    )
    VERSION = (
        re.compile(r".*__version__ = \"(.*?)\"", re.S).match(ctidb_text).group(1)
    )

# def find_packages(location):
#     packages = []
#     for pkg in ["ctidb"]:
#         for _dir, subdirectories, files in os.walk(os.path.join(location, pkg)):
#             if "__init__.py" in files:
#                 tokens = _dir.split(os.sep)[len(location.split(os.sep)) :]
#                 packages.append(".".join(tokens))
#     return packages

setup(
    name='ctidb',
    version=VERSION,
    description='criminalip.ctidb reader',
    long_description=README,
    author='aispera',
    author_email='infra@aispera.com',
    license=LICENSE,
    url='https://github.com/aispera/ctidb',
    install_requires=[],
    packages=find_packages(exclude=[]),
    # packages=find_packages("."),
    keywords=['aispera', 'ctidb', 'criminalip'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
