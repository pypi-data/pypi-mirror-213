from setuptools import setup, find_packages

setup(
    name='airohit-fasterrcnn',
    version='1.0.0',
    description='a library for fasterrcnn detect',
    author='airohit.com',
    packages=['network_files_fasterrcnn', 'backbone_fasterrcnn'],
    install_requires=[
        'numpy'
    ],
)