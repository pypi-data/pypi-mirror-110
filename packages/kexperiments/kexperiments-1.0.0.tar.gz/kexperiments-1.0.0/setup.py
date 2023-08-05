import setuptools


long_description = """A Python package for utilizing experimentation methods in tests, 
                        sample size calculations, inference, and sampling."""

setuptools.setup(
    name="kexperiments",
    version="1.0.0",
    author="Amar Mohabir",
    author_email="amar@koho.ca",
    description="A Python package for experimentation at KOHO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kohofinancial/kexperiments",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "kexperiments"},
    packages=setuptools.find_packages(where="kexperiments"),
    python_requires=">=3.4"
)
