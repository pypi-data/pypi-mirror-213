import numpy as np
from math import factorial as fac
from numba import njit, prange

@njit(parallel=True)
def numbye(qvec, natoms, f0, rs, s):
    for i in prange(natoms):
        for j in prange(i + 1, natoms):
            d = ((rs[i] - rs[j])**2).sum()**0.5
            s += 2 * f0[i, :] * f0[j, :] * np.sinc(qvec * d / np.pi)
        s += f0[i, :]**2
    return s


# Not used
#@njit(parallel=True)
#def numba_dist(pos, N, Ntot):
#    ''' Return distances between all N atoms in Nx3 pos array.
#        WIP: PBCs '''
#    dists = np.zeros(Ntot)
#    ct = 0
#    for i in prange(N):
#        for j in prange(i + 1, N):
#            d = ((pos[i] - pos[j])**2).sum()**0.5
#            dists[ct] = d
#            ct += 1
#
#    return dists
#
#
#@njit(parallel=True)
#def numba_dist_pbc(pos, N, Ntot, cell):
#    ''' Return distances between all N atoms in Nx3 pos array. '''
#    dists = np.zeros(Ntot)
#    c = cell / 2  # half cell length in xyz
#    ct = 0
#    for i in prange(N - 1):
#        for j in prange(i + 1, N):
#            r = (pos[i] - pos[j])  # vector. Consider np.rint for more speed
#            r_mic = (r + c) % cell - c
#            dists[ct] = (r_mic**2).sum()**0.5  # MICed distance
#            ct += 1
#
#    return dists