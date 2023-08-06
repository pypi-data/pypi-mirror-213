"""
Fixed radius nearest neighbors computation tools.
"""

import os
import numpy as np
from f2py_jit import jit
from atooms.core.utils import Timer

__all__ = ['VicsekNeighbors']


# Neighbors

class _Neighbors:
    def __init__(self, system, rcut=1., method='kdtree'):
        self.system = system
        self.rcut = rcut
        self.neighbors = None
        self.number_neighbors = None
        self.npart = len(self.system.particle)
        # Timers
        self.timer = {'id2ori': Timer(), 'f90': Timer(), 'kdtree': Timer()}

    def compute(self, box, positions, orientations):
        """
        Compute nearest neighbors in fixed radius.

        This function *must* return 
        - `self.sum_neighbors`: sum of neighbor orientation for each particle
        - `self.number_neighbors`: number of neighbors for each particle
        """
        pass

# Neighbors algorithms

class Python(_Neighbors):
    def __init__(self, system):
        _Neighbors.__init__(self, system, npart)

    def neighborold(self):
        """
        Legacy O(n*n) neighbor search algorithm

        Useful for unit tests; it isn't compatible with 'vicsek.py'
        """
        # TODO: adapt to standard compute method

        orients = []
        for o in self.system.particle:
            center = o.position

            orients.append([])

            for p in self.system.particle:  # append point to to numpy array
                if p is o:
                    continue
                dr = p.distance(o, self.system.cell)
                dr = np.sum(dr**2)**0.5
                if dr <= self.rcut:
                    orients[-1].append(float(p.orient))

        return orients

class F90(_Neighbors):
    def __init__(self, system, inline=False, f90file='neighbor_list_newton_inline.f90'):
        _Neighbors.__init__(self, system)

        self.f90file = f90file
        self.inline = inline
        self.ids = np.ones(self.npart)

    def _setup(self, nneigh):
        """
        Setup arrays for neighbor search in Fortran, using (estimated) number of neighbors for each particle
        """

        if self.neighbors is None or self.neighbors.shape[1] != self.npart or self.neighbors.shape[0] < nneigh:
            self.neighbors = np.ndarray(shape=(nneigh, self.npart),
                                        order='F', dtype=np.int32)
        if self.number_neighbors is None or len(self.number_neighbors) != self.npart:
            self.number_neighbors = np.ndarray(
                self.npart, order='F', dtype=np.int32)

    def _index_to_sum(self, orientations):
        """Convert neighbor indices to proper orientations"""

        # Setup arrays
        sum_neighbors = np.zeros(self.npart, dtype=complex)
        orientations = np.exp(1j*orientations)

        # Compute neighbor sum for each particle
        self.timer['id2ori'].start()
        for i in range(self.npart):
            j = self.number_neighbors[i]
            sum_neighbors[i] = np.sum(orientations[self.neighbors[0:j, i]].tolist())
        self.timer['id2ori'].stop()

        return sum_neighbors

    def compute(self, box, positions, orientations):
        """Compute nearest neighbors in radius using Fortran kernel"""

        # Initialize F90 module
        d = os.path.join(os.path.dirname(__file__), self.f90file)
        f90 = jit(d, inline=self.inline, flags="-O3 -ffast-math")

        # Initialize and setup arrays
        nneigh = int(np.pi * np.max(self.rcut)**2 * self.system.density * 1.)
        # nneigh : estimated number of neighs given starting density in circular area
        self._setup(nneigh)

        # Call Fortran function
        self.timer['f90'].start()
        err = f90.neighbor_list.compute(
            box, positions, self.ids, self.rcut, self.neighbors, self.number_neighbors)

        # Error flag handling
        if err:
            nneigh = max(self.number_neighbors)
            self._setup(nneigh)
            err = f90.neighbor_list.compute(
                box, positions, self.ids, self.rcut, self.neighbors, self.number_neighbors)
            assert not err, "something wrong with neighbor_list"
        self.timer['f90'].stop()

        # Shift Fortran ids to Python ids
        self.neighbors -= 1

        # Convert neighbors' indices to sum of neighbors' orientations
        self.sum_neighbors = self._index_to_sum(orientations)

        return self.sum_neighbors, self.number_neighbors

