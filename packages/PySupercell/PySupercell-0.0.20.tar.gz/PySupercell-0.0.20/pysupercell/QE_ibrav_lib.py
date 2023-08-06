#!/usr/bin/env python


import numpy as np
import os

r2=np.sqrt(2)
r3=np.sqrt(3)

center_dic={"F":("Face-centered"),
            "I":("Body-centered"),
            "A":("Base-centered"),
            "B":("Base-centered"),
            "C":("Base-centered"),
            "P":("P"            ),
            "R":("Rhombohedral"  )}
brav_dic={}
for num in range(1,3):      brav_dic.setdefault(num,"Triclinic"     )
for num in range(3,16):     brav_dic.setdefault(num,"Monoclinic"    )
for num in range(16,76):    brav_dic.setdefault(num,"Orthorhombic"  )
for num in range(76,143):   brav_dic.setdefault(num,"Tetragonal"    )
for num in range(143,168):  brav_dic.setdefault(num,"Trigonal"      )
for num in range(168,195):  brav_dic.setdefault(num,"Hexagonal"     )
for num in range(195,230):  brav_dic.setdefault(num,"Cubic"         )

ibrav_dic={ ("Free","P"):0,
            ("Cubic","P"):1, 
            ("Cubic","Face-centered"):2, 
            ("Cubic","Body-centered"):3,
            ("Hexagonal","P"):4,
            ("Trigonal","P"):4,
            ("Trigonal","Rhombohedral"):5,
            ("Tetragonal","P"):6,
            ("Tetragonal","Body-centered"):7,
            ("Orthorhombic","P"):8,
            ("Orthorhombic","Base-centered"):9,
            ("Orthorhombic","Face-centered"):10,
            ("Orthorhombic","Body-centered"):11,
            ("Monoclinic","P"):12,
            ("Monoclinic","Base-centered"):13,
            ("Triclinic","P"):14}


def build_cell_from_lattice_constants(latt,angle_unit='degree'):
    a=latt['a']
    b=latt['b']
    c=latt['c']
    alpha=latt['alpha']
    beta=latt['beta']
    gamma=latt['gamma']
    alpha_r, beta_r,gamma_r = np.deg2rad(alpha), np.deg2rad(beta), np.deg2rad(gamma)
    if angle_unit=='rad': alpha_r,beta_r,gamma_r = alpha,beta,gamma
    v1=[a,0,0]
    v2=[b*np.cos(gamma_r),b*np.sin(gamma_r),0]
    v3=[c*np.cos(beta_r),
        c*np.cos(beta_r)*np.cos(gamma_r)/np.sin(gamma_r),
        c*np.sqrt( 1 + 2*np.cos(alpha_r)*np.cos(beta_r)*np.cos(gamma_r) - np.cos(alpha_r)**2 - np.cos(beta_r)**2-np.cos(gamma_r)**2)/np.sin(gamma_r)]
    cell = np.array([v1,v2,v3],float)
    return cell


