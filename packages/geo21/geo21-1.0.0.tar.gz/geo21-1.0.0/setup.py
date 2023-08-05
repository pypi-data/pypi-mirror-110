import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="geo21",
    version="1.0.0",
    description="It perform all the geoprocessing task",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Nandan Pattanayak",
    author_email="mail2nandan18@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["geo21"],
    include_package_data=True,
    install_requires=["pandas","numpy","Shapely"]
)