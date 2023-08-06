# import setuptools
import setuptools
from distutils.core import setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("HanLabTools/version.py", "r") as f:
    # Define __version__ in separate file. That way online documentation can read it too
    exec(f.read())

setup(
    name="HanLabTools",
    version=__version__,
    description="Import tools for DNPLab specific to the Han Lab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Thorsten Maly",
    author_email="tmaly@bridge12.com",
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24",
    ],
    package_data={"HanLabTools": ["config/HanLab.cfg"]},
    packages=setuptools.find_packages(),
    url="https://github.com/Bridge12Technologies/HanLabTools",
    project_urls={
        "Tracker": "https://github.com/Bridge12Technologies/HanLabTools/issues"
    },
)