def get_connect(ibrav,latt):
    connect_dic={
                  2 : np.array(([-1./2.,  0.0,1./2.],[   0.0,1./2.,1./2.],[-1./2., 1./2.,  0.0]),float),
                  3 : np.array(([1./2., 1./2.,1./2.],[-1./2.,1./2.,1./2.],[-1./2.,-1./2.,1./2.]),float),
                  7 : np.array(([1./2.,-1./2.,1./2.],[ 1./2.,1./2.,1./2.],[-1./2.,-1./2.,1./2.]),float),
                  9 : np.array(([1./2., 1./2.,  0.0],[-1./2.,1./2.,  0.0],[   0.0,   0.0,  1.0]),float),
                 -9 : np.array(([1./2.,-1./2.,  0.0],[ 1./2.,1./2.,1./2.],[   0.0,   0.0,  1.0]),float),
                 10 : np.array(([1./2.,   0.0,1./2.],[ 1./2.,1./2.,  0.0],[   0.0, 1./2.,1./2.]),float),
                 11 : np.array(([1./2., 1./2.,1./2.],[-1./2.,1./2.,1./2.],[-1./2.,-1./2.,1./2.]),float),
                 13 : np.array(([1./2,    0.0,-1./2],[ 0.0,    1.0,  0.0],[ 1./2.,  0.0,  1./2]),float),
                 14: build_cell_from_lattice_constants(latt),
                 }

    if abs(ibrav)==5:
        a=latt['a'];c=latt['c']
        R_cosalpha=(2*c**2-3*a**2)/(2*c**2+6*a**2)
        print ( "cosalpha(celldm4)=",R_cosalpha)
        tx=np.sqrt((1-R_cosalpha)/2)
        ty=np.sqrt((1-R_cosalpha)/6)
        tz=np.sqrt((1+2*R_cosalpha)/3)
        A = np.array(([[1,0,0],[-1./2.,r3/2,0],[0,0,c/a]]),float)   #basis vectors of the hexagonal representation
        if ibrav==5 or ibrav==-5:
            B = 1/np.sqrt(2-2*R_cosalpha)*np.array(([[tx,-ty,tz],[0,2*ty,tz],[-tx,-ty,tz]]),float)
        #elif ibrav==-5:
        #   u = tz + 2*r2*ty
        #   v = tz - r2*ty
        #   B = 1/np.sqrt(6-6*R_cosalpha)*np.array(([[u,v,v],[v,u,v],[v,v,u]]),float)
        #print ( np.linalg.det(B*A**-1))
        connect_dic.setdefault(ibrav,np.dot(B,np.linalg.inv(A)))
    else:
        connect_dic.setdefault(ibrav,np.eye(3))
    if np.linalg.det(connect_dic[ibrav])==0:
        print ( "The connect matrix is:\n",connect_dic[ibrav])
        exit("The connect matrix is singular! Check your structure carefully!")
    return connect_dic[ibrav]


def make_cell_qe(ibrav,celldm,verbosity=True):
    if verbosity:
        print ('\nbuild cell from the following parameters:')
        print ('ibrav={0}'.format(ibrav))
        for i in range(1,7):
            print ('celldm({0}) ={1:12.6f}'.format(i,celldm[i]))
        print ('make sure they are correct\n')
    def dv(): exit ('make_cell_qe: under development!')
    a=celldm[1]
    b=a*celldm[2]
    c=a*celldm[3]
    cell=np.zeros((3,3),float)
    if ibrav in [1,2,3]:
        cell=np.diag([celldm[1]]*3)
    if ibrav==4:
        cell[0,0]=a
        cell[1,0]=a*np.cos(2*np.pi/3)
        cell[1,1]=a*np.sin(2*np.pi/3)
        cell[2,2]=c
    elif ibrav==5:
        dv()
    elif ibrav==6:
        cell=np.diag([a,a,c])
    elif ibrav==7:
        cell[0]=np.array([ a,-a,c])/2.
        cell[1]=np.array([ a, a,c])/2.
        cell[2]=np.array([-a,-a,c])/2.
    elif ibrav in [8,9]:
        cell=np.diag([a,b,c])
    elif ibrav==10:
        dv()
    elif ibrav==11:
        dv()
    elif abs(ibrav)==12:
        cell[0,0]=a
        if ibrav==12:
            cell[2,2]=c
            cell[1,0]=b*celldm[4]
            cell[1,1]=b*np.sqrt(1-celldm[4]**2)
        elif ibrav==-12:
            cell[1,1]=b
            cell[2,0]=c*celldm[4]
            cell[2,2]=c*np.sqrt(1-celldm[4]**2)
    elif abs(ibrav)==13:
        if ibrav==13:
            cell[0]=np.array([a/2,0,-c/2])
            cell[1]=np.array([b*celldm[4],b*np.sqrt(1-celldm[4]**2),0])
            cell[2]=np.array([a/2,0, c/2])
        elif ibrav==-13:
            cell[0]=np.array([ a/2,b/2,0])
            cell[1]=np.array([-a/2,b/2,0])
            cell[2]=np.array([c*celldm[4],0,c*np.sqrt(1-celldm[4]**2)])
    elif ibrav==14:
       cell[0,0]=a
       cell[1,0]=b*celldm[6]
       cell[1,1]=b*np.sqrt(1-celldm[6]**2)
    elif ibrav==0:
       print ('free lattice, no celldm implemented!')
    return cell*units.Bohr






