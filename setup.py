from setuptools import setup

#with open("README.md", "r", encoding="utf-8") as fh:
    #long_description = fh.read()

setup(
    name            = "tropos_uv", 
    version         = "1.1",
    author          = "Rico Hengst, Nicolas Bayer, Lionel Doppler",
    author_email    = "rico.hengst@tropos.de",
    description     = "The software package contains scripts to process UV radiation data, based on measurements with the spectroradiometer BTS2048. The Python software package is tailored to read the data in the manufacturer data format 'Solarscan'. The software package is able to export the data in the netcdf format and to generate plots of the measured and dervied variables.",
    packages        = [ 'tropos_uv' ],
    package_dir     = {'tropos_uv': 'src'}, # Our packages live under src but src is not a package itself
    package_data    = { # include config files
        # If any package contains * files, include them:
        "": ["config/templates/*"],
    },
    python_requires = '>=3.7',
    install_requires=[
        'argparse',
        'attrdict',
        'jstyleson',
    ],
    entry_points    = { 
        'console_scripts': [ 
            'troposuv = tropos_uv.bts_process:run' 
        ] 
    },  
     classifiers    = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL v3.0",
        "Operating System :: OS Independent",
    ],
)


