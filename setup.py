from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="text-autocompletion",
    version="0.1.0",
    description="A toy implementation of a text autocompletion module",
    author="Wenhao Gu",
    install_requires=required,
    python_requires=">=3.6",
) 