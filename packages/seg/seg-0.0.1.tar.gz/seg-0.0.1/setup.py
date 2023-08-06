# from distutils.core import setup
from setuptools import setup

setup(
    # Application name:
    name="seg",

    # Version number:
    version="0.0.1",

    # Application author details:
    author="Yinsheng Zhang (Ph.D.)",
    author_email="oo@zju.edu.cn",

    # Packages
    packages=["seg", "seg.data"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/seg/",

    #
    license="LICENSE.txt",
    description="Image segmentation tools specially for blood vessels.",

    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf-8').read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
        "scikit-learn",
        "matplotlib",
        "numpy",
        "pandas",
        "statsmodels",
        "h5py",
        "opencv-python",
        "torch",
    ],

    package_data={
        "": ["*.txt", "*.csv", "*.png", "*.jpg", "*.json"],
    }
)

# To Build and Publish (for developer only),
# Run: python -m build
# Run: python -m pyc_wheel qsi_tk.whl  [optional]
# or
# Run: python setup.py sdist bdist_wheel; twine upload dist/*
