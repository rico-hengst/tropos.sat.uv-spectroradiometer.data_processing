import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TROPOS-SAT-BTS", # Replace with your own username
    version="0.0.1",
    author="Rico Hengst, Nicolas Bayer, Lionel Doppler",
    author_email="rico.hengst@tropos.de",
    description="The software package contains scripts to process UV radiation data, based on measurements with the spectroradiometer BTS2048. The Python software package is tailored to read the data in the manufacturer data format 'Solarscan'. The software package is able to export the data in the netcdf format and to generate plots of the measured and dervied variables.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitea.tropos.de/hengst/tropos.sat.uv-spectroradiometer.data_processing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL v2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
