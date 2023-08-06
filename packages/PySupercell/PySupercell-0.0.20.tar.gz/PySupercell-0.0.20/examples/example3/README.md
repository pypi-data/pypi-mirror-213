# create structure with screw dislocations

use burgers vector to define the extending direction

* First create the supercell structure, make sure that the crystal axes align with XYZ axes

    pysc --task=redefine --cell_orientation=1 --sc1=10,0,0 --sc2=0,6,0 --sc3=0,0,1

* Then run the command to create the dislocated structure

    pysc --task=screw_dislocation --burgers_vector=0,0,1 --poscar=POSCAR_redefine --screw_idir=2 --display_structure=T


*   The script "make_screw_diamond.py" 

    provides an alternative way to create the structure

    with more flexible and adavnced usages
