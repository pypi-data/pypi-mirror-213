from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="PyHarshit",
    version="0.0.8",
    author="Harshit Shrivastav",
    author_email="itsharshit@yandex.com",
    description="Utlity file for my codes",
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
