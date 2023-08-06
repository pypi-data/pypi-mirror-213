import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SSML-parser",
    version="1.0.0",
    author="Nishant Sharma",
    description="An SSML parsing library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=(
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ),
    )