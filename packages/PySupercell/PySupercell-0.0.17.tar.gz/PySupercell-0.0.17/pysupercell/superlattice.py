#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       match_latt.py                                                #
#  Dependence: parse.py,crystal_structure.py                                #
#  Usage:      find matched superlattices for two given structures          #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Sep 25, 2019                                                 #
#                                                                           #
#===========================================================================#


from __future__ import print_function
import numpy as np
import itertools


desc_str = '''Objective: find match superlattice for two two-dimensional (2-D) structures'''

notes='''
Note 1: Before usage prepare the two 2-D structure files 
        POSCAR1, POSCAR2, respectively, in VASP5-POSCAR format
Note 2: Set the vacuum layer along the c-axis of the unit cell
'''

alert='''
\n{0}\n{1:>30s}\n{0}\n
Benchmark for this code has been carried out 
for some specific cases.
But the author cannot warrant full correctness
Be cautious when you use this code 
for real research or pulication! 
Check your output structures carefully.
Bug report or improvement suggestions are welcome.
Shunhong Zhang <szhang2@ustc.edu.cn>
\n{0}\n{1:>30s}\n{0}\n
'''.format('='*60,'WARNING')

def gcd(a, b): return gcd(b, a % b) if b else a
def area_cell(cell): return np.linalg.norm(np.cross(cell[0],cell[1]))


#find the commensurate supercell area for two 2-D structures
def find_match_area(cell_1,cell_2,maxarea,tolerance):
    print("\nSearching for matched area for superlattices")
    area_1=area_cell(cell_1)
    area_2=area_cell(cell_2)
    n1=area_1/area_2
    scale_list=[]
    for (i,j) in itertools.product(range(1,int(maxarea/area_1)),range(1,int(maxarea/area_2))):
        n2=float(i)/float(j)
        if abs(n1*n2-1)<tolerance and gcd(i,j)==1:
            scale_list.append((i,j))
    print ( 'done\n')
    return scale_list

#find possible shpaes for a supercell with spefified scale relative to the unit cell
def find_supercell(scale):
    scale+=1
    trans=[]
    for (i,j,m,n) in itertools.product(range(1,scale),range(scale),range(-scale,scale),range(1,scale)):
        if i*n-j*m == scale: trans.append([i,j,m,n])
    return np.array(trans)

# a supercell built from a unit cell by a 2D array [[i,j],[m,n]]
def supercell_info(trans,cell):
    i,j,m,n=trans
    sc_cell=[cell[0]*i+cell[1]*j,cell[0]*m+cell[1]*n,cell[2]]
    sc_a=np.linalg.norm(sc_cell[0])
    sc_b=np.linalg.norm(sc_cell[1])
    sc_angle=np.arccos(np.dot(sc_cell[0],sc_cell[1])/sc_a/sc_b) 
    sc_angle = np.rad2deg(sc_angle)  #angle in degree
    return [sc_a,sc_b,sc_angle]

def err(x,y):
    if x==y: return 0
    elif y:  return abs(x/y-1)
    else:    return abs(y/x-1)

#Judge whether two supercells are matched within specified tolerance
def match_supercell(cell_1,trans_1,cell_2,trans_2,tolerance,min_sc_angle,max_sc_angle):
    sa1,sb1,sangle1 = supercell_info(trans_1,cell_1)
    sa2,sb2,sangle2 = supercell_info(trans_2,cell_2)
    if err(sangle1, sangle2)<tolerance and min_sc_angle<=sangle1<=max_sc_angle and min_sc_angle<=sangle2<=max_sc_angle:
       if (err(sa1,sa2)<tolerance and err(sb1,sb2)<tolerance):
          #print ( 'angle1=',sangle1,'angle2=',sangle2,', angle matched!')
          #print ( 'a1=',sa1,', b1=',sb1,', a2=',sa2,', b2=',sb2,', lattice length matched!')
          return 'T'
       elif (err(sa1,sb2)<tolerance and err(sa2,sb1)<tolerance):
          #print ( 'angle1=',info1[2],'angle2=',info2[2],', angle matched!')
          #print ( 'a1=',info1[0],', b1=',info1[1],', a2=',info2[0],', b2=',info2[1],', lattice length matched! But a rotation is needed!')
          return 'R'
    else:
       return 'F'

def find_match_supercell(scale_set,cell_1,cell_2,tolerance,min_sc_angle,max_sc_angle):
    match_sc_set=[]
    for scale_1,scale_2 in scale_set:
        sc_set_1=find_supercell(scale_1)
        sc_set_2=find_supercell(scale_2)
        for (sc_1,sc_2) in itertools.product(sc_set_1,sc_set_2):
            if match_supercell(cell_1,sc_1,cell_2,sc_2,tolerance,min_sc_angle,max_sc_angle) == 'T':
                match_sc_1=np.eye(3,3,dtype=float)
                match_sc_2=np.eye(3,3,dtype=float)
                match_sc_1[:2,:2]=np.array(sc_1).reshape(2,2)
                match_sc_2[:2,:2]=np.array(sc_2).reshape(2,2)
                match_sc_set.append((scale_1,match_sc_1,scale_2,match_sc_2))
    return match_sc_set


