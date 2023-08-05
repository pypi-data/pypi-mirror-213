from setuptools import setup, find_packages 

with open("README.md", "r") as fh:
    long_description = fh.read()
 
    setup(
        
    name="SimpleShape",
    version="1.5",
    author="Tilen Žel",
    author_email="tilen.zel@gmail.com",
 
    #Small Description about module
    description="""A simple package for creating geometric objects""",
 
    # Specifying that we are using markdown file for description
    long_description=long_description,
    long_description_content_type="text/markdown",
 
    # Any link to reach this module, ***if*** you have any webpage or github profile
    # url="https://github.com/username/",
    packages=find_packages(),
 
 
    license="MIT",
 
    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)