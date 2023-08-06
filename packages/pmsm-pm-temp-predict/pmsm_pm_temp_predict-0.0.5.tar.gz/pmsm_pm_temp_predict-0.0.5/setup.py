from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Permanent magnet temperature prediction'
LONG_DESCRIPTION = 'This package provides an API to predict the temperature of the permanent magnet located on the rotor of the PMS motor based on the motor voltage, current, and temperature of the coolant and stator windings.'

# Setting up
setup(
        name="pmsm_pm_temp_predict", 
        version=VERSION,
        author="Oleksandr",
        author_email="<oleksandr.ohlashennyi.knm.2020@lpnu.ua>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas', 'sklearn', 'numpy', 'filesplit'],
        
        keywords=['python', 'pmsm', 'motor', 'temperatue', 'prediction'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ],
        include_package_data=True,
        package_data={'': ['data/*', 'data/split/*']},
)
