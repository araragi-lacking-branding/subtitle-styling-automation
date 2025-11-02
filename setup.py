from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="subtitle-styling-automation",
    version="0.1.0",
    author="Your Name",
    description="A tool to extract and modify subtitle styling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pysrt>=1.1.2",
        "chardet>=5.0.0",
        "pysubs2>=1.6.0",
    ],
    entry_points={
        "console_scripts": [
            "subtitle-style=subtitle_styling.cli:main",
        ],
    },
)
