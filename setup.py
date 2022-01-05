import setuptools

setuptools.setup(
    name="hyperborea",
    version="0.1.0",
    author="Jeremy Deram",
    author_email="jderam@gmail.com",
    description="Character Generator plus other tools for the Hyperborea RPG",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/jderam/hyperborea-tools",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
