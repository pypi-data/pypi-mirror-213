from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="whist_score",
    version="0.1.13",
    author="Erwin Mintiens",
    author_email="erwin.mintiens@protonmail.com",
    license_files=("LICENSE",),
    description="whist_score is a scorekeeper for the whist card game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erwinmintiens/whist-score",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.json"]},
    install_requires=["click>=7.1.2", "colorama>=0.4.6"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        whist-score=main:main
    """,
)
