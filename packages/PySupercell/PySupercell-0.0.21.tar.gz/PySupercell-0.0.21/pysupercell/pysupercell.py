#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       crystal_structure.py                                         #
#  Dependence: phonopy (partial), outcar (partial)                          #
#  Usage:      define a class for crystal structures                        #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Oct 21, 2020                                                 #
#                                                                           #
#===========================================================================#


import os
import sys
import numpy as np
import warnings
import itertools
import copy 
import scipy.constants
from .QE_ibrav_lib import *

 

try:
    from termcolor import cprint
    color_print=True
except:
    color_print=False


Bohr_to_Angstrom = scipy.constants.physical_constants['Bohr radius'][0]*1e10


def parse_poscar(fil='POSCAR'):
    pyver = sys.version_info[0]
    if not os.path.isfile(fil): exit('cannot find the file {} for loading structure'.format(fil))
    gl=open(fil)
    gl.readline()
    scale = float(gl.readline())
    cell=scale*np.fromfile(gl,sep=' ',count=9).reshape(3,3)
    line=gl.readline().split()
    try:
        # vasp 4 and earlier
        counts = np.array(line, int)
        if pyver==2: syms = raw_input("input chemical species:")
        elif pyver==3: syms = input("input chemical species:")
        print (pyver,syms)
        addline="sed -i '5a\\"+syms+"' "+fil
        print('read chemical species from input: ',addline)
        os.system(addline)
        species=syms.split()
    except:
        # vasp 5 and later
        species =  line
        counts = np.array(gl.readline().split(), int)

    # Cartesian or fractional coordinates?
    line = gl.readline()[0].lower()
    if line.startswith('s'):
        print ('Selective dynamics implemented in {}'.format(fil))
        ctype = gl.readline()[0].lower()
    else:
        ctype = line

    if ctype.startswith('c'):  mult = np.linalg.inv(cell)
    elif ctype.startswith('d'): mult = np.eye(3)
    else: raise Exception('"{0}" is unknown coord. type'.format(ctype))
    natom=sum(counts)
    spos = np.zeros((natom, 3))
    for i in range(natom):
        spos[i] = np.array(gl.readline().split()[:3], float)
    spos = np.dot(spos, mult)
    return cell,species,counts,spos


def gen_Rvecs(ncell=1,boundary_condition=[1,1,1]):
    Rvecs = np.mgrid[-ncell:ncell+1,-ncell:ncell+1,-ncell:ncell+1].reshape(3,-1).T
    for i in range(3): 
        if boundary_condition[i]==0: Rvecs = Rvecs[Rvecs[:,i]==0]
    return Rvecs
 

# still under development
def parse_cif(fil):
    import re
    lines=np.array(open(fil).readlines())

    idx=np.where([re.search('_cell_length',line) for line in lines])
    a,b,c=[float(item.split()[1]) for item in lines[idx]]
    idx=np.where([re.search('_cell_angle',line) for line in lines])
    alpha,beta,gamma=[float(item.split()[1]) for item in lines[idx]]
    latt={'a':a,'b':b,'c':c,'alpha':alpha,'beta':beta,'gamma':gamma}

    idx=np.where([re.search('Uiso',line) for line in lines])
    atoms =  np.array([item.split() for item in lines[idx]])
    sites=atoms[:,0]
    symbols=atoms[:,1]

    cell = build_cell_from_latt_constants(14,1,latt)
    species = []
    counts = []
    for symbol in symbols: 
        cc = 0
        if symbol not in species:
            species.append(symbol)
            cc += 1
        else:
            counts.append(cc)
    pos=np.array(atoms[:,2:5],float)
    return cell,species,counts,pos


def parse_pwi(filpw='scf.in'):
    if not os.path.isfile(filpw): exit('cannot find {} for loading structure'.format(filpw))
    lines=open(filpw).readlines()
    nml=parse_pwi_nml(filpw=filpw)
    ibrav=nml['SYSTEM']['ibrav']
    celldm_=np.array(nml['SYSTEM']['celldm'])
    idx=np.where(celldm_)[0]
    celldm=np.zeros(7,float)
    celldm[idx+1]=celldm_[idx]
    nat=nml['SYSTEM']['nat']
    get_species=[item.rstrip('\n').split() for item in os.popen('grep -i upf {0}'.format(filpw)).readlines()]
    species=[item[0] for item in get_species]
    idx=np.where([re.search('ATOMIC_POSITIONS',line) for line in lines])[0][-1]
    get_pos=lines[idx+1:idx+nat+1]
    symbols=[get_pos[i].split()[0] for i in range(nat)]
    cc=collections.Counter(symbols)
    counts=np.array([cc[ispec] for ispec in species])
    pos=np.array([np.array(item.split()[1:],float) for item in get_pos])
    cell=make_cell_qe(ibrav,celldm)
    return cell,species,counts,pos



# Note: This function has a strong dependence on phonopy version
# If it reports some errors, most likely your need ot modify it
# according to the version of phonopy used in your platform
def get_symm_from_phonopy(symmprec=1e-4,poscar='POSCAR'):
    from phonopy.interface.vasp import read_vasp
    try: from phonopy.structure.grid_points import get_symmetry_dataset
    except: from phonopy.structure.cells import get_symmetry_dataset
    struct = read_vasp(poscar)
    dataset = get_symmetry_dataset(struct,symprec=symmprec)
    return dataset


def print_latt_param(latt):
    print ('\n{0}\nLattice Parameters\n{0}\n'.format('-'*40))
    keys=['a','b','c','alpha','beta','gamma']
    units=['Angs']*3+['deg']*3
    fmt='{0:8s}  {1:10.5f}  {2:8s}'
    for i in range(6):
        print(fmt.format(keys[i],latt[keys[i]],units[i]))
    print ('\n{0}\nLattice Parameters\n{0}\n'.format('-'*40))

def print_cell(cell,unit='Angs'):
    print ('\n{0}\nCell basis in {1}\n{0}\n'.format('-'*50,unit))
    print ((('{:15.10f}'*3+'\n')*3).format(*tuple(cell.flatten())))
    print ('{0}\nCell basis in {1}\n{0}\n'.format('-'*50,unit))

def get_cryst_ase(cell,symbols,pos):
    cryst_ase = Atoms(symbols=symbols,cell=cell.T, scaled_positions=pos.T,pbc=True)
    return cryst_ase


