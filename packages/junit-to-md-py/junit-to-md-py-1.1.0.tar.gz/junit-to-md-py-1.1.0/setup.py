from setuptools import setup

setup(
    name="junit-to-md-py",
    version="1.1.0",
    author="srydz_catalogicsoftware",
    author_email="srydz@catalogicsoftware.com",
    description="Python script which converts junit xml file/text into the markdown representation",
    long_description=open("README.rst", encoding="utf-8").read(),
    url="https://github.com/catalogicsoftware/dpx-utils-junit-to-md",
    license="MIT",
    install_requires=[
        "lxml",
    ],
    entry_points={
        "console_scripts": [
            "junit-to-md-py = script.junit_to_md:main",
        ]
    },
)
