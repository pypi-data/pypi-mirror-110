import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="num2name",
    version="0.0.1",
    author="ksumit",
    author_email="sumitkushwah1729@gmail.com",
    description="Convert any number into name ex. 44-> forty four",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sumit-kushwah/num2name",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
