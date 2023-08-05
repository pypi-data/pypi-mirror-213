from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="yhc_pypi",
    version="1.0.0",
    author="windsky",
    author_email="luna_hc@pku.edu.cn",
    description="test setup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/your-package",
    packages=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
