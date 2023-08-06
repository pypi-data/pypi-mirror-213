import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium-simplified",
    version="0.6",
    author="rajnish kumar",
    author_email="raajrajnish@gmail.com",
    description="A free, open-source web automation library for the Chrome browser using Selenium Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raajrajnish/SeleniumSimplified.git",
    packages=setuptools.find_packages(),
    # packages=['simplified'],
    install_requires=['selenium'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)