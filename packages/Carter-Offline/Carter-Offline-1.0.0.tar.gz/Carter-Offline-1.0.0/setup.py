from setuptools import setup, find_packages

setup(
    name='Carter-Offline',
    version='1.0.0',
    description='A package for interacting with Carter API and saving its responses to an intent classifier, to host a Carter agent locally.',
    author='Sanware Technologies - https://github.com/Sanware',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any dependencies required by your package
        'torch',
        'pyttsx3'
        'nltk'
    ],
)
