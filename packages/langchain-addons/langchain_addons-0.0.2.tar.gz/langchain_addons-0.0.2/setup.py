from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="langchain_addons",
    version="0.0.2",
    license="MIT License",
    author="Eduardo M. de Morais",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="emdemor415@gmail.com",
    keywords="preprocessing",
    description=u"...",
    packages=["langchain_addons"],
    install_requires=["langchain"],
)