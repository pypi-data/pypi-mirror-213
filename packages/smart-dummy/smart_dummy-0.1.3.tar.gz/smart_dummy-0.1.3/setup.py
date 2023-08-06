from setuptools import setup, find_packages


setup(
    name="smart_dummy",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24',
        'pandas>=1.0',
        'pydantic>=1.10',
        'scikit-learn>=1.0',
        'spacy>=3.5'
    ],
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
