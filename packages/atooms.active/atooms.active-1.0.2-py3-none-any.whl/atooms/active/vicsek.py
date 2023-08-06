"""
Vicsek model simulation backend.
"""

import os
import numpy as np
from f2py_jit import jit

__all__ = ['Vicsek']

_f90 = jit("""
subroutine fold(pos, center, side)
	implicit none
	double precision, intent(inout) :: pos(:,:)
	double precision, intent(in)	:: center(:), side(:)
	integer							:: i
	do i = 1,size(pos,2)
		pos(:,i) = pos(:,i) - center
		pos(:,i) = pos(:,i) - nint(pos(:,i)/side)*side
		pos(:,i) = pos(:,i) + center
	end do
end subroutine fold
""", flags="-O3 -ffast-math")


# Backend
def noise_scalar(orientations, number_neighbors, sum_neighbors, eta, n):
    """Compute orientations with scalar noise (Vicsek et al, 1995; Grégoire and Chaté, 2008)."""
    rnd = eta * np.random.uniform(-np.pi, np.pi, size=n)
    avg = np.angle(sum_neighbors)
    do = avg+rnd
    return do

def noise_vectorial(orientations, number_neighbors, sum_neighbors, eta, n):
    """Compute orientations with vectorial noise (Grégoiré and Chatè, 2008)"""
    rnd = number_neighbors*eta * np.exp(1j*np.random.uniform(-np.pi, np.pi, size=n))
    do = np.angle(sum_neighbors+rnd)
    return do


_noise_db = {'scalar': noise_scalar,
             'vectorial': noise_vectorial}

class Vicsek(object):
    """
    Base Vicsek model simulation backend.

    Parameters
    ----------
    system: atooms system
                    `atooms` system to be evolved during the simulation.
    eta: 	float
                    Noise amplitude.
    v0: 	float
                    Velocity module.
    noise: 	{'scalar', 'vectorial'}, default 'vectorial'
                    Orientation update method. Available methods are `scalar`, which employs the scalar noise discussed in Vicsek et al, 1995; `vectorial` which employs the vectorial noise discussed in Grégoiré and Chatè, 2008.
    radius: float, default 1.0
                    Interaction radius.
    deltat: float, default 1.0
                    Time step.
    """

    def __init__(self, system, eta, v0, noise='vectorial', radius=1.0, deltat=1.0):
        self.system = system
        self.eta = eta
        self.v0 = v0
        self.deltat = deltat
        self.radius = radius
        # Setup neighbor related variables
        self.neighbors = None
        self.sum_neighbors = None
        self.number_neighbors = None

        # Set noise
        if noise in _noise_db:
            self.noise = _noise_db[noise]
        else:
            assert hasattr(noise, '__call__'), f'noise must be in {list(_noise_db.keys())} or callable'
            self.noise = noise

    def __str__(self):
        return f"""
		backend: Vicsek model
		algorithm: {self.noise}
		timestep: {self.deltat}
"""

    def _fold(self, method='f90'):
        """
        Fold self into central cell.
        View-based fork of atooms.system.particle folding routine
        """
        pos = self.system.view('pos', order='F')
        npart = len(self.system.particle)
        ndim = len(self.system.cell.side)
        if method == 'python':
            # Setup Fortran ordered arrays
            center = np.ndarray(shape=(ndim, npart), order='F', dtype=np.float64)
            center[:, :] = self.system.cell.center[:, None]
            side = np.ndarray(shape=(ndim, npart), order='F', dtype=np.float64)
            side[:, :] = self.system.cell.side[:, None]

            # Move the center to 0 when cell isn't centered in 0
            if not np.all(self.system.cell.center == 0.):
                pos -= center
                pos[:] = pos - np.rint(pos/side)*side
                pos += center
            else:
                pos[:] = pos - np.rint(pos/side)*side
            return self
        elif method == 'f90':
            _f90.fold(pos, self.system.cell.center, self.system.cell.side)

    def run(self, steps):
        """
        Evolve the system, as prescribed by `atooms.simulation.core.Simulation` class.  

        User defined orientation update methods can be provided via `self.neighbors` class variable. 
        """
        # Setup arrays (get views on atooms.system arrays)
        positions = self.system.view('pos', order='F')
        orientations = self.system.view('orientation', order='F')
        velocities = self.system.view('velocity', order='F')
        box = self.system.cell.side

        # Instantiate default neighbor list
        if self.neighbors == None:
            from neighbors import VicsekNeighbors
            self.neighbors = VicsekNeighbors(self.system, method='kdtree')

        # Main loop
        for i in range(steps):
            # Get sum of neighbors of each particle, its number of neighbors and timer data
            self.sum_neighbors, self.number_neighbors = self.neighbors.compute(box, positions, orientations)

            # Compute orientations according to noise kind specified by user
            orientations[:] = self.noise(orientations, self.number_neighbors,
                                         self.sum_neighbors, self.eta, len(self.system.particle))

            # Update velocities
            dv = np.asarray([self.v0*np.cos(orientations),
                             self.v0*np.sin(orientations)])
            velocities[:, :] = dv

            # Update positions
            dq = dv*self.deltat
            positions += dq

            # Apply PBC
            self._fold()
