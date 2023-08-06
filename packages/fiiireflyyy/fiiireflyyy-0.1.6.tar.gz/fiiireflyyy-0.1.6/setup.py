from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.6'
DESCRIPTION = 'A python package covering miscellaneous uses, from system management to machine learning and image or' \
              ' data processing. Developed for personal uses.'

# Setting up
setup(
    name="fiiireflyyy",
    version=VERSION,
    author="fiiireflyyy (Willy Lutz)",
    author_email="<lutz0willy@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['scikit-learn', 'umap-learn', 'opencv-python', 'matplotlib', 'tensorflow', 'pandas',
                      'numpy', 'imaris-ims-file-reader', 'zarr', 'seaborn'],
    keywords=['python', 'machine learning', 'deep learning', 'data analysis', 'system management', 'data processing'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