def write_supercell_log(match_sc_set,cell_1,cell_2):
    print('\n{0} matched supercells found in total.'.format(len(match_sc_set)))
    if len(match_sc_set)==0: 
        print('You can retry with larger --tolernace or --maxarea')
    with open('supercell.log','w') as fw:
        fw.write('# Note: we use the lattice of struct 2 for building superstructures\n')
        fw.write('# err_a and err_b represent the lattice mismatch (in percent) along a and b axes\n')
        fw.write('# Superstructure crystal axes A and B are constructed by\n')
        fw.write('# A = i*a1 + j*a2, B = m*a1 + n*a2 (a1, a2 are unit cell crystal axes)\n')

        fw.write('\n{0}\n'.format('='*110))
        fw.write(' '.join(['{:>6s}'.format(item) for item in ('case','struct','size')]))
        fw.write(' '.join(['{:>12s}'.format(item) for item in ('a','b','gamma')]))
        fw.write(('{:>4s} '*4).format('i','j','m','n')+('{:>12s}'*2).format('err_a (%)','err_b (%)'))
        fw.write('\n{}\n'.format('='*110))
        for isc,match_sc in enumerate(match_sc_set): 
            scale_1,match_sc_1,scale_2,match_sc_2=match_sc
            sc_1=match_sc_1[:2,:2].flatten()
            sc_2=match_sc_2[:2,:2].flatten()
            fw.write(' '.join(['{:6d}'.format(item) for item in (isc,1,scale_1)]))
            fw.write(' '.join(['{:12.5f}'.format(item) for item in supercell_info(sc_1,cell_1)]))
            fw.write(' '.join(['{:4.0f}'.format(item) for item in sc_1])+'\n')
            fw.write(' '.join(['{:6d}'.format(item) for item in (isc,2,scale_2)]))
            fw.write(' '.join(['{:12.5f}'.format(item) for item in supercell_info(sc_2,cell_2)]))
            fw.write(' '.join(['{:4.0f}'.format(item) for item in sc_2]))
            a1,b1,ang1=supercell_info(sc_1,cell_1)
            a2,b2,ang2=supercell_info(sc_2,cell_2)
            fw.write(('{:12.5f}'*2).format(100*(a1-a2)/a2,100*(b1-b2)/b2))
            if isc<len(match_sc_set)-1: fw.write('\n{}\n'.format('-'*110))
        fw.write('\n{}\n'.format('='*110))
    print('see supercell.log for details\n')



def get_args():
    import argparse
    parser = argparse.ArgumentParser(prog='superlatt.py', description = desc_str)
    parser.add_argument('--poscar1', type=str, default='POSCAR1', help='POSCAR file for the  first structure')
    parser.add_argument('--poscar2', type=str, default='POSCAR2', help='POSCAR file for the second structure')
    parser.add_argument('--maxarea', type=float, default=200, help='maximum area for the superlattice, in unit of angstrom square')
    parser.add_argument('--tolerance', type=float, default=0.02, help='tolerance for lattice mismatch')
    parser.add_argument('--min_sc_angle',type=float,default=30,help='minimum angle for supercells, in degree, in rangg of (0,180)')
    parser.add_argument('--max_sc_angle',type=float,default=150,help='maximum angle for supercells, in degree, in range of (min_sc_angle, 180)')
    parser.add_argument('--interlayer_gap',type=float,default=3,help='interlayer gap for the two components of heterostructure')
    parser.add_argument('--vacuum',type=float,default=15,help='vacuum distance between periodic images of slab heterostructure')
    parser.add_argument('--pos_type',type=str,default='direct',help='style of atom coordinates, direct or cart')
    args = parser.parse_args()
    return parser, args


def verbose_setup(args):
    print ('\nMake superlattice from two structures')
    print ('{0}\nSuperlattice setup\n{0}'.format('-'*60))
    print ('Structure 1 from {}'.format(args.poscar1))
    print ('Structure 2 from {}'.format(args.poscar2))
    print ('Tolerance of lattice mismatch: {:6.3f} %'.format(args.tolerance))
    print ('Min angle of lattice vectors in supercells: {:6.3f} deg'.format(args.min_sc_angle))
    print ('Max angle of lattice vectors in supercells: {:6.3f} deg'.format(args.max_sc_angle))
    print ('Max area of supercell: {:8.3f} Angstrom^2'.format(args.maxarea))
    print ('Vacuum distance in vertical direction: {:6.3f} Angstrom'.format(args.vacuum))
    print ('Interlayer gap = {:6.3f} Angstrom'.format(args.interlayer_gap))
    print ('-'*60)
    print ('\nPlease verify the above setup\n')



if __name__=='__main__':
    print ('\nRunning the script: {0}\n'.format(__file__.lstrip('./')))
    try:
        from termcolor import cprint
        cprint (desc_str,'blue')
        cprint (notes,'green')
        cprint (alert,'red')
    except:
        print ('{0}\n{1}\n{2}'.format(desc_str,notes,alert))
