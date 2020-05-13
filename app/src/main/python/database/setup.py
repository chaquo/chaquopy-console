import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logStore-pkg-vGsteiger-moritzwuerth", # Replace with your own username
    version="0.0.3",
    author="Viktor Gsteiger",
    author_email="v.gsteiger@unibas.ch",
    description="A package for access to the sqLite database for the BACnet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cn-uofbasel/BACnet/tree/master/groups/07-logStore/src",
    packages=setuptools.find_packages(),
    install_requires=[
          'sqlalchemy',
          'cbor',
          'pynacl',
          'testfixtures',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
