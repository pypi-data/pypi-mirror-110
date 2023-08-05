import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="ai_object_detection",
    version="1.1.7",
    url="https://github.com/nhanvpt102/AI-Object-Detection",
    license='MIT',

    author="Nhan Vo",
    author_email="nhanvpt102@gmail.com",

    description="AI Object Detection",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",

    packages=find_packages(exclude=('tests',)), # List of all python modules to be installed
    python_requires='>=3.6',                # Minimum version requirement of the package
    #py_modules=["ai_object_detection"],             # Name of the python package
    #package_dir={'':'ai_object_detection/src'},     # Directory of the source code of the package

    keywords = ['AI-Object-Detection'],   # Keywords that define your package best

    install_requires=[
      'selenium',
      'openpyxl',
      'argparse',
      'opencv-python',
      'scipy',
      'pillow',
      'pandas',
      'colorlog',
      'olefile',
      'pdf2image',
      'pywin32',
      'pypiwin32',
      'importlib-resources'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
