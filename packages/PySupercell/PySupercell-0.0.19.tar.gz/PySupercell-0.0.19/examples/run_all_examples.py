#!/usr/bin/env python

import os


def run_example_1():
    # Example 1: create supercell and slab
    """This example show how to create a supercell of diamond-Si
    and create a slab based on it
    The primitive cell structure is used, stored in POSCAR
    """

    os.chdir('example1')
    # To create a convention cell, use the command
    cmd = "pysc --task=redefine --sc1=-1,1,1 --sc2=1,-1,1 --sc3=1,1,-1"
    os.system(cmd)

    # You can check the generated POSCAR_redefine file 
    # To create a slab structure, run
    cmd = "pysc --task=slab --hkl=111 --thickness=3 --vacuum=20"
    os.system(cmd)

    # To query the bond length between two atoms
    cmd_1 = "pysc --task=bond --atom_index=0,1 --poscar=POSCAR_slab"
    cmd_2 = "pysc --task=latt_info --poscar=POSCAR_slab"
    os.system(cmd_1)
    os.system(cmd_2)

    # To write structure information for QE pw.x (under testing)
    cmd = "v2qe"
    os.system(cmd)
    os.chdir('..')


def run_example_2():
    os.chdir('example2')
    cmd = "pysc --task=tube --chiral_num=4,6"
    os.system(cmd)
    os.chdir('..')


def run_example_3():
    os.chdir('example3')
    cmd = "pysc --task=redefine --cell_orientation=1 --sc1=10,0,0 --sc2=0,6,0 --sc3=0,0,1"
    os.system(cmd)
    # Then run the command to create the dislocated structure
    cmd = "pysc --task=screw_dislocation --burgers_vector=0,0,1 --poscar=POSCAR_redefine --screw_idir=2 --display_structure=F"
    os.system(cmd)
    os.chdir('..')


def run_example_4():
    os.chdir('example4')
    cmd = "pysc --task=bending --nn=8 --idir_per=1 --idir_bend=2"
    os.system(cmd)
    cmd = "pysc --task=cmp --poscar1=POSCAR_flat --poscar2=POSCAR_bending"
    os.system(cmd)
    os.chdir('..')



if __name__=='__main__':
    run_example_1()
    run_example_2()
    run_example_3()
    run_example_4()
