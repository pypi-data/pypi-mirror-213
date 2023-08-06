''' A python script to generate input files for the Ewald code '''

# Import modules
from .structure import Structure
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
import re


class Ewald():
    '''
    Calculates the infinite periodic potential of a solid state crystal.
    The system is divided into three zones:
        Zone 1: qm region
        Zone 2: Exact point charge region
        Zone 3: Fitted Parameters

    Parameters
    ----------
    qm_region : file
        xyz file containing the qm region (vasp_suite asymmetric unit)
    filename : str
        name of the POSCAR/ CONTCAR structure file
    charges : file
        file containing the charges of the atoms in the POSCAR
    n : list
        list of sum expansion (2n+1) x (2n+1) x (2n+1)
    r_cut : float
        cutoff radius for the point charge region
    expansion : list
        list of the expansion parameters [ n1, n2, n3 ]
    Atom : str
        atom symbol and index for the central atom of the qm region <Dy1>

    Returns
    -------
    ewald.out : file
        output file containing coordinates and charges for xfield
    '''

    def __init__(
            self,
            qm_region,
            filename,
            charges,
            atom,
            n,
            r_cut,
            expansion,
            bound,
            verbose
            ):
        '''
        Initializes the Ewald class
        '''
        self._s = Structure(filename)
        self._s.Vasp_reader()
        self._charges = charges
        self._n = n
        self._r_cut = r_cut
        self._exp = np.array(expansion)
        self._atom = atom
        self._qm_region = qm_region
        self.read_charges()
        self._s.bv = self._s.bv / (2 * np.pi)
        self.alpha = 0.2
        self.evconv = 1e10 * constants.e / (4 * np.pi * constants.epsilon_0)
        self.bound = bound
        self.verbose = verbose

        # initial checks 
        a1, a2, a3 = self._s.av
        n1, n2, n3 = self._exp
        a1, a2, a3 = a1 * n1, a2 * n2, a3 * n3
        a_v = np.array([a1, a2, a3])
        min = np.linalg.norm(np.min(a_v, axis=0))
        if self._r_cut > min:
            raise ValueError("Cutoff radius is larger than the smallest lattice vector")

        # check unit cell charge
        if np.sum(self._q) != 0:
            raise ValueError("Unit cell is not charge neutral")

    def read_charges(self) -> None:
        '''
        Reads the charges from the file
        '''
        with open(self._charges, 'r') as f:
            _q = f.readlines()
        self._q = [float(i) for i in _q]
        if len(self._q) != self._s._N:
            raise ValueError(
                    "Number of charges does not match number of atoms")

    def _uc_print(self) -> None:
        '''
        Creates a print out for the unit cell information
        '''
        print('''
--------------------------------

     Unit Cell Information

--------------------------------
        ''')

        print("Lattice Vectors:")
        for i in range(len(self._s.av)):
            print(f"{self._s.av[i, 0]:.8f} {self._s.av[i, 1]:.8f} {self._s.av[i, 2]:.8f}")
        print("\nCoordinates:")
        for i in range(self._s._N):
            print(f"{self._s.coords[i, 0]:.8f} {self._s.coords[i, 1]:.8f} {self._s.coords[i, 2]:.8f} {self._s._atom_list[i]} {self._q[i]:.8f}")
        print("\nReciprocal Lattice Vectors:\n")
        for i in range(len(self._s.bv)):
            print(f"{self._s.bv[i, 0]:.8f} {self._s.bv[i, 1]:.8f} {self._s.bv[i, 2]:.8f}")

    def _compute_n(self) -> None:
        _n1 = list(range(-self._n[0], self._n[0]+1))
        _n2 = list(range(-self._n[1], self._n[1]+1))
        _n3 = list(range(-self._n[2], self._n[2]+1))
        self._n = np.array([[_n1[i], _n2[j], _n3[k]]
                            for i in range(len(_n1))
                            for j in range(len(_n2))
                            for k in range(len(_n3))], dtype=int)

    def _images(self):
        coords = self._s.coords
        _n = self._n
        _av = self._s.av
        images = np.array([coord + _n[i] for i in range(len(_n))
                           for coord in coords], dtype=float)
        images = images @ _av
        self.images: np.ndarray = images
        self._num_images = len(images)

    def _ewald_recip(self) -> None:
        '''
        Calculates the reciprocal space contribution to the Ewald sum
        '''
        prefactor = (np.pi * self._s.V)**(-1)
        av = self._s.av
        bv = self._s.bv
        q = self._q
        coords = self._s.coords
        _n = self._n

        e_recip = np.zeros((self._s._N, self._s._N), dtype=float)
        f_recip = np.zeros((self._s._N, 3), dtype=float)

        for i in range(self._s._N):
            for j in range(self._s._N):
                for k in range(len(_n)):
                    if i == j or _n[k, 0] == 0 or _n[k, 1] == 0 or _n[k, 2] == 0:
                        continue
                    else:
                        r = coords[i]@av - coords[j]@av
                        m = bv @ _n[k]
                        e_recip[i,j] += q[j] * np.exp(-(np.pi**2 * m@m / self.alpha**2)) / (m@m) * np.cos(2 * np.pi * m @ r) 
                        f_recip[i] += q[j] * np.exp(-(np.pi**2 * m@m / self.alpha**2)) * np.sin(2 * np.pi * m @ r) * m
        self.e_recip = self.evconv * prefactor * e_recip
        self.f_recip = prefactor * f_recip

    def _ewald_real(self) -> None:
        '''
        Calculates the real space contribution to the Ewald sum
        '''
        coords = self._s.coords @ self._s.av
        q = self._q
        q = [q] * len(self._n)
        q = np.array(q, dtype=float).flatten()

        e_real = np.zeros((self._s._N, self._num_images), dtype=float)
        f_real = np.zeros((self._s._N, 3), dtype=float)

        for i in range(self._s._N):
            for j in range(self._num_images):
                if (coords[i] == self.images[j]).all():
                    continue
                else:
                    r = np.linalg.norm(coords[i] - self.images[j])
                    e_real[i, j] = q[j] * sp.special.erfc(self.alpha * r) / r
                    f_real[i] += q[j] * sp.special.erfc(self.alpha * r) * (coords[i] - self.images[j]) / (r**3)
        self.e_real = self.evconv * e_real
        self.f_real = f_real

    def _ewald_self(self):
        e_self = np.zeros(self._s._N, dtype=float)
        f_self = np.zeros((self._s._N, 3), dtype=float)
        q = self._q

        for i in range(self._s._N):
            e_self[i] = -q[i] * 2 * self.alpha / np.sqrt(np.pi)
            f_self[i] = -q[i] * 2 * self.alpha / np.sqrt(np.pi) * self._s.coords[i] @ self._s.av
        self.e_self = self.evconv * e_self
        self.f_self = f_self

    def Calculate_Ewald(self) -> None:
        '''
        Calculates the Ewald sum
        '''
        self._uc_print()
        self._compute_n()
        self._images()
        print('''
--------------------------------

          Ewald Sum

--------------------------------
''')
        self._ewald_recip()
        self._ewald_real()
        self._ewald_self()
        self.e_real, self.e_recip = np.sum(self.e_real, axis=1), np.sum(self.e_recip, axis=1)
        self.e_total = self.e_real + self.e_recip + self.e_self
        for i in range(self.e_total.shape[0]):
            print(f'Index: {i}\nReal: {self.e_real[i]:.5f}, Recip: {self.e_recip[i]:.5f}, Self: {self.e_self[i]:.5f}, Total: {self.e_total[i]:.5f}')

    def _vector(self):
        '''
        Calculates the translation vector for the cell
        '''
        coords = self._s.coords
        atom = self._atom
        atom = re.split(r'(\d+)', atom)
        for ind, sym in enumerate(self._s.atoms):
            if sym == atom[0]:
                atom_index: int = ind

        _prev = np.sum(self._s.natoms[:atom_index])
        location = int(_prev + int(atom[1]) - 1)

        _dest = np.array([
            [0.5, 0.0, 0.0],
            [0.0, 0.5, 0.0],
            [0.0, 0.0, 0.5]
            ], dtype=float)

        if self._exp[0] % 2 == 0:
            _dest[0, 0] = 0.0
        if self._exp[1] % 2 == 0:
            _dest[1, 1] = 0.0
        if self._exp[2] % 2 == 0:
            _dest[2, 2] = 0.0

        _dest = _dest.sum(axis=0)
        _vector = coords[location] - _dest
        coords = coords - _vector
        coords %= 1.0
        self._s.coords = coords

    def _build_supercell(self):
        '''
        Generates the _supercell
        '''
        _exp = self._exp
        _av = self._s.av
        coords = self._s.coords
        e_total = self.e_total
        atom_list = self._s._atom_list

        _n1 = list(range(_exp[0]))
        _n2 = list(range(_exp[1]))
        _n3 = list(range(_exp[2]))

        _n = np.array([[_n1[i], _n2[j], _n3[k]]
                       for i in range(len(_n1))
                       for j in range(len(_n2))
                       for k in range(len(_n3))], dtype=int)

        coords = np.array([coord + _n[i]
                           for i in range(len(_n))
                           for coord in coords], dtype=float)

        for i in range(len(coords)):
            coords[i, 0] = coords[i, 0] / _exp[0] - 0.5
            coords[i, 1] = coords[i, 1] / _exp[1] - 0.5
            coords[i, 2] = coords[i, 2] / _exp[2] - 0.5

        _av[0], _av[1], _av[2] = _av[0] * _exp[0], _av[1] * _exp[1], _av[2] * _exp[2]
        coords = coords @ _av

        e_total = [e_total] * (_exp[0] * _exp[1] * _exp[2])
        e_total = np.array(e_total, dtype=float).flatten()

        q = [self._q] * (_exp[0] * _exp[1] * _exp[2])
        q = np.array(q, dtype=float).flatten()

        atom_list = [atom_list] * (_exp[0] * _exp[1] * _exp[2])
        atom_list = np.array(atom_list, dtype=str).flatten()

        self._supercell: np.ndarray = coords
        self._b = e_total
        self._q = q
        self._atom_list = atom_list

    def _create_zones(self):
        rcut = self._r_cut
        coords = self._supercell
        atom_list = self._atom_list
        q = self._q
        b = self._b
        file = self._qm_region

        with open(file, 'r') as f:
            _qm = f.readlines()
        _qm = [line.strip().split() for line in _qm]
        _qm = np.array(_qm[2:])
        _qm = np.array(_qm[:, 1:], dtype=float)

        _supercell = np.concatenate((coords,
                                     b[:, None],
                                     q[:, None],
                                     atom_list[:, None]), axis=1)

        _sphere = np.array([coord for coord in _supercell
                            if np.linalg.norm(coord[:3]) < rcut])

        _param = np.array([coord for coord in _supercell
                           if np.linalg.norm(coord[:3]) > rcut])

        self._sphere = _sphere
        self._param = _param
        self._qm = _qm
        self._supercell = _supercell

    def _drive_dipole(self) -> float:
        '''
        Calculates the dipole moment and drives it to zero
        '''
        _sphere = self._sphere
        _param = self._param

        ind1, ind2, ind3 = np.random.choice(len(_param), 3, replace=True)

        r = np.array([_param[ind1], _param[ind2], _param[ind3]])

        _r = np.array([_param[ind1, :3],
                       _param[ind2, :3],
                       _param[ind3, :3]], dtype=float)

        q = np.array([_param[ind1, 4],
                      _param[ind2, 4],
                      _param[ind3, 4]], dtype=float)

        # delete the three reandom charges
        np.delete(_param, [ind1, ind2, ind3], axis=0)

        # calculate the dipole moment
        dipole_sphere = np.array(_sphere[:, 4], dtype=float) @ np.array(_sphere[:, :3], dtype=float)
        dipole_param = np.array(_param[:, 4], dtype=float) @ np.array(_param[:, :3], dtype=float)
        dipole_total = dipole_sphere + dipole_param
        print(f'Initial dipole moment = [{dipole_total[0]:.5f} {dipole_total[1]:.5f} {dipole_total[2]:.5f}]')
        d = - np.array(dipole_total, dtype=float)

        # Solve the linear equation system
        x = np.linalg.lstsq(_r.T, d, rcond=None)[0]

        # Modify the charges
        q += x

        dipole_moment = q @ _r
        print(f'Fitted dipole moment = [{dipole_moment[0]:.5f} {dipole_moment[1]:.5f} {dipole_moment[2]:.5f}]')

        # combine the charges and coordinates 
        r[:, 4] = q

        # update the _param 
        _param = np.concatenate((_param, r), axis=0)

        # Calculate the new dipole moment
        dipole_param = np.array(_param[:, 4], dtype=float) @ np.array(_param[:, :3], dtype=float)
        dipole_total = dipole_sphere + dipole_param
        print(f'Final dipole moment = [{dipole_total[0]:.5f} {dipole_total[1]:.5f} {dipole_total[2]:.5f}]') 
        rms = np.sqrt(np.mean(dipole_total**2))
        print(f'RMS = {rms:.5f}\n')
        # Drive the dipole moment to zero
        self._param = _param
        return rms

        # calculate the change in charge for each of the three charges so the total dipole moment is zero 
    def Create_Zones(self) -> None:
        '''
        Creates the zones for the Ewald sum
        '''
        self._vector()
        self._build_supercell()
        self._create_zones()
        print('''
--------------------------------

     Driving Dipole Moment
           To Zero

--------------------------------
Beginning RMS trials...
''')
        rms = 2.0
        run = 0
        while rms > 1:
            rms = self._drive_dipole()
            run += 1
            if run > 100:
                raise ValueError('Could not drive the dipole moment to zero')

    def _fit_params(self):
        verbose: int = self.verbose
        _sphere = np.array(self._sphere)
        _param = np.array(self._param)
        _sphere_coords = np.array(_sphere[:, :3], dtype=float)
        _param_coords = np.array(_param[:, :3], dtype=float)
        print('''
--------------------------------

        Fitting Parameters

--------------------------------
''')

        bi = np.array(_sphere[:, 3], dtype=float)

        A = 1 / sp.spatial.distance.cdist(_sphere_coords, _param_coords, 'euclidean')
        rijs = sp.spatial.distance.squareform(1/sp.spatial.distance.pdist(_sphere_coords, 'euclidean'))
        P = rijs @ (self.evconv * np.array(_sphere[:, 4], dtype=float))
        P_param = A @ (self.evconv * np.array(_param[:, 4], dtype=float))
        bi -= P
        bi -= P_param

        c = np.ones((1, len(_param)))
        d = -(np.sum(np.array(_sphere[:, 4], dtype=float)) + np.sum(np.array(_param[:, 4], dtype=float))) * self.evconv

        Q, R = np.linalg.qr(c.T, mode='complete')

        AQ = A @ Q

        b2 = bi - AQ[:, 0] * (1/R[0]).T * d

        x2 = sp.optimize.lsq_linear(AQ[:, 1:],
                                    b2,
                                    bounds=(-15, 15),
                                    method='bvls',
                                    tol=1e-8,
                                    max_iter=10000,
                                    verbose=verbose)
        x2 = x2.x

        x1 = (1/R[0]).T * d
        x = np.concatenate((x1, x2), axis=0)
        x = Q @ x

        x = x / self.evconv
        x = np.array(_param[:, 4], dtype=float) + x

        # calcualte rmsd
        q_total = np.concatenate((_sphere[:, 4], x), axis=0)
        coords = np.concatenate((_sphere_coords, _param_coords), axis=0)
        rij = sp.spatial.distance.squareform(
                1/sp.spatial.distance.pdist(coords, 'euclidean'))
        rij[np.where(rij == np.inf)] = 0

        potential = self.evconv * np.array(q_total, dtype=float) @ rij
        ewald = np.array(_sphere[:, 3], dtype=float)
        rmsd = np.sqrt(np.sum(
            (potential[:len(_sphere)] - ewald)**2) / len(ewald))

        self.rmsd = rmsd
        self.q_total = q_total
        self.coords = coords
        self._x = x

    def _outputs(self) -> None:
        coords = np.array(np.hstack((self.coords,
                                     self.q_total[:, None])), dtype=str)
        # remove _qm region
        _qm = np.array(self._qm[:, :3], dtype=float)
        for i in range(len(_qm)):
            for j in range(len(coords)-1):
                if np.allclose(_qm[i, :3],
                               np.array(coords[j, :3], dtype=float)):
                    coords = np.delete(coords, j, axis=0)

        with open('ewald.out', 'w') as f:
            for i in range(len(coords)):
                f.write(f'{coords[i,0]} {coords[i,1]} {coords[i,2]} {coords[i,3]}\n')

    def Fitting(self) -> None:
        '''
        Fits the parameters for the Ewald summation
        '''
        self._fit_params()
        print(f'RMSD = {self.rmsd}')
        print(f'Charge of the sphere = {np.sum(np.array(self._sphere[:, 4]), dtype=float)}')
        print(f'Charge of the parameter region = {np.sum(self._x)}')
        print(f'Charge of sphere + parameter region = {np.sum(np.array(self._sphere[:, 4], dtype=float)) + np.sum(self._x)}')
        print(f'Number of sphere charges = {len(self._sphere) - len(self._qm)}')
        print(f'Number of parameter charges = {len(self._param)}')
        print(f'Number of total charges = {len(self._sphere) - len(self._qm) + len(self._param)}')
        self._outputs()


