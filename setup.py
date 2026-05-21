from setuptools import setup, find_packages


__version__ = "0.0.6"


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="hackatari",
    version=__version__,
    author="Quentin Delfosse, Jannis Blüml",
    author_email="quentin.delfosse@cs.tu-darmstadt.de",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/k4ntz/HAckAtari",
    description="Extended Atari Learning Environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "ocatari", "gymnasium[atari, accept-rom-license]",
    ],
)
