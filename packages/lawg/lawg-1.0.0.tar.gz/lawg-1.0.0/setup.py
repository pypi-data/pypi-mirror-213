from setuptools import setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="lawg",
    version="1.0.0",
    url="https://github.com/lawgdev/lawg.py",
    author="hexiro",
    description="🐍 lawg's python integration",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=[],
    install_requires=[],
    zip_safe=True,
)
