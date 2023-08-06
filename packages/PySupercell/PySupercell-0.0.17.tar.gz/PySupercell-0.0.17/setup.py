#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       setup.py                                                     #
#  Usage:      install the files as a lib and generate excutables           #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Jun 04, 2023                                                 #
#                                                                           #
#===========================================================================#


import glob
import os
import sys
import platform
from distutils.core import setup
#from setuptools import setup


def set_path(bin_dirs):
    current_path = os.environ['PATH'].split(os.pathsep)
    for bin_dir in bin_dirs:
        binpath="export PATH=\$PATH:{0}".format(bin_dir)
        print ('\nThe directory containing executive files is:\n{}'.format(bin_dir))
        print (binpath)
        if sys.platform=='linux':
            if bin_dir not in current_path:  
                print ('It has been added to ~/.bashrc')
                print ('Run "source ~/.bashrc" to activate it')
                add_binpath = 'echo "{0}"|cat >>~/.bashrc'.format(binpath)
                os.system(add_binpath)
            else:  
                print ('The utility directory already in the path\n')
        else:
            print ('You are using {} operating system'.format(sys.platform))
            print ('Please set the environment variable manually')



def test_modules(module_list,desc,pkg='asd'):
    import importlib
    import glob
    import shutil
    print ( '\n{0}\nTEST: {1}\n{0}'.format('='*50,desc))
    print ( '{0:40s} {1:10s}\n{2}'.format('MODULE','STATUS','-'*50))
    #cwd=os.getcwd()
    #os.chdir(os.path.expanduser("~"))
    for mod in module_list:
        try:
            mod = mod.replace('/','.')
            importlib.import_module(mod)
            print('{0:40s} success'.format(mod))
        except:
            print('{0:40s} failed!'.format(mod))
    print('{0}\n'.format('='*50))
    for item in glob.glob('*pyc'): os.remove(item)
    if os.path.isdir('__pycache__'): shutil.rmtree('__pycache__')



def write_code_info(kwargs_setup):
    with open('pysupercell/__init__.py','w') as fw:
        for key in ['__name__','__version__','__author__','__author_email__','__url__','__license__','__platforms__']:
            print ('{:<20s}  =  "{}"'.format(key,kwargs_setup[key.strip('__')]),file=fw)




core_modules=[
'QE_ibrav_lib',
'arguments',
'pysupercell',
'superlattice',
'__init__',
]

core_modules = ['pysupercell/{}'.format(item) for item in core_modules]
scripts_pysupercell = glob.glob('bin/*')

long_desc="A Open-source Python library for playing with crystal structures, such as supercell, dislocation, slab, and nanotube"


kwargs_setup=dict(
name='PySupercell',
version='0.0.17',
author='Shunhong Zhang',
author_email='zhangshunhong.pku@gmail.com',
url='https://pypi.org/project/PySupercell',
download_url='https://pypi.org/project/PySupercell',
keywords=['Python','Crystal structure','supercell'],
py_modules=core_modules,
license="MIT License",
description='Python library for creating and manipulating crystal structures',
long_description=long_desc,
platforms=[platform.system()],
install_requires=[
'numpy',
'matplotlib',
'scipy'
],
provides=["pysc","v2qe","qe2v","make_superlatt","mpi_make_superlatt","boltz_tools"],
scripts=scripts_pysupercell,
)


if __name__=='__main__':
    print ('{0}\nOperating System: {1}'.format('-'*50,platform.system()))
    print ('\n{0}\nINSTALL\n{0}\n'.format('-'*50))
    setup(**kwargs_setup)
    print ('{0}'.format('-'*50))
    write_code_info(kwargs_setup)
    test_modules(core_modules,'core modules')
    print ('\n{0}\nDone\n{0}\n'.format('-'*50))
