"""Setup for installing the package."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()



setuptools.setup(
    name="sc-editor",
    version="1.93",
    author="cintagramabp",
    description="A battle cats save file editor korean version",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fieryhenry/BCSFE-Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={'SC_Editor': ['*.properties',]},
    include_package_data=True,
    
    python_requires=">=3.9",
    install_requires=[
        "colored",
        "tk",
        "python-dateutil",
        "requests",
        "pyyaml",
    ],
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
        ],
    },
    flake8={"max-line-length": 160},
)
