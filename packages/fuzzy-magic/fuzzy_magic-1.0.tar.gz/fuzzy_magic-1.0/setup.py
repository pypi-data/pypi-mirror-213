import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "fuzzy_magic",
    version = "1.0",
    author = "Pedro López",
    author_email = "p.lopez@exus.ai",
    url = "https://github.com/EXUS-AI-Labs/ailabs-fuzzylogic",
    description = "A Fuzzy Logic library to create Mamdani Fuzzy Systems the easiest way possible",
    long_description = long_description,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)