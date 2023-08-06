from setuptools import setup
with open('README.md', 'r') as f:
    longdesc = f.read()
setup(
    name='blessable',
    version='1.0.2',
    author='www.mrfake.name',
    description='"Blessable" - a simple markup language for Blessings.',
    long_description=longdesc,
    long_description_content_type='text/markdown',
    homepage='https://github.com/fakerybakery/blessable',
    packages=['blessable'],
    install_requires=['blessed'],
)
