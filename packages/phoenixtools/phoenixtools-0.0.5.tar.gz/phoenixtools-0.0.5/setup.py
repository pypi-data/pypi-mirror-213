from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'Easy hacking tools'
LONG_DESCRIPTION = 'Easy hacking tools used for educational purposes'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="phoenixtools", 
        version=VERSION,
        author="Jack B.",
        author_email="<BurrJ22@outlook.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)