class Potential:
    '''
    Class for plotting potential on a mesh grid
    '''

    def __init__(
            self,
            filename: str,
            xy_grid: int,
            n_points: int,
            n_contours: int,
            ):
        '''
        Initializes the plotter
        '''
        self.filename = filename
        self.xy_grid = xy_grid
        self.n_points = n_points
        self.n_contours = n_contours

    def _data(self) -> None:
        '''
        Reads the data file
        '''
        with open(self.filename, 'r') as f:
            data = f.readlines()
        self.data = np.array([i.strip().split() for i in data], dtype=float)

    def _potential(self) -> None:
        '''
        Construct the mesh grid and calculate the potential
        '''
        data = self.data

        x = np.linspace(-self.xy_grid, self.xy_grid, self.n_points)
        y = np.linspace(-self.xy_grid, self.xy_grid, self.n_points)
        X, Y = np.meshgrid(x, y)

        Z = np.zeros_like(X)
        for i in range(len(X)):
            for j in range(len(X)):
                for k in range(len(data)):
                    Z[i, j] += data[k, 3] / np.sqrt((X[i, j] - data[k, 0])**2 + (Y[i, j] - data[k, 1])**2 + data[k, 2]**2)

        self.X = X
        self.Y = Y
        self.Z = Z

    def Plot(self) -> None:
        '''
        Plots the potential
        '''
        self._data()
        self._potential()

        fig, ax = plt.subplots()
        ax.contourf(self.X, self.Y, self.Z, self.n_contours, cmap='viridis')
        ax.set_xlabel('x/ Å')
        ax.set_ylabel('y/ Å')
        # show colorbar
        cbar = fig.colorbar(ax.contourf(self.X, self.Y, self.Z, self.n_contours, cmap='viridis'))
        cbar.set_label('Potential')
        plt.show()
