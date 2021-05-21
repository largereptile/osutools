from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='osu!tools',
    version='0.2.1',
    packages=['osutools'],
    url='https://github.com/largereptile/osutools',
    license='MIT',
    author='largereptile',
    author_email='harry@barold.dev',
    description='A python wrapper for working with the osu! API, databases and file formats',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
