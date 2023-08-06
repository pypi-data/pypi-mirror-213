from setuptools import setup, find_packages

with open("./Readme.md", "r") as rf : 
    long_description = rf.read()

setup(
    name = "conversion-units",
    version = "0.0.2",

    package_dir= {"":"conversion_units"},
    packages= find_packages(where="conversion_units"),

    description = "unified package contening collection of method to convert values from one unit to another. It can be a Distance, a Time, a Temperature, a Mass . . .etc",
    long_description= long_description,
    long_description_content_type = "text/markdown",

    author= "Brice KENGNI ZANGUIM",
    author_email="kenzabri2@yahoo.com",

    url = "https://github.com/Brice-KENGNI-ZANGUIM/conversion-units",
    license= "MIT",

    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        
    ],
    include_package_data=True,

    install_requires = [""],

    extra_requires = {
        "dev" : ["twine>=4.0" , "pytest>=7.1" ]
    } ,

    python_requires = ">=3.9"

)