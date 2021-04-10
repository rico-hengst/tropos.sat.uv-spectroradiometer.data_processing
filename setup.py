import setuptools

#with open("README.md", "r", encoding="utf-8") as fh:
    #long_description = fh.read()

setuptools.setup(
    name="troposzz", 
    version="1.1",
    author="Rico Hengst, Nicolas Bayer, Lionel Doppler",
    author_email="rico.hengst@tropos.de",
    description="The software package contains scripts to process UV radiation data, based on measurements with the spectroradiometer BTS2048. The Python software package is tailored to read the data in the manufacturer data format 'Solarscan'. The software package is able to export the data in the netcdf format and to generate plots of the measured and dervied variables.",
    package_dir = {'': 'src'}, # Our packages live under src but src is not a package itself
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'argparse',
    ],
    entry_points={ 
        'console_scripts': [ 
            'troposzz = src.troposzz.bts_process.__main__' 
        ] 
    },  
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL v3.0",
        "Operating System :: OS Independent",
    ],
)


