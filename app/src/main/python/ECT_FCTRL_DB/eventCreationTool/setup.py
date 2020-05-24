import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eventCreationTool",
    version="1.5",
    author="Günes Aydin, Joey Zgraggen, Nikodem Kernbach",
    author_email="nikodem.kernbach@unibas.ch",
    description="A simple tool for creating BACnet feeds and events",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cn-uofbasel/BACnet/tree/master/groups/04-logMerge/eventCreationTool",
    packages=setuptools.find_packages(),
    install_requires=[
          'cbor',
          'pynacl',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
