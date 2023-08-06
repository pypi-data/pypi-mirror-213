"""
Build instructions for setuptools. Install manually with
`python setup.py install`
"""

from setuptools import setup


def readme():
    """
    :return: Content of README.md
    """
    with open("README.md") as file:
        return file.read()


setup(
    name="CheckMyTex",
    version="0.10.4",
    description="A simple tool for checking complex LaTeX documents, e.g., dissertations.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="LaTeX",
    url="https://github.com/d-krupke/checkmytex",
    author="Dominik Krupke",
    author_email="krupke@ibr.cs.tu-bs.de",
    license="MIT",
    packages=[
        "checkmytex",
        "checkmytex.finding",
        "checkmytex.latex_document",
        "checkmytex.utils",
        "checkmytex.cli",
        "checkmytex.filtering",
    ],
    install_requires=[
        "pyspellchecker==0.7.2",
        "flachtex>=0.3.11",
        "yalafi>=1.3.0",
        "proselint>=0.13.0",
        "rich>=12.5.1",
    ],
    entry_points={
        "console_scripts": ["checkmytex=checkmytex.__main__:main"],
    },
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
)
