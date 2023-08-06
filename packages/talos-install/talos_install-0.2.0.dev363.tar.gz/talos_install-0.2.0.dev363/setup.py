import setuptools
from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    setup_requires=['pbr>=2.0.0'],
    pbr=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