def writeVestaMode(vesta_file, nat, magmom,
    scaling_factor, norm_filter=0.1, colors=['red'], 
    transparency=1, counts=None, tag='mag', color_mapping_func=None, idir=0):

    vesta = open(vesta_file)
    vfile = vesta.read()
    vesta_front = vfile.split("VECTR")[0]
    vesta_end   = vfile.split("VECTT\n 0 0 0 0 0")[1]

    modef = open(vesta_file.replace('.vesta','_{}.vesta'.format(tag)), 'w')
    modef.write(vesta_front)

    eigvec = np.zeros((nat,3))
    if len(magmom) == nat:         eigvec[:,idir] = magmom
    elif len(magmom) == nat*3:     eigvec = magmom.reshape(-1,3)
    else:  exit ('Wrong size of MAGMOM!')

    sf = scaling_factor
    towrite = "VECTR\n"
    vec_count = 0
    vec = eigvec*sf
    for i in range(1,1+nat):
        if np.linalg.norm(vec[i-1])<norm_filter: continue
        vec_count += 1
        towrite += "%4d%9.5f%9.5f%9.5f\n"%(vec_count,*tuple(vec[i-1]))
        towrite += "%5d  0   0    0    0\n 0 0 0 0 0\n"%i
    towrite += " 0 0 0 0 0\n"
    towrite += "VECTT\n"

    def rgb_for_color(color):
        return {'red':[255,0,0],'green':[0,255,0],'blue':[0,0,255]}[color]

    fmt = "%4d%6.3f "+"%4d"*3+"%5.0f\n"
    vec_count = 0
    cc = np.cumsum(counts)
    for i in range(1,1+nat):
        if np.linalg.norm(eigvec[i-1]*sf)<norm_filter: continue
        vec_count += 1
        if color_mapping_func is not None:
            rgb = rgb_for_color(color_mapping_func(eigvec[i-1]))
        else:
            if len(colors)==1:  rgb = rgb_for_color(colors[0])
            else:               rgb = rgb_for_color(colors[np.where(cc>=i)[0][0]])
        towrite += fmt%(vec_count,0.5,*tuple(rgb),transparency)
    modef.write(towrite)
    return 0


def write_neighs_list(dists,iat,Rvecs):
    nat = dists.shape[0]
    nn_idx = np.mgrid[0:nat,0:len(Rvecs)].reshape(2,-1).T
    dists_iat = dists.flatten()
    sort_idx = np.argsort(dists_iat)
    fmt = '{:5d}  '+'{:4d} '*4 + '{:12.5f}\n'
    with open('neigh_atom_{}.dat'.format(iat),'w') as fw:
        fw.write('# Neighbors list of atom {}\n'.format(iat))
        fw.write('# Number of Neighbors = {} * {} = {}\n'.format(nat,len(Rvecs),nat*len(Rvecs)))
        fw.write('# Note: atom index starts from 0\n')
        fw.write(('{:>5s}  '+'{:>4s} '*4+'{:>12s}'+'\n').format('# inn','jat','Rx','Ry','Rz','dist'))
        for ii,inn in enumerate(sort_idx):
            fw.write(fmt.format(ii,nn_idx[inn,0],*tuple(Rvecs[nn_idx[inn,1]]),dists_iat[inn]))


def write_all_neighs_lists(dists_all,Rvecs,cutoff=3,num_neigh=20):
    nat = dists_all.shape[0]
    nn_idx = np.mgrid[0:nat,0:len(Rvecs)].reshape(2,-1).T
    fmt = '{:5d}  '+'{:5d} '*2 + '{:4d} '*3 + '{:12.5f}\n'
    with open('neigh_lists.dat','w') as fw:
        fw.write('# Neighbors list of {} atoms\n'.format(nat))
        fw.write('# Number of Neighbors/atom = {} * {} = {}\n'.format(nat,len(Rvecs),nat*len(Rvecs)))
        fw.write('# Distance cutoff = {}\n'.format(cutoff))
        fw.write('# Note: atom index starts from 0\n')
        fw.write(('{:>5s}  '+'{:>5s} '*2+'{:>4s} '*3+'{:>12s}'+'\n').format('# inn','iat','jat','Rx','Ry','Rz','dist'))
        for iat in range(nat):
            dists_iat = dists_all[iat].flatten()
            truncate_idx = np.where(dists_iat<cutoff)
            dists_iat_truncated = dists_iat[truncate_idx]
            nn_idx_truncated = nn_idx[truncate_idx]
            sort_idx = np.argsort(dists_iat_truncated)
            for ii,inn in enumerate(sort_idx):
                jat,iR = nn_idx_truncated[inn]
                fw.write(fmt.format(ii,iat,jat,*tuple(Rvecs[iR]),dists_iat_truncated[inn]))
    

def map_data(latt,data,comp='z',display_coord='xy',repeat_x=1,repeat_y=1,repeat_z=1,
    marked_positions=None,scatter_size=5,cmap='turbo',colorbar_orientation='vertical',
    vmin=0,vmax=0,show=True,grid_x=0,grid_y=0):
    import matplotlib.pyplot as plt
    coord_dir = {'x':0,'y':1,'z':2}
    aux_dir = {'xx':0,'yy':1,'zz':2,'yz':3,'xz':4,'xy':5}
    pos_cart = np.dot(data[:,:3],latt)
    if comp in aux_dir.keys():    ii = aux_dir[comp]+5; tag='$\sigma$'
    if comp.lower() in coord_dir.keys():  ii = coord_dir[comp.lower()]; tag=''
    m_data = data[:,ii]
    if comp in ['X','Y','Z']: m_data = pos_cart[:,coord_dir[comp.lower()]]
    dim_idx = [coord_dir[i] for i in display_coord]
    repeat = np.array([repeat_x,repeat_y,repeat_z])[dim_idx]
    reduced_latt = latt[dim_idx][:,dim_idx]
    coord = np.tile(pos_cart[:,dim_idx],(repeat[0],repeat[1],1,1))
    m_data = np.tile(m_data,(repeat[0],repeat[1],1))
    for i,j in np.ndindex(repeat[0],repeat[1]):
        coord[i,j] += np.dot([i,j],reduced_latt)
    points = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]])
    points_cart = np.dot(points,reduced_latt)
    kwargs = dict(c=m_data,cmap=cmap,s=scatter_size)
    if vmin<vmax: kwargs.update(vmin=vmin,vmax=vmax)
    fig,ax=plt.subplots(1,1)
    scat = ax.scatter(coord[...,0],coord[...,1],**kwargs)
    cb = fig.colorbar(scat,shrink=0.5,orientation=colorbar_orientation)
    cb.ax.set_title(tag+'$_{'+'{}'.format(comp)+'}$')
    ax.plot(*tuple(points_cart.T),ls='--',alpha=1,c='b')
    ax.set_aspect('equal')
    ax.set_axis_off()
    if marked_positions is not None:
        ax.scatter(*tuple(marked_positions[:,dim_idx].T),marker='*',fc='r',s=120)
    if grid_x!=0: 
        for ix in np.arange(1,grid_x): ax.axvline(ix*latt[0,0]/grid_x,ls='--',c='gray',alpha=0.6,zorder=-1)
    if grid_y!=0: 
        for iy in np.arange(1,grid_y): ax.axhline(iy*latt[1,1]/grid_y,ls='--',c='gray',alpha=0.6,zorder=-1)
    fig.tight_layout()
    if show: plt.show()
    return fig


