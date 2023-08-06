from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="canarytrap",
    version="1.0.1",
    description="A Python package to watermark text.",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Matthew Lee",
    author_email="matthewleemattner@gmail.com",
    url="https://github.com/MatthewLeeCode/CanaryTrap",
    packages=find_packages(),
    python_requires='>=3.9',
)
