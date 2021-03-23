import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tropos.solarscan_or0_import", # Replace with your own username
    version="0.0.1",
    author="Rico Hengst, Nicolas Bayer, Lionel Doppler",
    author_email="rico.hengst@tropos.de",
    description="The software package contains scripts to process UV radiation data, based on measurements with the spectroradiometer BTS2048. The Python software package is tailored to read the data in the manufacturer data format 'Solarscan'. The software package is able to export the data in the netcdf format and to generate plots of the measured and dervied variables.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rico-hengst/tropos.solarscan_or0_import",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL v3.0",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.6',
    #entry_points='''
    #    [console_scripts]
    #    yourscript=yourscript:cli
    #''',
    entry_points={ 
        'console_scripts': [ 
            'tropos.solarscan_or0_import = src.BTS_main_process:main' 
        ] 
    }, 
)