def get_element_info_phonopy(symbol):
    import phonopy.structure.atoms as atoms
    return atoms.atom_data[atoms.symbol_map[symbol]]


# get the arc length of amp*sin(2*pi*omega*x) between [0,x]
# here x is in range (0,1/omega]
def get_sin_arc_length_scipy(x,amp=1,omega=1):
    from scipy.special import ellipe,ellipeinc
    fac = (2*np.pi*amp*omega)**2
    aa = np.sqrt(1+fac)/(2*np.pi*omega)
    cc = fac/(1+fac)
    E = aa*ellipeinc(2*np.pi*omega*x,cc)
    return E


def find_normal_vector(u,v,n1,m1,eps=1e-4,max_int=100):
    # Assume u and v are two noncollinear vectors, A=n1*u+m1*v.
    # Find B=n2*u+m2*v which is perpendicular to A. 
    # Here n1,n2,m1,m2 are all integers.
    A = n1*u + m1*v
    LA = np.linalg.norm(A)
    for (nn,mm) in itertools.product(range(max_int+1),range(max_int+1)):
        vecs=[(nn,mm),(-nn,mm),(nn,-mm),(-nn,-mm)]
        for (n2,m2) in vecs:
            if n2==m2==0: pass
            elif abs(np.dot(A,n2*u+m2*v)/LA/np.linalg.norm(n2*u+m2*v))<=eps:
                connect=np.array([A,n2*u+m2*v,[0,0,1]],float)
                if abs(np.linalg.det(connect))>0: return n2,m2
            else: pass
    if n2==max_int or m2==max_int:
        exit("cannot find the normal vector!")


