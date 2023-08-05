import os

from setuptools import setup, find_packages

__version__ = '0.0.dev1623945779'


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='aiorx',
    version=__version__,
    description='Minimal ReactiveX using AsyncIO',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    author='Éttore Leandro Tognoli',
    author_email='ettoreleandrotognoli@gmail.com',
    data_files=[
        'LICENSE',
    ],
    packages=find_packages(
        './src/main/python/',
    ),
    package_dir={'': 'src/main/python'},
    include_package_data=True,
    keywords=['RX', 'Async'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Framework :: AsyncIO',
    ],
    install_requires=[
    ],
)
