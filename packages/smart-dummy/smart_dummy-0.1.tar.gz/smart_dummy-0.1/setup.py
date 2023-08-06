from setuptools import setup, find_packages


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    with open(filename) as f:
        lineiter = (line.strip() for line in f)
        return [line for line in lineiter if line and not line.startswith("#")]


reqs = parse_requirements('requirements.txt')

setup(
    name="smart_dummy",
    version="0.1",
    packages=find_packages(),
    install_requires=reqs,
    author="Muriel Grobler, Emma Zhang",
    author_email="muriel.grobler@gmail.com, emma.lzhang@gmail.com",
    description="A smart and easy replacement to pandas.get_dummies() ",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/emmalzhang/smart_dummy",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
