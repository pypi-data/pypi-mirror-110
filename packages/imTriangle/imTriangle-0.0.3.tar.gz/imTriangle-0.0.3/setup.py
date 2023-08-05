from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


setup(
    name='imTriangle',
    version='0.0.3',
    author="mamdasn s",
    author_email="<mamdassn@gmail.com>",
    url="https://github.com/Mamdasn/imTriangle",
    description='This snippet of code attempts to put triangle pixelation effect on images.',
    long_description=long_description,
    long_description_content_type = "text/markdown",
    include_package_data=True,
    package_dir={'': 'src'},
    py_modules=["imTriangle"],
    install_requires=[
        "numpy", 
        "numba",
        "imPixelate",
        ],
    keywords=['python', 'traingle effect', 'triangle pixelation effect'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/imTriangle'],
)
