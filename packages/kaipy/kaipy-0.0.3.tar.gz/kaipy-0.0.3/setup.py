import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kaipy",
    version="0.0.3",
    author="Center for Geospace Storms",
    author_email="eric.winter@jhuapl.edu",
    description="Postprocessing code for models in the kaiju software system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/aplkaiju/kaiju/src/master/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "ai.cdas==1.2.3",
        "alive_progress==3.1.4",
        "astropy==4.3.1",
        "cdasws==1.7.40",
        "cdflib==0.4.4",
        "configparser==5.2.0",
        "dataclasses_json==0.5.7",
        "h5py==3.7.0",
        "matplotlib==3.5.2",
        "netCDF4==1.6.0",
        "numpy==1.21.6",
        "progressbar==2.5",
        "pyhdf==0.10.5",
        "pytest==7.1.2",
        "scipy==1.7.3",
        "spacepy==0.3.0",
        "sunpy==3.1.8",
        "xarray==0.20.2"
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
