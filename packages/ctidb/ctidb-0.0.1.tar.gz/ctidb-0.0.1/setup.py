from setuptools import setup, find_packages

setup(
    name='ctidb',
    version='0.0.1',
    description='criminalip.ctidb reader',
    author='aispera',
    author_email='infra@aispera.com',
    url='https://github.com/aispera/ctidb',
    install_requires=['Crypto', 'mmap', 'ipaddress', 'struct'],
    packages=find_packages(exclude=[]),
    keywords=['aispera', 'ctidb', 'criminalip'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)