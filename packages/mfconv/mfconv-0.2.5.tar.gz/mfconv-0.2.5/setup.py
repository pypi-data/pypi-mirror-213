import io
import os
import re
from setuptools import setup, find_packages

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# # Find version info from module (without importing the module):
# with open("mfconv/__init__.py", "r") as fileObj:
#     version = re.search(
#         r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
#     ).group(1)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name="mfconv",
    version='0.2.5',
    url="https://github.com/gmezacuadra/mfconv",
    author="Gustavo Meza-Cuadra",
    author_email="gmeza-cuadra@flosolutions.com",
    description=("""a python package to plot modflow convergence while you run a model"""),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    # packages=find_packages(where="mfconv"),
    # package_dir={"": "mfconv"},
    install_requires=[],
    keywords="",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
