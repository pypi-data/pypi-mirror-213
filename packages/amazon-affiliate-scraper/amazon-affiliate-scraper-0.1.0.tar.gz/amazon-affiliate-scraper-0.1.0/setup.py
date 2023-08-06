from setuptools import setup, find_packages

with open("README.md", "r") as file:
    readme_content = file.read()

setup(
    name="amazon-affiliate-scraper",
    version="0.1.0",
    license="MIT License",
    author="Marcuth",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    author_email="marcuth2006@gmail.com",
    keywords="amazon affiliate scraper",
    description="A simple library to help a developer who is affiliated with Amazon to automate the process.",
    packages=["amazon_affiliate"] + [ "amazon_affiliate/" + x for x in find_packages("amazon_affiliate") ]
)