import os
from setuptools import setup, find_packages

def parse_reqs(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path) as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="myExceptions",
    version="0.0.4",
    packages=find_packages(),
    exclude_package_data={'': ['*.env', '.env']},
    # No default dependencies: you _must_ pick dev _or_ docker
    install_requires=[],
    extras_require={
        # pip install .[docker] → will pull in exactly these
        'docker': parse_reqs('requirements/docker-requirements.txt'),
        # pip install .[dev]    → will pull in exactly these
        'dev':    parse_reqs('requirements/requirements.txt'),
    },
    author="Bruce Wayne",
    description="Exceptions package for Zartex",
)