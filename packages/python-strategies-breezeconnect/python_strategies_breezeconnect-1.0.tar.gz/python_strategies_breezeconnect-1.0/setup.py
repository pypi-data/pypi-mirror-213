import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_strategies_breezeconnect",
    version="1.0",
    author="UAT python strategy Breeze Connect",
    author_email="test@mail.com",
    description="breeze connect strategies in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['uat-breeze-connect','nest_asyncio'],
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
