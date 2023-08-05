import sys
from setuptools import setup

if sys.version_info < (3, 6):
    sys.exit('Sorry, zgtf requires Python >= 3.6')

requirements = [
    "htseq>=0.11"
]

setup(
    name='zgtf',
    version='0.1.2',
    description="gtf conversion utility.",
    author="Foivos Gypas",
    author_email='foivos.gypas@unibas.ch',
    url='',
    packages=['zgtf'],
    package_dir={'zgtf': 'zgtf'},
    include_package_data=True,
    scripts=['scripts/gtf2bed12'],
    install_requires=requirements,
    keywords='zgtf',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