def_ibrav='''
ibrav =  0: Free lattice (The card CELL_PARAMETERS required in this case)
ibrav =  1: Simple cubic lattice (sc),        v1=a(1,0,0),       v2=a(0,1,0),                       v3=a(0,0,1)
ibrav =  2: Face-centered cubic (fcc),        v1=(a/2)(-1,0,1),  v2=(a/2)(0,1,1),                   v3=(a/2)(-1,1,0)
ibrav =  3: Body-centered cubic (bcc),        v1=(a/2)(1,1,1),   v2=(a/2)(-1,1,1),                  v3=(a/2)(-1,-1,1)
ibrav =  4: Hexagonal and Trigonal P,         v1=a(1,0,0),       v2=a(-1/2,sqrt(3)/2,0),            v3=a(0,0,c/a)
ibrav =  5: Trigonal R, 3 fold axis c,        v1=a(-tx,ty,tz),   v2=a(0,2ty,tz),                    v3=a(-tx,-ty,tz)
ibrav = -5: Trigonal R, 3 fold axis <111>,    v1=(u,v,v),        v2=(v,u,v),                        v3=(v,v,u)        (under test)
ibrav =  6: Tetragonal P (st),                v1=a(1,0,0),       v2=a(0,1,0),                       v3=a(0,0,c/a)
ibrav =  7: Body-centered tetragonal (bct),   v1=a/2*(1,-1,c/a), v2=a/2*(1,1,c/a),                  v3=a/2*(-1,-1,c/a)
ibrav =  8: Orthorhombic P,                   v1=a(1,0,0),       v2=a(0,b/a,0),                     v3=a(0,0,c/a)
ibrav =  9: Base-centered orthorhombic,       v1=(a/2,b/2,  0),  v2=(-a/2,b/2,  0),                 v3=(   0,   0,  c)  (Note: C as the base face)
ibrav = -9: Base-centered orthorhombic,       v1=(a/2,-b/2, 0)   v2=( a/2,b/2,  0),                 v3=(   0,   0,  c)  (Note: C as the base face)
ibrav = 10: Face-centered orghogonal (fco),   v1=(a/2, 0, c/2),  v2=( a/2,b/2,  0),                 v3=(   0, b/2,c/2)
ibrav = 11: Body-centered orthorhombic (bco), v1=(a/2,b/2,c/2),  v2=(-a/2,b/2,c/2),                 v3=(-a/2,-b/2,c/2)
ibrav = 12: Monoclinic P,                     v1=(a,0,0),        v2=(b*cos(gamma),b*sin(gamma),0),  v3 = (0,0,c)
ibrav =-12: Monoclinic P,                     v1 = (a,0,0),      v2 = (0,b,0),                      v3 = (c*cos(beta),0,c*sin(beta))
ibrav = 13: Based-centered monoclinic,        v1=(a/2, 0,-c/2),  v2=(b*cos(gamma),b*sin(gamma),0),  v3=(a/2,0,c/2)      (Note: B as the base face)
ibrav = 14: Triclinic,                        v1=(a,0,0),        v2=(b*cos(gamma),b*sin(gamma),0),  
            v3 =  (c*cos(beta),c*cos(beta)cos(gamma)/sin(gamma),c*sqrt( 1 + 2*cos(alpha)cos(beta)cos(gamma)
                - cos(alpha)^2-cos(beta)^2-cos(gamma)^2)/sin(gamma))
'''

def_ibrav_note='''
IMPORTANT NOTICE: until QE v.6.4.1, axis for ibrav=-13 had a
different definition: v1(old) = v2(now), v2(old) = -v1(now)
'''


if __name__=='__main__':
    print ('Runing script {0}\n'.format(__file__.lstrip('./')))
