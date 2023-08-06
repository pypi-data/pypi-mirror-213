from setuptools import setup, find_packages

setup(
    name="langtests",
    version="0.1",
    description="An evaluation library for NLP models",
    author="Openlayer",
    author_email="engineers@openlayer.com",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'rouge-score'
    ],
)