import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UzbekLemmatizer",
    version="1.0.4",
    author="Maksud Sharipov, Ollabergan Yuldashov",
    author_email="maqsbek72@gmail.com, ollaberganyuldashov@gmail.com",
    description="Uzbek Lemmatizer for Python. A Python package to lemmatize Uzbek words.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaksudSharipov/UzbekLemmatizer",
    project_urls={
        "Bug Tracker": "https://github.com/MaksudSharipov/UzbekLemmatizer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['python', 'UzbekLemmatizer', 'uzbek words', 'Lemmatizer'],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"": ["*.xml"]},
    #package_data={"": ["cyr_exwords.csv", "lat_exwords.csv"],},
)