from setuptools import setup

setup(
    name='osu!tools',
    version='0.1.1',
    packages=['osutools'],
    url='https://github.com/largereptile/osutools',
    license='MIT',
    author='largereptile',
    author_email='harry@barold.dev',
    description='A python wrapper for working with the osu! API, databases and file formats',
    install_requires=['requests>=2.25.1', 'pyttanko>=2.1.0']
)
