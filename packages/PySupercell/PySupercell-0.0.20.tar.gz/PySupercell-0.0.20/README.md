# PySupercell
A Python library for crystal structure operations

## Code introduction

This is a python package for creating and manipulating crystal structures

Copyright Shunhong Zhang 2023

zhangshunhong.pku@gmail.com


## Code citation

If you usage of this code lead to some publications, we request that you kindly cite it like

Shunhong Zhang, PySupercell: a python library for crystal structure operations (2023)


## Code distributions

* arguments: some arguments for command line
* QE_ibrav_lib: some defination of bravais lattice following Quantum ESPRESSO
* pysupercell: the core lib, with the class cryst_struct


## Installation
* Fast installation via pypi
pip install pysupercell


* Install manually from tarball 
1. Download the zip or tarball (tar.gz) of the package
2. unzip the package
3. Run one of the two following command
   python setup.py install --home=.
   python setup.py install --user

* To check whether you have successfully install the package, go to the python interactive shell
 
import pysupercell

  If everything runs smoothly, the installation should be done. 
  Contact the author if you come across any problem.

## Clean installation
./clean

This operation removes "build" and "dists" directories generated upon compilation
and results in the examples/tests_basic directory, including dat and ovf files, and figures in png


## Usage

* Use pysuerpcell as an API

    The major functions are collected in pysupercell.py library, as a cryst_struct class, to use it in your python script, use

    from pysupercell.pysupercell import cryst_struct

    Then you can create a instance of the class, for example, if you want to load structure from POSCAR, use

    struct = cryst_struct(file_poscar='POSCAR')

    struct.print_latt_param()


* Use pysupercell as an executable (python script)

    Some functionalities can be accessed via the pysc.py script under "bin" directory. Run

    pysc.py 

    to see the detailed description of usage


## Additional Notes

Note: This is a .md file in Markdown, to have a better view on the contants

we suggest you to install mdview, a free software for viewing .md files

Under Ubuntu, run the following commands to install it

sudo atp update

sudo apt install snapd

sudo snap install mdview

