import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="lodestone-python-sdk",
    version="1.0.6",
    author="bocai",
    author_email="peijianbo@tuyoogame.com",
    description="Auth to tuyoo's Lodestone",
    long_description=README,
    long_description_content_type="text/markdown",

    install_requires=['requests', 'urllib3<2.0'],
    packages=find_packages(),

    python_requires='>3.2',
)