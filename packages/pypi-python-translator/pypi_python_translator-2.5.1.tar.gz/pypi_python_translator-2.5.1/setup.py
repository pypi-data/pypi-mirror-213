import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypi_python_translator",
    version="2.5.1",
    author="SForces",
    author_email="osmntn08@gmail.com",
    description="A Python package for translation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SForces/pypi_python_translator",
    packages=["translator"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
