import setuptools

with open("README.md", "r") as pkg:
    long_description = pkg.read()

setuptools.setup(
    name="charred",
    version="0.1.11",
    author="Endormi",
    author_email="contactendormi@gmail.com",
    description="Very simple char functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/endormi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
