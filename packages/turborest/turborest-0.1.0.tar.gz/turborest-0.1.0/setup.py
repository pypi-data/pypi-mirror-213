import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turborest",
    version="0.1.0",
    author="ByteSentinel.io",
    author_email="dev@bytesentinel.io",
    description="A simple REST client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bytesentinel-io/turborest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
