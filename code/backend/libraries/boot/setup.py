import os
from setuptools import setup, find_packages


# Read the contents of the requirements.txt file
def parse_requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
        return f.read().splitlines()

setup(
    name='blossom_boot',
    version='0.0.1',
    packages=find_packages(),
    install_requires=parse_requirements(),
    author='Bruce Wayne',
    description='Boot package for all backend microservices',
)
