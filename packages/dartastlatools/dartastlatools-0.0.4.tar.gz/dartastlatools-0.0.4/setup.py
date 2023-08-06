from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Tools for DART and ASTLA project'
LONG_DESCRIPTION = 'Several scripts about preprocessing and postprocessing (child) speech ASR input and output.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="dartastlatools", 
        version=VERSION,
        author="Wieke Harmsen",
        author_email="<wiekeharmsen@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas', 'numpy', 'glob2==0.7', 're', 'praat-textgrids==1.0.2'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        keywords=['python', 'child speech'],
)