from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Permanent magnet temperature prediction'

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "pmsm_pm_temp_predict/README.md").read_text()

# Setting up
setup(
        name="pmsm_pm_temp_predict", 
        version=VERSION,
        author="Oleksandr",
        author_email="<oleksandr.ohlashennyi.knm.2020@lpnu.ua>",
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type='text/markdown',
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
