from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="turborest",
    version="0.1.3",
    author="ByteSentinel.io",
    author_email="dev@bytesentinel.io",
    description="A library for monitoring files and directories for changes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bytesentinel-io/turborest",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)