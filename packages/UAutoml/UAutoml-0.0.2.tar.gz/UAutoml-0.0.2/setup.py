from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='UAutoml',
    version='0.0.2',
    description='Automated Machine Learning Framework for Data Analysisr',
    author= 'Ujjwal Reddy K S',
    url = 'https://github.com/ujjwalredd/Automated-Machine-Learning-Framework-for-Data-Analysis',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['ML', 'Auto Data Analysis', 'models'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['UAutoml'],
    package_dir={'':'src'},
    install_requires = [
        'numpy',
        'scikit-learn'
    ]
)
