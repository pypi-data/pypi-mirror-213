import os
from setuptools import setup
import setuptools



def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "image_processing-package-dio-challenge",
    version="0.0.1",
    author="Matheus Lima Moreira",
    author_email="math.lima.m@gmail.com",
    description=('''A image processing tool that generates normal maps'''),
    packages=setuptools.find_packages(),
    install_requires=["requirements.txt"]

)