import os
from setuptools import setup, find_packages


# Read the contents of the requirements.txt file
def parse_requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
        return f.read().splitlines()

setup(
    name='blossom_http',
    version='0.0.2',
    packages=find_packages(),
    install_requires=parse_requirements(),
    exclude_package_data={'': ['*.env', '.env']},  # Extra safeguard to exclude .env files
    author='Bruce Wayne',
    description='HTTP package for Blossom',
)
