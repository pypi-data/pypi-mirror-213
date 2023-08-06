import setuptools
from distutils.core import setup

with open('README.md','r') as f:
    long_description = f.read()

setup(
    name='pyB12SPS',
    version= "0.1.1",
    author='Bridge12 Technologies, Inc',
    author_email='yhuang@bridge12.com',
    description='A Python Package for Interfacing with the Bridge12 Shim Power Supply',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://www.bridge12.com/',
    project_urls={
        #'Documentation':'http://pyb12shim.bridge12.com',
        },
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=['numpy','pyserial', 'PyQt5'],

    entry_points = dict(
        console_scripts = [
            "pyB12SPSGUI = pyB12SPS.pyB12SPSGUI:main_func"
        ]
    ),
    package_data={"pyB12SPS": ["pyB12SPSGUI.ui"]},
)
