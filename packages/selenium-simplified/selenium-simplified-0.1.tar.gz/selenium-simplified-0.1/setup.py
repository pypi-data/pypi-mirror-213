import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium-simplified",
    version="0.1",
    author="rajnish kumar",
    author_email="raajrajnish@gmail.com",
    description="a better approach to do automation using simplified python on chrome browser",
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