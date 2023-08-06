from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('version', 'r', encoding='utf-8') as f:
    version = f.read()



setup(
    name="ANBUtils",
    version=version,
    packages=find_packages(),
    author="redbson",
    author_email="redbson@gmail.com",
    url="https://github.com/redbson/ANBUtils",
    description = "ANBUilts is a versatile Python package that offers a comprehensive set of utility functions and tools for data analysis, database operations, and messaging integration.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    install_requires=[
        "matplotlib>=3.0.0",
        "numpy>=1.0.0",
        "pandas>=1.0.0",
        "pymongo>=4.0.2",
        "requests>=2.0.0",
        "matplotlib>=3.0.0",

    ]
)
