from setuptools import setup

with open("README.md", "r", encoding="utf-8") as ld:
    long_description = ld.read()

setup(
    name="OrbusMaker",
    version="1.1.3",
    author="Wilovy09",
    author_email="orbuscompany@gmail.com",
    description="An app skeleton creator, using CLI interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Orbus-Company/OrbusMaker",
    python_requires=">3.10",
    project_url={
        "Bug Tracker": "https://github.com/Orbus-Company/OrbusMaker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["orbus"],
    entry_points={"console_scripts": ["create-flet-app = orbusmaker.__main__:FLET"]},
)