#!/usr/bin/env python

import numpy as np
import copy
from pysupercell.pysupercell import map_data
from astk.utility import parse
import matplotlib.pyplot as plt


def plot_screw_3d(latt,pos,screw_centers,glide_coord=0.5,cmap='turbo',show=True,
    repeat=1,separate=False,nn=300,alpha=0.8):
    from scipy.interpolate import griddata
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

    pos_cart = np.dot(pos,latt)
    aa = np.min(pos_cart[:,:2],axis=0)
    bb = np.max(pos_cart[:,:2],axis=0)
    coords = np.mgrid[aa[0]:bb[0]:1.j*nn,aa[1]:bb[1]:1.j*nn]
    xx,yy = coords
    gdata = griddata(pos_cart[:,:2],pos_cart[:,2], (xx,yy), method = 'nearest')
    fig = plt.figure()
    ax = Axes3D(fig)
    for ii in range(repeat):
        if not separate:
            surf = ax.plot_surface(xx, yy, gdata + ii*latt[2,2], 
            shade=True,linewidth=0, antialiased=True, cmap=cmap,alpha=0.7)
        else:
            surf = ax.plot_surface(xx[:,:nn//2], yy[:,:nn//2], gdata[:,:nn//2] + ii*latt[2,2], 
            shade=True,linewidth=0, antialiased=True, cmap=cmap,alpha=alpha)
            surf = ax.plot_surface(xx[:,nn//2:], yy[:,nn//2:], gdata[:,nn//2:] + ii*latt[2,2], 
            shade=True,linewidth=0, antialiased=True, cmap=plt.cm.get_cmap(cmap).reversed(),alpha=alpha)
     
    ax.set_xlim(-aa[0],bb[0])
    ax.set_ylim(-aa[1],bb[1])
    ax.set_zlim(-1,2)
    for screw_center in screw_centers:
        points = np.zeros((2,3))
        points[:,:2] = np.dot(screw_center,latt)[:2]
        points[:,2] = ax.get_zlim()
        ax.plot(*tuple(points.T),color='r',lw=2)
    fig.colorbar(surf,shrink=0.6)
    if show: plt.show()
    return fig


def find_directional_bonds(struct,directional_vec=[1,1,1],thr_angle=10):
    Rvecs,dists_all = struct.get_dists_all(verbosity=2)
    neigh,bonds = struct.find_neighbors(dists_all,Rvecs,bond_range=[1,2])
    directional_bonds=[]
    for iat in range(struct._natom):
        directional_bonds.append([])
        for inn,(jat,iR) in enumerate(neigh[iat]):
            dvec = np.dot(struct._pos[jat] + Rvecs[iR] - struct._pos[iat], struct._cell)
            if np.linalg.norm(dvec)<1e-3: continue
            nn = np.dot(dvec,directional_vec)/np.linalg.norm(dvec)/np.linalg.norm(directional_vec)
            if abs(nn)>1 and abs(abs(nn)-1)<1e-4: nn=1*np.sign(nn)
            angle = np.rad2deg(np.arccos(nn))
            if abs(angle)<thr_angle or (180-angle)<thr_angle: directional_bonds[iat].append([jat,iR])
    #directional_bonds = np.array(directional_bonds)
    return directional_bonds,Rvecs


def ax_plot_cut_bonds(ax,st,restart=False,bond_range=[0,2],cutting_coord=0.5,x_range=[0.25,0.75]):
    cut_bonds = []
    if not restart:
        Rvecs,dists_all = st.get_dists_all(verbosity=2)
        neigh,bonds = st.find_neighbors(dists_all,Rvecs,bond_range=[1,2])
    neighs = np.loadtxt('neigh_lists.dat',skiprows=5)[:,1:]
    for inn,(iat,jat,Rx,Ry,Rz,bond) in enumerate(neighs):
        iat = int(iat)
        jat = int(jat)
        if x_range[0]<st._pos[iat,0]<x_range[1] and x_range[0]<st._pos[jat,0]<x_range[1]:
            if (st._pos[iat,1]-cutting_coord) * (st._pos[jat,1] + Ry - cutting_coord) < 0:
                cut_bonds.append([iat,jat,Rx,Ry,Rz,bond])
    ax.axhline(cutting_coord*st._cell[1,1])
    cut_bonds = np.array(cut_bonds)
    idx = np.where(np.logical_and(cut_bonds[:,-1]<bond_range[1],cut_bonds[:,-1]>bond_range[0]))[0]
    cut_bonds = cut_bonds[idx]
    fig1,ax1 = plt.subplots(1,1)
    for inn,(iat,jat,Rx,Ry,Rz,bond) in enumerate(cut_bonds):
        points = np.array( [st._pos[int(iat)], st._pos[int(jat)] + np.array([Rx,Ry,Rz]) ]) 
        points = np.dot(points, st._cell)
        ax.plot(*tuple(points[:,:2].T),'g')
        ax1.plot(st._pos_cart[int(iat),0],bond,'o',c='r')
    fig1.savefig('bond_distribution',dpi=400)


def ax_plot_111_bonds(ax,st,directional_vec,restart=False,bond_range=[0,2],x_range=[0.25,0.75]):
    bonds_111,Rvecs = find_directional_bonds(st,directional_vec)
    for iat in range(st._natom):
        for inn,(jat,iR) in enumerate(bonds_111[iat]):
            points = np.array( [st._pos[iat], st._pos[jat] + Rvecs[iR] ]) 
            points = np.dot(points, st._cell)
            ax.plot(*tuple(points[:,:2].T),c='r',lw=1.2,zorder=-1)


def write_struct(struct,nx=1,ny=1,screw_centers=None,tag='screw_dipole'):
    fil = 'POSCAR_{}_{}_{}'.format(tag,nx,ny)
    struct._system='{}, size = {} * {}'.format(tag,nx,ny)
    if screw_centers is not None: struct._system += ', S = '+' '.join(['{:6.3f}'.format(ii) for ii in screw_centers.flatten()])
    print ('Writing structure {} to {}'.format(tag,fil))
    struct._write_poscar_head(filename=fil)
    struct._write_poscar_atoms(filename=fil,mode='a')


def adjust_screw_centers(screw_centers):
    adjusted_screw_centers = copy.copy(screw_centers)
    for ii,center in enumerate(screw_centers):
        cc = np.floor(center*np.array([nx,ny,1])) 
        cc = np.array(cc) + hollow_pos
        cc /= np.array([nx,ny,1],float)
        norm = np.linalg.norm(cc-center,axis=1)
        adjusted_screw_centers[ii] = cc[np.argmin(norm)]
    return adjusted_screw_centers


def make_screw_quadrupole(st_tilt,nx,ny,adjust_screw_centers_to_hollow=True,show=True):
    print ('\nBuilding screw quadrupole')
    st = st_tilt.redefine_lattice(verbosity=0)
    burgers_vectors = np.array([[0,0,1],[0,0,-1],[0,0,-1],[0,0,1]])*c
    screw_centers = np.array([[1,1,0],[3,1,0],[1,3,0],[3,3,0]])/4.
    if adjust_screw_centers_to_hollow: screw_centers = adjust_screw_centers(screw_centers)
    for ii,(burgers_vector,screw_center) in enumerate(zip(burgers_vectors,screw_centers)):
        st = st.make_screw_dislocation(burgers_vector,screw_center,normal,**screw_kwargs)
    write_struct(st,nx,ny,screw_centers,'screw_quadrupole_tilt')
    kwargs.update(marked_positions = np.dot(screw_centers,st._cell),)
    fig = map_data(st._cell,st._pos,**kwargs)
    if show: plt.show()


def make_screw_dipole(st_tilt,nx,ny,adjust_screw_centers_to_hollow=True,show=False):
    print ('\nBuilding screw dipole')
    st = st_tilt.redefine_lattice(verbosity=0)
    burgers_vectors = np.array([[0,0,1],[0,0,-1]])*c
    screw_centers  = np.array([[1/4,1/2,0],[3/4,1/2,0],]) 
    if adjust_screw_centers_to_hollow: screw_centers = adjust_screw_centers(screw_centers)
    for ii,(burgers_vector,screw_center) in enumerate(zip(burgers_vectors,screw_centers)):
        st = st.make_screw_dislocation(burgers_vector,screw_center,normal,**screw_kwargs)
    st._shift_atoms_to_home()
    #fig = plot_screw_3d(st._pos_cart[nn*3:4*nn])
    st_tilt._pos = st._pos
    st_tilt._pos_cart = np.dot(st_tilt._pos,st_tilt._cell)
    #write_struct(st,nx,ny,'screw_dipole')
    write_struct(st_tilt,nx,ny,screw_centers,'screw_dipole_tilt')
 
    trans_mat = st_tilt._cell/np.linalg.norm(st_tilt._cell,axis=1)[:,np.newaxis]
    directional_vec = np.dot([1,1,1], np.linalg.inv(trans_mat))
    kwargs.update(marked_positions = np.dot(screw_centers,st._cell),)
    fig = map_data(st._cell,st._pos,**kwargs) 
    ax=fig.axes[0]
    ax_plot_cut_bonds(ax,st,cutting_coord=screw_centers[0,1],restart=False)
    ax_plot_111_bonds(ax,st,directional_vec,x_range=[0,1])
    fig.tight_layout()
    fig.savefig('Screw_dipole_map_111',dpi=250)
    if show: plt.show()


def make_screw_monopole(st_tilt,nx,ny,adjust_screw_centers_to_hollow=True,show=False):
    print ('\nBuilding screw monopole')
    st = st_tilt.redefine_lattice(verbosity=0)
    burgers_vectors = np.array([[0,0,-1]])*c
    screw_centers = np.array([[0.5,0.5,0]])
    if adjust_screw_centers_to_hollow: screw_centers = adjust_screw_centers(screw_centers)
    for ii,(burgers_vector,screw_center) in enumerate(zip(burgers_vectors,screw_centers)):
        st = st.make_screw_dislocation(burgers_vector,screw_center,normal,**screw_kwargs)
    st._shift_atoms_to_home()
    st_tilt._pos = st._pos
    st_tilt._pos_cart = np.dot(st_tilt._pos,st_tilt._cell)
    #write_struct(st,nx,ny,'screw_monopole')
    write_struct(st_tilt,nx,ny,screw_centers,'screw_monopole_tilt')
 
    #fig = plot_screw_3d(st._cell,st._pos[nn*3:4*nn],screw_centers)
    trans_mat = st_tilt._cell/np.linalg.norm(st_tilt._cell,axis=1)[:,np.newaxis]
    directional_vec = np.dot([1,1,1], np.linalg.inv(trans_mat))
    kwargs.update(marked_positions = np.dot(screw_centers,st._cell),scatter_size=30)
    fig = map_data(st._cell,st._pos,**kwargs)
    Rvecs,dists_all = st.get_dists_all(boundary_condition=[0,0,1],verbosity=2)
    neigh,bonds = st.find_neighbors(dists_all,Rvecs,bond_range=[1,2])
    ax_plot_111_bonds(fig.axes[0],st,directional_vec,x_range=[0,1])
    fig.tight_layout()
    fig.savefig('Screw_monopole_map_111',dpi=250)
    if show: plt.show()


nx=9
ny=4
nn = nx*ny
shift = np.array([1/12,1/8,0])


fil = 'POSCAR_redefine'
uc_tilt = parse.parse_poscar(fil=fil)
uc_tilt._pos += shift
uc_tilt._pos_cart = np.dot(uc_tilt._pos,uc_tilt._cell)

sc = np.diag([nx,ny,1])
st_tilt = uc_tilt.build_supercell(sc,verbosity=0)
st = st_tilt.redefine_lattice(verbosity=0)
#write_struct(st,nx,ny,'supercell')
write_struct(st_tilt,nx,ny,tag='supercell_tilt')

pos0 = uc_tilt._pos
hollow_pos = np.array([
pos0[1] + pos0[11],
pos0[2] + pos0[8],
pos0[11]+ pos0[7],
pos0[4] + pos0[9]])/2

hollow_pos[:,2] = 0


c = st._latt_param()['c']
normal = np.array([0,1,0])

kwargs = dict(
comp='Z',
repeat_x=1,
repeat_y=1,
repeat_z=1,
scatter_size=10,
show=False,
cmap='turbo',
display_coord='xy',
#colorbar_orientation='horizontal',
colorbar_orientation='vertical',
grid_x=nx,
grid_y=ny,
)


screw_kwargs = dict(
screw_idir=2,
verbosity=1,
shift_to_home=False,
)

if __name__=='__main__':
    #fig = map_data(st._cell,st._pos,**kwargs)
    #make_screw_monopole(st_tilt,nx,ny)
    make_screw_dipole(st_tilt,nx,ny,show=True)
    #make_screw_quadrupole(st_tilt,nx,ny)

