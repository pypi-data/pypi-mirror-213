# Example 1: create supercell and slab

This example show how to create a supercell of diamond-Si
and create a slab based on it

The primitive cell structure is used, stored in POSCAR

* To create a convention cell, use the command

    pysc --task=redefine --sc1=-1,1,1 --sc2=1,-1,1 --sc3=1,1,-1

    You can check the generated POSCAR_redefine file 

* To create a slab structure, run

    pysc --task=slab --hkl=111 --thickness=3 --vacuum=20

* To query the bond length between two atoms

    pysc --task=bond --atom_index=0,1 --poscar=POSCAR_slab

    pysc --task=latt_info --poscar=POSCAR_slab


* To write structure information for QE pw.x (under testing)
    
    v2qe
