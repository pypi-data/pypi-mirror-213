from setuptools import setup
with open('README.md', 'r') as f:
    longdesc = f.read()
setup(
    name='blessable',
    version='1.0.3',
    author='www.mrfake.name',
    description='"Blessable" - a simple markup language for Blessings.',
    long_description=longdesc,
    long_description_content_type='text/markdown',
    url='https://github.com/fakerybakery/blessable',
    packages=['blessable'],
    install_requires=['blessed'],
    project_urls={
        "Bug Reports": "https://github.com/fakerybakery/blessable/issues",
        "Source": "https://github.com/fakerybakery/blessable",
    },
)