class KDTree(_Neighbors):
    def __init__(self, system):
        _Neighbors.__init__(self, system)

    def compute(self, box, positions, orientations):
        """
        Compute nearest neighbors in radius using kD-trees
        --------------------------------------------------
        kD-tree algorithm implementation: Francesco Turci and Daniele Coslovich
        """

        # Import needed pkgs
        from scipy import sparse
        from scipy.spatial import cKDTree

        # kD-tree algorithm
        self.timer['kdtree'].start()
        # Shift center to L/2 and transpose Fortran arrays to order='C'
        hbox = box/2.
        positions = np.transpose(positions) + hbox
        orient = np.transpose(orientations)
        # Define kD-tree and distance matrix
        tree = cKDTree(positions, boxsize=box)
        dist = tree.sparse_distance_matrix(tree, max_distance=self.rcut, output_type='coo_matrix')
        # important 3 lines: we evaluate a quantity for every column j
        data = np.exp(orient[dist.col]*1j)
        # construct a new sparse marix with entries in the same places ij of the dist matrix
        neighbors = sparse.coo_matrix((data, (dist.row, dist.col)), shape=dist.get_shape())
        # and sum along the columns (sum over j)
        sum_neighbors = np.squeeze(np.asarray(neighbors.tocsr().sum(axis=1)))
        # also get number of neighbors for each row/particle
        self.number_neighbors = neighbors.tocsr().getnnz(axis=0)
        self.timer['kdtree'].stop()

        return sum_neighbors, self.number_neighbors

# Interface

class VicsekNeighbors:
    """
    Interface for fixed-radius nearest neighbor search algorithms.

    Parameters
    ----------
    method: {'kdtree', 'f90'}
            Algorithm selection. Available algorithms are `KDTree`, `F90`, and `Python` (the latter to be used only for testing purposes).

    ## `F90` 
    Compute fixed-radius nearest neighbors using a O(n*n), Fortran algorithm. 
    The Fortran kernel is compiled just-in-time via `f2py-jit`; multiple choices are available

    - `neighbor_list.f90`: a basic implementation of the algorithm, without speed-ups, with inlining;
    - `neighbor_list_newton.f90`: Newton's third law is used to roughly halve computation times, keeping all other features intact;
    - `neighbor_list_inline.f90`: currently the fastest implementation, which doesn't rely on inlining (this might change in the future).

    Parameters
    ----------

    f90file:    string, optional
                Fortran kernel file name
    inline:     bool, default True
                Enable inlining in Fortran kernel execution. Currently, this is set to `False` due to performance issues.

    Callable using `method='f90'`.

    ## `KDTree` (default)
    Compute fixed-radius nearest neighbors using a O(n*log n), Python algorithm.
    This algorithm stems from [this](https://framagit.org/coslo/vicsek) implementation by Daniele Coslovich and Francesco Turci, and relies on `scipy.spatial.cKDTree`.

    Callable using `method='kdtree'`.

    ## `Python`
    Compute fixed-radius nearest neighbors using a basic, O(n*n), Python algorithm. 
    This mustn't be used outside testing. 

    It isn't callable via `method` variable. 
    """

    def __init__(self, system, method='kdtree', **kwargs):
        # Set noise
        if method == 'kdtree':
            self.method = KDTree(system)
        elif method == 'f90':
            self.method = F90(system, **kwargs)
        else:
            raise ValueError(f'wrong method {method}')

    def compute(self, box, positions, orientations):
        """
        Interface for `active.vicsek`.

        Parameters
        ----------

        box:            float or Numpy array
                        Simulation cell size.
        positions:      Numpy array
                        Particle positions. Must be Fortran ordered (`order='F'`).
        orientations:   Numpy array
                        Particle orientations. Must be Fortran ordered (`order='F'`).

        """
        return self.method.compute(box, positions, orientations)
