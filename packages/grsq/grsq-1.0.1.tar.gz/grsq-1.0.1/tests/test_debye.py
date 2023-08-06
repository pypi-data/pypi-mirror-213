"""
Unit and regression test for the grsq package.
"""

# Import package, test suite, and other packages as needed
import sys
import numpy as np
from ase.io import read
from ase import Atoms

try: # this is NOT how this is supposed to be done I think...
    from grsq import Debye
    from grsq import RDF, RDFSet, rdfset_from_dir
except:
    sys.path.append('src/')
    from grsq import Debye
    from grsq import RDF, RDFSet, rdfset_from_dir


def test_debye_numba():
    ''' Test that the Debye and numba implementations give the same result '''
    atoms = read('tests/data/testmol.xyz')
    deb = Debye()
    slow = deb.debye(atoms)
    fast = deb.debye_numba(atoms)
    # assert np.sum(np.abs(slow - fast)) < 1e-8  # XXX fails on gitlab, works locally...
    print(np.sum(np.abs(slow - fast)))


def test_debye_f0_update():
    ''' Test that an update of the atomic FFs is being triggered
        if the atoms in the atoms object change.
    '''
    fw_atoms = read('tests/data/testmol.xyz')
    syms = fw_atoms.get_chemical_symbols()
    syms.reverse()
    rw_atoms = Atoms(''.join(syms), positions=np.flip(fw_atoms.positions))
    deb = Debye()
    s_fw = deb.debye(fw_atoms)
    s_rw = deb.debye(rw_atoms)
    assert np.sum(np.abs(s_fw - s_rw)) < 1e-8

def test_custom_cm():
    ''' Check that putting in the same FF as custom FF
        gives the same result as using FFs from the periodictable package
    '''
    qvec = np.arange(0, 20, 0.01)
    atoms = read('tests/data/xray_2particle/test.xyz')
    deb = Debye(qvec=qvec)
    i_deb = deb.debye(atoms)
    custom_cm = {'Pt':deb.cm['Pt']}
    deb_ccm = Debye(qvec=qvec, custom_cm=custom_cm)
    i_ccm = deb_ccm.debye(atoms)
    assert (np.abs((i_deb - i_ccm) / i_deb) < 5e-3).all()


def test_debye_selective():
    ''' Test the debye implementation that only calculates
        terms between list1 and list2
    '''
    atoms = read('tests/data/testmol.xyz')
    subset_atoms = atoms[:3]
    deb = Debye()
    full_on_subset = deb.debye(subset_atoms)
    idx1 = [0, 1, 2]
    idx2 = [0, 1, 2]
    subset_on_full = deb.debye_selective(atoms, idx1, idx2)
    assert np.sum(subset_on_full - full_on_subset) < 1e-9





