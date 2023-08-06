#!/usr/bin/env python

import numpy as np
import phonopy.interface.vasp as vasp
import phonopy.structure.grid_points as gp
import phonopy.structure.atoms as atoms
from collections import Counter

# structure loaded from POSCAR
struct = vasp.read_vasp('POSCAR')
dataset = gp.get_symmetry_dataset(struct,symprec=1e-5)
for key,val in dataset.items(): print (key,val)
vasp.write_vasp('POSCAR_1',struct,direct=True)

exit()
# standardized structure
st = struct.copy()
for key,value in st.__dict__.items(): print (key,value)
symbols = [atoms.atom_data[n][1] for n in dataset['std_types']]
st._set_parameters(
cell=dataset['std_lattice'],
symbols=symbols,
numbers=dataset['std_types'],
scaled_positions=dataset['std_positions'])
vasp.write_vasp('POSCAR_std',st,direct=True)
