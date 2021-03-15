from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="transcriber-wrapper",
    description="A wrapper of well-known translators that transform text into its phonetic transcription",
    version="1.1.0",
    install_requires=[],
    include_package_data=True,
    packages=find_packages(),
    author="Willian Antunes",
    author_email="willian.lima.antunes@gmail.com",
    license="GPL3",
    keywords="linguistics ipa transcriber phonetics pronunciation dictionary",
    url="https://github.com/willianantunes/transcriber-wrapper",
    project_urls={
        "Bug Tracker": "https://github.com/willianantunes/transcriber-wrapper/issues",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: " "GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
