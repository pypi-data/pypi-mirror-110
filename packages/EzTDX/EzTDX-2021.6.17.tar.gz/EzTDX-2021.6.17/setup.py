import re
from setuptools import setup, find_packages

# read version from module
with open('src/eztdx/__init__.py', 'r') as fo:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fo.read(), re.MULTILINE).group(1)

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='EzTDX',
    version=version,
    author='Chris Garrett',
    author_email='cmgarOK@gmail.com',
    description='A Python interface to the TeamDynamix REST APIs',
    license='GPLv3+',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cgarrett/eztdx',
    project_urls={
        'Bug Tracker': 'https://github.com/cgarrett/eztdx/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=['requests'],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
)