class cryst_struct(object):
    def __init__(self,cell,species,counts,pos,scale=1,system='system',source='VASP'):
        self._system=system
        self._scale=scale
        self._cell=np.array(cell)
        self._species=np.array(species)
        self._symbols=np.repeat(species,counts)
        self._counts=np.array(counts)
        self._pos=pos                    # atomic positions in fracitonal coordinates
        self._natom=sum(counts)
        self._center=np.average(pos,axis=0)
        self._pos_cart = np.dot(self._pos,self._cell)
        self._center_cart = np.average(self._pos_cart,axis=0)


    @classmethod
    def load_poscar(cls,file_poscar='POSCAR'):
        cell,species,counts,pos = parse_poscar(file_poscar)
        return cls(cell,species,counts,pos)


    @classmethod
    def load_cif(cls,file_cif='struct.cif'):
        cell,species,counts,pos = parse_cif(file_cif)
        return cls(cell,species,counts,pos)


    @classmethod
    def load_pwscf_in(cls,file_pwscf_in='pwscf.in'):
        cell,species,counts,pos = parse_pwi(file_pwscf_in)
        return cls(cell,species,counts,pos)


    def get_ase(self):
        return get_cryst_ase(self._cell,self._symbols,self._pos)
      
    def latt_param(self):
        #a,b,c = np.linalg.norm(self._cell,axis=1)
        a = np.linalg.norm(self._cell[0])
        b = np.linalg.norm(self._cell[1])
        c = np.linalg.norm(self._cell[2])
        alpha = np.arccos(np.dot(self._cell[1],self._cell[2])/b/c)
        beta  = np.arccos(np.dot(self._cell[2],self._cell[0])/c/a)
        gamma = np.arccos(np.dot(self._cell[0],self._cell[1])/a/b)
        alpha, beta, gamma = np.rad2deg([alpha,beta,gamma])
        return {'a':a,'b':b,'c':c,'alpha':alpha,'beta':beta,'gamma':gamma}

    def real_cell_volume(self): return abs(np.linalg.det(self._cell))

    def reciprocal_cell(self):  return 2*np.pi*np.linalg.inv(self._cell).T

    def bond_length(self,i,j,cell_idx=False,ncell=1,boundary_condition=[1,1,1]):
        Rvecs = gen_Rvecs(ncell,boundary_condition)
        dists = np.linalg.norm( np.dot(self._pos[j]-self._pos[i]+Rvecs, self._cell), axis=-1)
        bond = np.min(dists)
        if cell_idx: return bond,np.where(dists==bond)
        return bond


    # get distance from atom iat to other atoms in home and neighboring cellls
    # boundary condition 1 and 0 are periodic and open, respectively, for three lattice vectors
    def get_dists_one_atom(self,iat=0,boundary_condition=[1,1,1],ncell=1,verbosity=0):
        Rvecs = gen_Rvecs(ncell,boundary_condition)
        dists = np.zeros((self._natom,len(Rvecs)))
        diff = st._pos - st._pos[iat]
        for i,Rvec in enumerate(Rvecs):
            dvec = np.dot( diff + Rvec, self._cell)
            dist = np.linalg.norm(dvec,axis=-1)
            dists[:,i] = dist
        if verbosity: write_neighs_list(dists,iat,Rvecs)
        return Rvecs,dists


    def get_dists_all(self,boundary_condition=[1,1,1],ncell=1,verbosity=2,cutoff=3):
        nat = self._natom
        Rvecs = gen_Rvecs(ncell,boundary_condition)
        dists_all = np.zeros((nat,nat,len(Rvecs)))
        nn = len(Rvecs)//2
        diff = np.array([[self._pos[jat] - self._pos[iat] for jat in range(nat)] for iat in range(nat)])
        for i,Rvec in enumerate(Rvecs[:nn+1]):
            dvec = np.dot( diff + Rvec, self._cell)
            dist = np.linalg.norm(dvec,axis =-1)
            dists_all[:,:,i] = dist
            dists_all[:,:,-i-1] = dist.T
        if verbosity: write_all_neighs_lists(dists_all,Rvecs,cutoff)
        return Rvecs,dists_all


    def find_neighbors(self,dists=None,Rvecs=None,bond_range=[0,2],boundary_condition=[1,1,1],ncell=1,cutoff=3):
        if dists is None and Rvecs is None: Rvecs,dists = self.get_dists_all(boundary_condition,ncell,cutoff)
        nat = len(dists)
        neigh = []
        bonds = []
        for iat in range(nat):
            neigh.append([])
            bonds.append([])
            indice = np.where(np.logical_and(bond_range[0]<dists[iat], dists[iat]<bond_range[1]))
            nn = len(indice[0])
            for ii in range(nn):
                neigh[iat].append([indice[0][ii],indice[1][ii]])
                bonds[iat].append(dists[iat,indice[0][ii],indice[1][ii]])
        return neigh,bonds


    def print_latt_param(self):
        print_latt_param(self.latt_param())
      
    def is_slab(self,vacuum=10):
        max_diff = np.max(self._pos_cart,axis=0)-np.min(self._pos_cart,axis=0)
        slab=True
        if self.latt_param()['a'] - max_diff[0]>=vacuum:
            print ('slab structure, vacuum along crystal axis a')
        elif self.latt_param()['b'] - max_diff[1]>=vacuum:
            print ('slab structure, vacuum along crystal axis b')
        elif self.latt_param()['c'] - max_diff[2]>=vacuum:
            print ('slab structure, vacuum along crystal axis c')
        else:
            slab=False
        return slab


    def check_inversion_center(self,inv_center=np.zeros(3)):
        cc=np.append(0,np.cumsum(self._counts))
        ss=range(-1,2)
        inv_pairs=[]
        fmt='{0:3s} {1:3d} <-> {2:3d} + [{3:3d},{4:3d},{5:3d}]\n'
        for ic in range(len(cc)-1):
            rr=range(cc[ic],cc[ic+1])
            for iat,jat in itertools.product(rr,rr):
                for i,j,k in itertools.product(ss,ss,ss):
                    #R=np.dot([i,j,k],self._cell)
                    R=np.array([i,j,k])
                    dist = self._pos[iat]+self._pos[jat]+R-2*inv_center
                    if np.linalg.norm(dist)<1e-3:
                        inv_pairs.append([self._species[ic],iat+1,jat+1,i,j,k])
                        break
        with open('inv_pair.dat','w') as fw:
            for ip,pp in enumerate(inv_pairs):
                fw.write(fmt.format(*tuple(pp)))


    def find_symmetry(self,symmprec=1e-4,report=False,filposcar='POSCAR_for_symm_analysis',saveposcar=False):
        if self.is_slab() and report: 
            print ('slab structure, be cautious when using the 3D space group for symmetry analysis!\n')
        spg = None
        spg_no = 0
        try:
            self.write_poscar_head(filposcar)
            self.write_poscar_atoms(filposcar,mode='a')
            symm_data=get_symm_from_phonopy(symmprec=symmprec,poscar=filposcar)
            spg_no = symm_data['number']
            spg = symm_data['international']
            if not saveposcar: os.remove(filposcar)
        except:
            raise Exception('Fail to extract symmetry information via phonopy.\nPlease check the phonopy version compatibility.')

        if spg is not None and spg_no>0:
            if report:
                print ("space group:    {0}".format(spg))
                print ("space group No: {0}".format(spg_no))
            return spg,spg_no
        else:
            raise Exception('we need phonopy to help find symmetry currently, please install it via pip install phonopy')


    def get_ibrav(self,symmprec=1e-4,report=False,filposcar='POSCAR_for_symm_analysis'):
        spg,spg_no=self.find_symmetry(symmprec=symmprec,filposcar=filposcar)
        brav   = brav_dic[spg_no]
        center = center_dic[spg[0]]
        ibrav=ibrav_dic[brav,center]
        if report:
            print ("Lattice type:   {0}".format(brav,center))
            print ("ibrav =         {0}".format(ibrav))
        return ibrav,brav,center


    def shift_atoms_to_home(self):
        while True:
            idx=np.where(self._pos>=1.)
            if len(idx[0])==0: break
            self._pos[idx] -= 1.
        while True:
            idx=np.where(self._pos<0.)
            if len(idx[0])==0: break
            self._pos[idx] += 1.
        #center = np.average(self._pos,axis=0)
        #self._pos += np.ones_like(self._pos)*0.5
        #for atom in self._pos: atom -= center
        self._pos_cart = np.dot(self._pos,self._cell)
        self._center = np.average(self._pos)
        self._center_cart = np.average(self._pos_cart)


    def find_celldm(self,ibrav=None):
        if not ibrav:
            ibrav,brav,center=self.get_ibrav()
        latt=self.latt_param()
        cell=self._cell
        celldm=np.zeros(7,float)
        celldm[1]=latt['a']/Bohr_to_Angstrom
        if ibrav>=8:
            celldm[2]=latt['b']/latt['a']
        if ibrav==9:
            celldm[1]=(cell[0,0]-cell[1,0])
            celldm[2]=(cell[0,1]+cell[1,1])/celldm[1]
            celldm[3]=latt['c']/latt['a']
        if ibrav==4 or (ibrav>=6 and ibrav!=9):
            celldm[3]=latt['c']/latt['a']
        if abs(ibrav)==5:
            a=latt['a']
            c=latt['c']
            R_cosalpha=(2*c**2-3*a**2)/(2*c**2+6*a**2)
            celldm[4]=R_cosalpha
            celldm[1]=a/np.sqrt(2-2*R_cosalpha)/Bohr_to_Angstrom
        if ibrav==12 or ibrav==13:
            celldm[4]=(np.cos(latt['gamma']/180*np.pi))  # remove abs(), Oct. 22
        if ibrav==14:
            celldm[4]=abs(np.cos(latt['alpha']/180*np.pi))
            celldm[5]=abs(np.cos(latt['beta']/180*np.pi))
            celldm[6]=abs(np.cos(latt['gamma']/180*np.pi))
        return celldm


    def get_label_k(self):
        if self._is_slab==False:
            ibrav,brav,center=self._get_ibrav()
            label_dic = {'G':[0.0, 0.0, 0.0],
                          'K':[1./3.,1./3.,0.0]}
            if ibrav==4:
                label_dic.setdefault('M',[0.5,  0.0,  0.0])
                label_dic.setdefault('K',[1./3.,1./3.,0.0])
                label_dic.setdefault('A',[0.0,  0.0,  0.5])
            elif ibrav==6 or ibrav==8:
                label_dic.setdefault('X',[0.5, 0.0, 0.0])
                label_dic.setdefault('M',[0.5, 0.5, 0.0])
                label_dic.setdefault('Z',[0.0, 0.0, 0.5])
                if ibrav==8:
                   label_dic.setdefault('Y',[0.0, 0.5, 0.0])
            else:
                print ( ('sorry! we do not have the label lib for this symmetry now!'))


    def write_poscar_head(self,filename = 'POSCAR'):
        cell_fmt=('{:20.12f}'*3+'\n')*3
        with open(filename,'w') as fpos:
            fpos.write('{0}\n'.format(self._system))
            fpos.write('{0:10.7f}\n'.format(self._scale))
            fpos.write(cell_fmt.format(*tuple(self._cell.flatten())))


    def write_poscar_atoms(self,filename='POSCAR',postype='Direct',mode='a',selective_dynamics=False,fix_dirs=None):
        with open(filename,mode) as fpos:
            fpos.write(' '.join(['{0:3s}'.format(item) for item in self._species])+'\n')
            fpos.write(' '.join(['{0:3d}'.format(item) for item in self._counts])+'\n')
            if selective_dynamics: fpos.write('Selective_dynamics\n')
            fpos.write(postype+'\n')
            print_pos={'cartesian':self._pos_cart,'direct':self._pos}[postype.lower()]
            if selective_dynamics: 
                dyn=[{True:'F',False:'T'}[i in fix_dirs] for i in range(3)]
                print('\n'.join([' '.join(['{0:25.18f}'.format(item) for item in pos])+' '.join(['{0:>3s}'.format(L) for L in dyn]) for pos in print_pos]),file=fpos)
            else:
                print('\n'.join([('{:25.18f}'*3).format(*tuple(pos)) for pos in print_pos]),file=fpos)


    def write_pw_cell(self,filename=None):
        ibrav,brav,center=self.get_ibrav()
        celldm=self.find_celldm(ibrav)
        print ("ibrav={}".format(ibrav), file=filename)
        for i in range(1,7):
            if celldm[i]: print ('celldm({:1d}) = {:20.12f}'.format(i,celldm[i]), file=filename)
        print ("nat = {0:3d}".format(self._natom), file=filename)
        print ("ntyp = {0:2d}".format(len(self._species)), file=filename)


    def write_pw_atoms(self,ctype='crystal',filename=None):
        if ctype=='crystal' or ctype=='direct':
            print ("ATOMIC_POSITIONS crystal", file=filename)
            for sym,atom in zip(self._symbols,self._pos):
                print ('{0:2s}'.format(sym)+' '.join(['{0:20.14f}'.format(at) for at in atom]), file=filename)
        else:
            print ("ATOMIC_POSITIONS cartesian", file=filename)
            for sym,atom in zip(self._symbols,self._pos_cart):
                print ('{0:2s}'.format(sym)+' '.join(['{0:20.14f}'.format(at) for at in atom]), file=filename)


    def write_wien2k_struct(self,case='case',title='TITLE',symmprec=1E-4):
        from collections import Counter
        import phonopy.structure.atoms as atoms
        phonopy=os.popen('which phonopy').read().rstrip('\n')
        if not phonopy:
            print ('We cannot write {0}.struct because phonopy is not installed'.format(case))
            return 1
        symm_data=get_symm_from_phonopy(symmprec=symmprec)
        op=symm_data['space_group_operations']
        nrotate=len(op)
        nequiv=len(set(symm_data['atom_mapping'].values()))
        ibrav,brav,center=self.get_ibrav(symmprec=symmprec)
        spg,spg_no=self.find_symmetry(symmprec=symmprec)
        if ibrav==2: latt_type='F'
        elif ibrav==3: latt_type='B'
        else: latt_type=brav[0]
        local_rot=np.eye(3,3)
        multi=np.array(list(Counter(symm_data['atom_mapping'].values()).values()))
        cc=[0]+[i for i in np.cumsum(multi)]

        atomic_num=[atoms.symbol_map[self._symbols[cc[iat]]] for iat in range(nequiv)]

        if ibrav==2 or ibrav==3: multi=multi/4
        rot=np.array([item['rotation'] for item in op])
        trans=np.array([item['translation'] for item in op])

        with open('{0}.struct'.format(case),'w') as fw:
            print (case, file=fw)
            print ('{0:3s} LATTICE,NONEQUIV.ATOMS:{1:3d} {2:3d} {3:42s}'.format(latt_type,nequiv,spg_no,spg), file=fw)
            #print ('\n'.join([' '.join(['{0:18.12f}'.format(item/Bohr_to_Angstrom) for item in vec]) for vec in self._cell]), file=fw)
            print ('MODE OF CALC=RELA unit=bohr', file=fw)
            for key in ['a','b','c','alpha','beta','gamma']: fw.write('{:11.6f}'.format(self.latt_param()[key]/Bohr_to_Angstrom))
            fw.write('\n')
            for iat in range(nequiv):
                ii=symm_data['atom_mapping'][iat+1]-1
                print ('ATOM {0:4d}: X={1:10.8f} Y={2:10.8f} Z={3:10.8f}'.format(-iat-1,self._pos[ii,0],self._pos[ii,1],self._pos[ii,2]), file=fw)
                print ('{0:9s} MULT={1:2d} {2:10s} ISPLIT={3:2d}'.format('',multi[iat],'',multi[iat]), file=fw)
                if multi[iat]>1:
                    for jat in range(cc[iat]+1,cc[iat+1]):
                         print ('{0:8d}: X={1:10.8f} Y={2:10.8f} Z={3:10.8f}'.format(-iat-1,self._pos[jat,0],self._pos[jat,1],self._pos[jat,2]), file=fw)
                print ('{0:2s}{1:<3d}      NPT={2:5d}  R0={3:9.8f} RMT={4:10.5f}   Z:{5:10.6f}'.format(self._symbols[ii],iat+1,781,0.0001,2,atomic_num[iat]), file=fw)
                print ('LOCAL ROT MATRIX:', file=fw)
                print (' '.join(['{0:10.8f}'.format(item) for item in local_rot[0]]), file=fw)
                print ('\n'.join(['{0:18s}'.format('')+' '.join(['{0:10.8f}'.format(item) for item in line]) for line in local_rot[1:]]), file=fw)
            fw.write('  {0:2d}      NUMBER OF SYMMETRY OPERATIONS \n'.format(len(op)))
            for iop in range(nrotate):
                fw.write('\n'.join([' '.join(['{0:2d}'.format(rot[iop,i,j]) for j in range(3)])+' {0:10.8f}'.format(trans[iop,i]) for i in range(3)]))
                fw.write('\n{0:8d}\n'.format(iop+1))
        return 0


    def get_mass(self):
        amass=[get_element_info_phonopy(sym)[-1] for sym in self._symbols]
        return amass


    def get_mass_density(self):
        amass=self.get_mass()
        return sum(amass)/(self.real_cell_volume()*1e-24*scipy.constants.Avogadro)


    def get_volume_density(self):
        return self.real_cell_volume()/self._natom


    def visualize_struct(self):
        try: import matplotlib.pyplot as plt
        except: exit('cannot import matplotlib!')
        try: from mpl_toolkits.mplot3d import Axes3D
        except: exit('cannot import mpl_toolkits!')
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        markersize=40
        colors=['r','b','g']
        orig=np.array([0,0,0])
        pp=(orig,)+tuple(self._cell)
        for j in range(4):
            lines = np.array([[pp[j],pp[i]+pp[j]] for i in range(1,4)])
            [ax.plot3D(*(tuple(points.T)),color='g',ls='--') for points in lines]
 
        for iat in range(self._natom):
            #if magmom[iat]>0:
            ax.scatter(self._pos_cart[iat,0],self._pos_cart[iat,1],self._pos_cart[iat,2],s=50,edgecolor='blue',facecolor='r')
            #ax.scatter(tuple(self._pos[iat,:]),s=markersize,edgecolor='blue',facecolor='r')
            #elif magmom[iat]<0:
            #   ax.scatter(struct._pos[iat,0],struct._pos[iat,1],struc.t_pos[iat,2],s=markersize,edgecolor='red',facecolor='r')
        fig.savefig('struct',dpi=300)


    def shift_pos(self,idir,shift,to_home=True): # shift atoms in crystal along idir (crystal axis) with a distance $shift (in Angstreom)
        self._pos_cart[:,idir] += shift
        self._pos=np.dot(self._pos_cart,np.linalg.inv(self._cell))
        if to_home: self.shift_atoms_to_home()


    def molar_mass(self):
        def gcd(a,b): return gcd(b, a % b) if b else a
        nfu=self._counts[0]
        for ispec in range(1,len(self._species)):
            nfu=gcd(self._counts[ispec],nfu)
        print ('No. of formula units in cell: {0}'.format(nfu))
        try:
            amass=[get_element_info_phonopy(sym)[-1] for sym in self._species]
            molar_mass=sum(self._counts/nfu*amass)
        except:
            exit('cannot calculate molar mass from phonopy')
        return molar_mass


    def verbose_crystal_info(self):
        self.print_latt_param()
        print ('Species  Natom')
        for ispec,nat in zip(self._species,self._counts):
            print ('{:7s}  {:5d}'.format(ispec,nat))
        print ('\n')
        print ('Molar_mass = {:15.8f} g/mol'.format(self.molar_mass()))
        print ('Mass density   = {:10.5f}'.format(self.get_mass_density()))
        print ('Volume density = {:10.5f} Atom/Angstrom^3'.format(self.get_volume_density()))

          
             
    def build_supercell(self,sc,eps=1e-4,nr=1,verbosity=0):
        sc_scale=np.linalg.det(sc)
        if verbosity:
            print ('Supercell scale = {:10.5f}'.format(sc_scale))
            if sc_scale==0:  warnings.warn('The supercell size is zero!','red')
            elif sc_scale<0: warnings.warn("The supercell basis vectors are not right-handed!")

        sc_scale=abs(sc_scale)
        sc_counts=int(round(sc_scale))*self._counts
        primitive_cell_warning = '\nThe supercell size is smaller than the unit cell.\nAre you constructing primitive cell?'
        for nn in range(2,5):
            if (sc_scale*nn-1.<eps): 
                warnings.warn(primitive_cell_warning)
                sc_counts=np.array(list(map(int,self._counts/nn)))
                sc_symbols=np.concatenate([[item]*cc for item,cc in zip(self._species,sc_counts)])
        sc_cell=np.dot(sc,self._cell)
        sc_pos=np.zeros((0,3),float)
        nimage_atom=np.zeros(self._natom,int)

        rb1 = int(round(abs(sc[0,0])+abs(sc[1,0])+abs(sc[2,0])))+nr
        rb2 = int(round(abs(sc[0,1])+abs(sc[1,1])+abs(sc[2,1])))+nr
        rb3 = int(round(abs(sc[0,2])+abs(sc[1,2])+abs(sc[2,2])))+nr
        Rvecs = np.mgrid[-rb1:rb1+1,-rb2:rb2+1,-rb3:rb3+1].reshape(3,-1).T
        sc_inv = np.linalg.inv(sc)
        for iat in range(self._natom):
            for ii,Rvec in enumerate(Rvecs):
                if nimage_atom[iat]==sc_scale: break
                pos_image = self._pos[iat] + Rvec
                pos_image = np.dot(pos_image, sc_inv)
                if (np.all(pos_image>-eps) and np.all(pos_image<1-eps)):
                    sc_pos=np.vstack([sc_pos,pos_image])
                    nimage_atom[iat]+=1
        if abs(sc_scale*self._natom -  float(len(sc_pos))) > abs(eps):
            warning = ['{}\nWarning'.format('='*100)]
            warning.append('The number of atoms in the supercell is incorrect, print it out and check it carefully!')
            warning.append('The supercell size        = {:<8.4f}'.format(sc_scale))
            warning.append('No. of atoms in unit cell = {:<4d}'.format(self._natom))
            warning.append('No. of atoms in supercell = {:<4d}'.format(len(sc_pos)))
            warning.append('images for each atom:'.format(nimage_atom))
            warning.append('='*100)
            if color_print==True: cprint ('\n'.join(warning),'red')
            else: print ('\n'.join(warning))
        sc_struct=cryst_struct(sc_cell,self._species,sc_counts,sc_pos)
        return sc_struct   


    def redefine_lattice(self,sc1=[1,0,0],sc2=[0,1,0],sc3=[0,0,1],orientation=1,verbosity=1):
        orien_dic={ 0:'as original',
                    1:'A along X, B in XY plane',
                    2:'A along X, C in XZ plane',
                    3:'B along Y, A in XY plane',
                    4:'B along Y, C in YZ plane'}
        sc_redef=np.array([sc1,sc2,sc3])
        struct_redef = self.build_supercell(sc_redef,nr=1,verbosity=verbosity)
        latt=struct_redef.latt_param()
        a=latt['a']
        b=latt['b']
        c=latt['c']
        alpha=latt['alpha']/180*np.pi
        beta=latt['beta']/180*np.pi
        gamma=latt['gamma']/180*np.pi
        if verbosity:
            print ('\n{0}\nRedefine lattice\n{0}'.format('-'*60))
            print ('Transformation matrix\n')
            print ((('{:10.5f} '*3+'\n')*3+'\n').format(*tuple(sc_redef.flatten())))
            print ('orientation={0}: {1}'.format(orientation,orien_dic[orientation]))
            if orientation==0:
                print ('Orientation of redefined cell follows original cell')
        if orientation==0:
            struct_def = copy.deepcopy(self) 
        elif orientation==1:
            struct_redef._cell[0] = np.array([a,0,0])
            struct_redef._cell[1] = np.array([b*np.cos(gamma),b*np.sin(gamma),0])
            cx=c*np.cos(beta)
            cy=c*np.cos(alpha)*np.sin(gamma)
            cz=np.sqrt(c**2-cx**2-cy**2)
            struct_redef._cell[2] = np.array([cx,cy,cz])
        elif orientation==2:
            struct_redef._cell[0] = np.array([a,0,0])
            struct_redef._cell[2] = np.array([c*np.cos(beta),c*np.sin(beta),0])
            cx=c*np.cos(gamma)
            cy=c*np.cos(gamma)*np.sin(alpha)
            cz=np.sqrt(c**2-cx**2-cy**2)
            struct_redef._cell[1] = np.array([cx,cy,cz])
        elif orientation==3:
             print ('still under development')
        elif orientation==4:
             print ('still under development')
        else:
             print ('still under development')
        struct_redef._pos_cart = np.dot(struct_redef._pos,struct_redef._cell)
        if verbosity: 
            print_cell(struct_redef._cell)
            struct_redef.print_latt_param()
        return struct_redef


    def build_slab(self,h,k,l,thickness,vacuum,atom_shift=0):
        print ( 'hkl=',h,k,l)
        self.shift_pos(2,atom_shift*self.latt_param()['c'])
        print ( 'build slab model, thickness=',thickness,'UCs, vacuum distance=',vacuum,'Angstroem')
        eyes=np.eye(3)
        def gcd(a,b): return gcd(b, a % b) if b else a
        def lcm(a,b): return max(a,b)*int(a*b==0) + a*b/gcd(a,b)*int(a*b!=0)
        if   np.sum(np.abs([h,k,l]))==0:  exit('Error! Miller index cannot be (000)!')
        if   abs(h)+abs(k)==0: u,v=eyes[[0,1]]
        elif abs(k)+abs(l)==0: u,v=eyes[[1,2]]
        elif abs(h)+abs(l)==0: u,v=eyes[[2,0]]
        else:
            #intercept on the crystal axis
            hkl_lcm=lcm(h,lcm(k,l))
            v = np.zeros(3,float)
            try:       hh = hkl_lcm/h
            except:    hh = 0; v=eyes[0]
            try:       kk = hkl_lcm/k
            except:    kk = 0; v=eyes[1]
            try:       ll = hkl_lcm/l
            except:    ll=0; v=eyes[2]
            print ( 'intercept on the crystal axis',hh,kk,ll)
            u=np.array(([hh,-kk,0]),float)/gcd(hh,kk)
            if np.linalg.norm(v)==0:
                v=np.array(([hh,0,-ll]),float)/gcd(hh,ll)
        w=np.array(([h,k,l]),float)/gcd(gcd(h,k),l)
        print ( 'u= {0}\nv= {1}\nw= {2}'.format(u,v,w))
        sc = np.array([u,v,w*thickness],float)
        sc_size=np.linalg.det(sc)
        if sc_size==0:    exit('error! supercell size is 0')
        elif sc_size<0:   sc = np.array([v,u,w*thickness],float)
        struct_slab = self.build_supercell(sc)
        # rescale the lattice constant and the fractional coordinates in the vacuum direction
        cc = np.linalg.norm(struct_slab._cell[2])
        #struct_slab._pos[:,2]=struct_slab._pos[:,2]*cc/(cc+vacuum)+vacuum/2/(cc+vacuum)
        struct_slab._cell[2] *= (cc+vacuum)/cc
        struct_slab.shift_pos(2,vacuum/2)
        return struct_slab


    # build a supercell repeated along idir, which forms a sine-like bending film
    # the original structure has to be a 2D sheet/film/slab
    # nn: repeat cell number
    # amp: amplitude of the sine curve
    # idir_per: the direction (index) to repeat the cell
    # idir_bend: the direction for bending of the sheet (usually the vacuum direction)
    def build_bending_supercell(self,nn=10,amp=1,idir_per=0,idir_bend=2,central_z=0.5,verbosity=1):
        sc_mat = np.eye(3)
        sc_mat[idir_per,idir_per] *= nn
        sc = self.build_supercell(sc_mat)
        sc.write_poscar_head(filename='POSCAR_flat')
        sc.write_poscar_atoms(filename='POSCAR_flat',mode='a')

        thickness = np.max(sc._pos_cart[:,idir_bend]) - np.min(sc._pos_cart[:,idir_bend])
 
        lp = sc.latt_param()
        for ang in ['alpha','beta','gamma']:
            assert abs(lp[ang] - 90)<1e-2, 'the cell for building bending structure should be orthogonal!'
    
        lat_orig = lp[{0:'a',1:'b',2:'c'}[idir_per]]
        c_orig = lp[{0:'a',1:'b',2:'c'}[idir_bend]]

        per_grid = np.linspace(0.8,1.2,5001)*lat_orig
        arc_lens = np.array([get_sin_arc_length_scipy(x,amp=amp,omega=1/x) for x in per_grid])
        lat_bend = per_grid[np.argmin(abs(arc_lens-lat_orig))]
        
        sc._cell[idir_per,idir_per] = lat_bend

        xgrid = np.linspace(0,lat_bend,20001)
        arc_grid = get_sin_arc_length_scipy(xgrid,amp,1/lat_bend)

        for iat in range(sc._natom):
            x_cart = sc._pos_cart[iat,idir_per]
            # xc and zc are the cart coord of the central line
            ix = np.argmin(abs(arc_grid-x_cart))
            xc = xgrid[ix]
            zc = amp*np.sin(2*np.pi/lat_bend*xc) - central_z*c_orig

            #tangent at the xc
            theta = np.arctan(2*np.pi/lat_bend*amp*np.cos(2*np.pi*xc/lat_bend))
            thick = (sc._pos[iat,idir_bend] - central_z)*c_orig
            new_x = xc - thick*np.sin(theta)
            new_z = zc + thick*np.cos(theta)

            sc._pos[iat,idir_per] =  new_x/lat_bend
            sc._pos[iat,idir_bend] = new_z/c_orig

        sc.shift_atoms_to_home()

        height = np.max(sc._pos_cart[:,idir_bend]) - np.min(sc._pos_cart[:,idir_bend])
        length = get_sin_arc_length_scipy(lat_bend,amp,1/lat_bend)

        print ('The lattice changed upon bending')
        print ('orignal lattice = {:10.5f} Angs'.format(lat_orig))
        print ('bending lattice = {:10.5f} Angs'.format(lat_bend))
        print ('shrinking ratio = {:10.5f} %'.format((1-lat_bend/lat_orig)*100))
        print ('height of sheet = {:10.5f} Angs'.format(height))
        print ('length of sheet = {:10.5f} Angs'.format(length))
        print ('bend amplitude  = {:10.5f} Angs'.format(amp))
        print ('film thickness  = {:10.5f} Angs <- estimated'.format(thickness))

        return sc


    def build_tube(self,n1,m1,negative_R=False):
        print ('chiral vector:',n1,m1)

        n2,m2 = find_normal_vector(self._cell[0],self._cell[1],n1,m1)
        sc = np.array([[n1,m1,0],[n2,m2,0],[0,0,1]],float)
        struct_rect = self.build_supercell(sc)

        struct_rect.write_poscar_head('POSCAR_sc')
        struct_rect.write_poscar_atoms('POSCAR_sc')

        clat=np.linalg.norm(struct_rect._cell[1])
        L = np.linalg.norm(struct_rect._cell[0])  # The circumference of the tube
        R0 = L/2/np.pi                  # The radius of the tube
        thickness=np.max(struct_rect._pos_cart[:,2])-np.min(struct_rect._pos_cart[:,2])
        alat=(R0+thickness)*4
        blat=(R0+thickness)*4

        ave_z=np.average(struct_rect._pos_cart[:,2])
        Origin=[0.5,0.5,0.0]
        print ('the thickness of the sheet is {:12.7f} Angstrom'.format(thickness))
        print ('the radius of the nanotube is {:12.7f} Angstrom'.format(R0))

        tube_pos=np.zeros((struct_rect._natom,3),float)
        for iat in range(struct_rect._natom):
            x,y,z = struct_rect._pos[iat]
            theta = x*2*np.pi
            height = z*struct_rect._cell[2,2]-ave_z
            R = R0 + height
            if negative_R:  R = R0 - height
            tube_pos[iat,0] = R/alat*np.cos(theta)
            tube_pos[iat,1] = R/blat*np.sin(theta)
            tube_pos[iat,2] = y
            tube_pos[iat] += Origin
        tube_cell = np.diag([alat,blat,clat])
        tube_counts=struct_rect._counts
        tube_name='tube_{0}_{1}'.format(n1,m1)
        struct_tube = cryst_struct(tube_cell,struct_rect._species,tube_counts,tube_pos,system=tube_name)
        return struct_tube


    def make_screw_dislocation(self,burgers_vector,screw_center,normal,screw_idir=2,verbosity=1,shift_to_home=True):
        st = copy.deepcopy(self)
        pos_cart = copy.deepcopy(st._pos_cart)
        glide = np.cross(normal,burgers_vector)
        G0= np.linalg.norm(glide)
        B0 = np.linalg.norm(burgers_vector)
        assert B0!=0, 'Burgers vector cannot be zero vector!'
        assert G0!=0, 'Burgers vector and the normal vector of glide plane are parallel, not allowed!'
        glide /= G0
        if verbosity:
            fmt = '[{:8.4f}, {:8.4f}, {:8.4f}]'
            print (('B = '+fmt).format(*tuple(burgers_vector)),end = ' ')
            print ((' screw_center = '+fmt).format(*tuple(screw_center)),end = ' ')
            print ((' G = '+fmt).format(*tuple(glide)),end = ' ')
            print (' screw direction = {}'.format(screw_idir))
        relative_pos_cart = pos_cart - np.dot(screw_center,st._cell)
        relative_pos_cart[:,screw_idir] = 0
        pos_norm = np.linalg.norm(relative_pos_cart,axis=1)
        idx = np.where(pos_norm<1e-5)
        pos_norm[idx] = 1
        cosines = np.dot(relative_pos_cart,glide)/pos_norm
        relative_angles = np.arccos(cosines)
        signs = np.sign(np.dot(np.cross(glide,relative_pos_cart),burgers_vector))
        relative_angles[signs<0] = 2*np.pi - relative_angles[signs<0]

        shift = np.array([a*B0 for a in relative_angles/(2*np.pi)])
        shift[idx] = B0
        pos_cart[:,screw_idir] += shift

        #shift = np.array([a*burgers_vector for a in relative_angles/(2*np.pi)])
        #shift[idx] = burgers_vector
        #pos_cart += shift
 
        st._pos_cart = pos_cart
        st._pos = np.dot(pos_cart, np.linalg.inv(st._cell))
        if shift_to_home:
            st.shift_atoms_to_home()
            st._pos_cart = np.dot(st._pos,st._cell)
        return st


    def get_kmesh(self,kgrid_density):
        def kmf(kgrid,gi):
            kd = int(gi/kgrid/2/np.pi)
            if kd == 0: kd = 1
            kds=np.arange(kd,kd+4)
            dd=gi/2/np.pi/kds
            return kds[dd<kgrid][0]
        kmesh=[kmf(kgrid_density, rl) for rl in np.linalg.norm(self.reciprocal_cell(),axis=1)]
        return kmesh


    def writekp(self,kgrid_density,outdir='./'):
        kmesh = self.get_kmesh(kgrid_density)
        with open('{}/KPOINTS'.format(outdir), 'w') as f:
            f.write('Auto-mesh\n0\nMonkhorst Pack\n')
            f.write('%2d %2d %2d\n' % tuple(kmesh))
            f.write('%2d %2d %2d\n' % (0,0,0))


def verbose_pkg_info(version):
    try:
        from pyfiglet import Figlet
        pysc_text = Figlet().renderText('PySupercell')
        print ('\n{}'.format(pysc_text))
    except:
        print ('\nRunning the script: {0}\n'.format(__file__.lstrip('./')))
    print ('{:>53s}'.format('version {}'.format(version)))
    print ('{:>53s}\n'.format('Copyright @ Shunhong Zhang 2023'))


if __name__=='__main__':
    print ('Running {}'.format(__file__))
 
