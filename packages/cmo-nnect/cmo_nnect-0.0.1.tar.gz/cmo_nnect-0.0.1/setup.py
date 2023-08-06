from setuptools import setup, find_packages
from pathlib import Path

# read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cmo_nnect",
    version="0.0.1",
    python_requires=">=3.9",
    description="Connector with a variety of API's with ease.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Thijs van der Velden, Koen Leijsten",
    author_email="service@cmotions.nl",
    url="https://dev.azure.com/Cmotions/Packages/_git/DriveScanner",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "base64",
        "zeep",
    ],
    extras_require={
        "dev": [
            "black",
            "jupyterlab",
            "pytest>=6.2.4",
            "python-dotenv",
            "ipykernel",
            "twine"
        ],
    }
)
