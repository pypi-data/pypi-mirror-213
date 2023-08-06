

from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="afex-sso",
    version="0.0.56",
    description="For integrating sso",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="AFEX NIGERIA",
    author_email="it@africaexchange.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests >= 2.28.2", "django>=3.2"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.7",
)
