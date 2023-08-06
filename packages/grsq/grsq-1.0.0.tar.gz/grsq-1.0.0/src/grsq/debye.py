import numpy as np
from periodictable import cromermann
from grsq.accel import numbye

class Debye:

    def __init__(self, qvec=np.arange(0.0001, 10, 0.01), custom_cm=False):
        self.qvec = qvec                  # q vector
        self.f0 = None
        self.f0_elements = None
        self.custom_cm = custom_cm

        assert len(qvec.shape) == 1, 'Q-vector shape must be (N, )'

        # Cromer mann coefficients - look in f0_cromermann.txt
        # https://www.classe.cornell.edu/~dms79/x-rays/f0_CromerMann.txt
        # only used if custom_cm = True, otherwise the cromermann method
        # from periodictable will take care of it
        self.cm = {
            'Pt': {'a': np.array([27.00590, 17.76390, 15.71310, 5.783700]),
                   'b': np.array([1.512930, 8.811740, 0.4245930, 38.61030]),
                   'c': 11.68830},
            'Ag': {'a': np.array([19.28080, 16.68850, 4.804500, 1.046300]),
                   'b': np.array([0.6446000, 7.472600, 24.66050, 99.81560]),
                   'c': 5.179000},
            'Ir': {'a': np.array([30.70580, 15.55120, 14.23260, 5.536720]),
                   'b': np.array([1.309230, 6.719830, 0.1672520, 17.49110]),
                   'c': 6.968240},  # TODO: This is Ir4+.
            'Fe': {'a': np.array([11.04240, 7.374000, 4.134600, 0.4399000]),
                   'b': np.array([4.653800, 0.3053000, 12.05460, 31.28090]),
                   'c': 1.009700},  # TODO: This is Fe2+. Needs flexibility
            'P':  {'a': np.array([6.434500, 4.179100, 1.780000, 1.490800]),
                   'b': np.array([1.906700, 27.15700, 0.5260000, 68.16450]),
                   'c': 1.114900},
            'O':  {'a': np.array([3.048500, 2.286800, 1.546300, 0.8670000]),
                   'b': np.array([13.27710, 5.701100, 0.3239000, 32.90890]),
                   'c': 0.2508000},
            'C':  {'a': np.array([2.310000, 1.020000, 1.588600, 0.8650000]),
                   'b': np.array([20.84390, 10.20750, 0.5687000, 51.65120]),
                   'c': 0.2156000},
            'N':  {'a': np.array([12.21260, 3.13220, 2.01250, 1.166300]),
                   'b': np.array([5.701e-3, 9.89330, 28.9975, 0.582600]),
                   'c': -11.52900},
            'H':  {'a': np.array([0.4930020, 0.3229120, 0.1401910, 4.081e-2]),
                   'b': np.array([10.51090, 26.12570, 3.142360, 57.79970]),
                   'c': 3.0380001e-03},
            'Na': {'a': np.array([3.256500, 3.936200, 1.399800, 1.003200]),
                   'b': np.array([2.667100, 6.115300, 0.2001000, 14.03900]),
                   'c': 0.4040000},
            'I':  {'a': np.array([20.23320, 18.99700, 7.806900, 2.886800]),  # I-
                   'b': np.array([4.347000, 0.3814000, 27.76600, 66.87760]),
                   'c': 4.071200},
            'I0': {'a': np.array([20.14720, 18.99490, 7.513800, 2.273500]),
                   'b': np.array([4.347000, 0.3814000, 27.76600, 66.87760]),
                   'c': 4.071200},
            'Tl': {'a': np.array([21.39850, 20.47230, 18.74780, 6.828470]),   # Tl+
                   'b': np.array([1.471100, 0.5173940, 7.434630, 28.84820]),
                   'c': 12.52580},
            'Si': {'a': np.array([4.439180, 3.203450, 1.194530, 0.4165300]),   # Si4+
                   'b': np.array([1.641670, 3.437570, 0.2149000, 6.653650]),
                   'c': 0.7462970},
            'B':  {'a': np.array([2.054500, 1.332600, 1.097900, 0.7068000]),
                   'b': np.array([23.21850, 1.021000, 60.34980, 0.1403000]),
                   'c': -0.1932000},
            'S':  {'a': np.array([6.905300, 5.203400, 1.437900, 1.58630]),
                   'b': np.array([1.467900, 22.21510, 0.2536000, 56.17200]),
                   'c': 0.8669000},
            'Cl': {'a': np.array([11.46040, 7.196400, 6.255600, 1.645500]),
                   'b': np.array([1.0400000E-02, 1.166200, 18.51940, 47.77840]),
                   'c': -9.557400},
            'Ar': {'a': np.array([7.484500, 6.772300, 0.6539000, 1.644200]),
                   'b': np.array([0.9072000, 14.84070, 43.89830, 33.39290]),
                   'c': 1.444500}
                   }

    def atomic_f0(self, atom):
        ''' Atomic form factors '''
        if self.custom_cm:
            f0 = self.cm[atom]['c']
            a = self.cm[atom]['a']
            b = - self.cm[atom]['b']

            q2 = (self.qvec / (4 * np.pi))**2
            for n in range(4):
                f0 += a[n] * np.exp(b[n] * q2)
        else:
            f0 = cromermann.fxrayatq(atom, self.qvec)

        return f0

    def update_f0(self, atoms, custom_elements=None):
        if self.f0 is None:
            self.f0_elements = atoms.get_chemical_symbols()
            if custom_elements:
                self.f0_elements = custom_elements
            f0 = np.array([self.atomic_f0(sym) for sym in self.f0_elements])
            self.f0 = f0
        else:  # if the atoms have changed:
            these_syms = atoms.get_chemical_symbols()
            if these_syms != self.f0_elements:
                self.f0_elements = these_syms
                f0 = np.array([self.atomic_f0(sym) for sym in self.f0_elements])
                self.f0 = f0

    def debye_numba(self, atoms, custom_elements=None):
        self.update_f0(atoms, custom_elements)
        f0 = self.f0

        rs = atoms.get_positions()
        s = numbye(self.qvec, len(atoms), f0, rs, np.zeros(len(self.qvec)))
        return s

    def debye(self, atoms, custom_elements=None):
        ''' Debye Scattering from ASE atoms object'''

        s = np.zeros(len(self.qvec))
        self.update_f0(atoms, custom_elements)
        f0 = self.f0

        rs = atoms.get_all_distances()
        for q, qq in enumerate(self.qvec):
            for i in range(len(atoms)):
                s[q] += np.sum(f0[i, q] * f0[:, q] *
                               np.sinc(qq * rs[i, :] / np.pi))

        return s

    def debye_selective(self, atoms, idx1, idx2, custom_elements=None):
        ''' Only terms between atoms in lists idx1 and idx2
            (but not between atoms in either list) '''

        s = np.zeros(len(self.qvec))
        self.update_f0(atoms, custom_elements)
        f0 = self.f0

        rs = atoms.get_all_distances()
        for q, qq in enumerate(self.qvec):
            for i in idx1:
                s[q] += np.sum(f0[i, q] * f0[idx2, q] *
                               np.sinc(qq * rs[i, idx2] / np.pi))

        return s

