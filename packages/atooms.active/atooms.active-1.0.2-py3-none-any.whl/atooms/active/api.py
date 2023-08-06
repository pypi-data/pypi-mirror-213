"""
Basic API for active matter simulations
"""

import os
import numpy
import random
import logging
import csv

import argh
import numpy as np
from atooms.core.utils import setup_logging, mkdir, rmf
from atooms.simulation import Simulation
from atooms.trajectory import Trajectory, TrajectoryXYZ
from atooms.simulation.observers import write_trajectory, write, Scheduler

try:
    from vicsek import Vicsek
    from neighbors import VicsekNeighbors
except:
    from atooms.active.vicsek import Vicsek
    from atooms.active.neighbors import VicsekNeighbors

# Utilities


def _clear_logging():
    import logging
    log = logging.getLogger()
    for h in log.handlers[-2:]:
        log.removeHandler(h)

def _initialize_system(dim, L, npart, file_inp, load=False, save=False):
    """
    System initialization.
    The system can be generated on the spot, loaded from an input file or saved to disk
    """
    # TODO: move to utilities module
    # Import pkgs
    from atooms.system import System
    from atooms.system.cell import Cell

    # Set input trajectory file path
    input_file = os.path.join(os.path.dirname(__file__), file_inp)

    if (load == True and os.path.exists(input_file) == True):
        # Load system from file (file exists)
        logging.info("Load starting config from file")
        with TrajectoryXYZ(input_file, 'r') as th:
            system = th[0]
    elif (load == True and os.path.exists(input_file) == False):
        # Load system from file (file doesn't exist)
        raise Exception('Failed to load config from file.')
    elif not load:
        # Initialize system from scratch
        system = System(N=npart)
        system.cell = Cell(np.ones(dim)*L)
        # TODO: build system in place
        for p in system.particle:
            p.position = [L*np.random.uniform() for i in range(dim)]
            p.velocity = np.zeros(dim)
            p.orientation = np.random.uniform(-np.pi, np.pi)
            p.radius = None
            # apply PBC - slow, but it's just one call
            p.fold(system.cell)

    if (save and not load):
        # Save to file
        logging.info("Save starting config to file")
        logging.info("Existing start_traj.xyz will be overwritten")
        with TrajectoryXYZ(input_file, 'w') as th:
            th.variables = ['pos', 'orientation', 'velocity']
            th.write(system)
    elif (save and load):
        raise Exception("Cannot load and save system at the same time. Set load or save to False.")

    return system

def _random_choice_id(length=8, seed=None):
    """
    Generate UniqueIDentifier.
    RNG can be independent of global seed set by random.seed or numpy.random.seed
    """
    # TODO: move to utilities module (it can be useful elsewhere)
    import string
    rng = random.Random(seed)
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(rng.choices(alphabet, k=length))

def _order_parameter(sim, v0):
    # TODO: get view
    velocity = sim.system.dump('velocity')
    norm = np.linalg.norm(np.sum(velocity, axis=1))/len(sim.system.particle)
    return norm/v0

# API


@argh.arg('--load', action='store_true')
@argh.arg('--save', action='store_true')
def vm(file_inp, file_out, load=False, save=False, noise='vectorial',
       neighbors='kdtree', dim=2, npart=2048, eta=0.4, rho=2., v0=1.,
       nsteps=1000, checkpoint_interval=0, config_number=0, verbose=False,
       seed=1, seed_inp='data/seed.txt', block='', restart=False, dry=False, log=True):
    """
    Simple API with logging facilities for Vicsek model simulations.

    Parameters
    ----------
    file_inp:               string
                            Input file path.
    file_out:               string
                            Output file path.
    load:                   bool, default False
                            Enable loading of starting trajectory from `file_inp`
    save:                   bool, default False
                            Enable saving of starting trajectory to `file_out`
    noise:                  string, default 'vectorial'
                            Orientation update method. See `active.vicsek` module.
    neighbors:              string, default `kdtree`
                            Fixed radius neighhbor search algorithm. Akin to `method` parameter in `active.neighbors`.
    dim:                    int, default 2
                            System dimensionality.
    npart:                  int, default 2048
                            Number of particles.
    eta:                    float, default 0.4
                            Noise amplitude
    rho:                    float, default 2.0
                            Particle number density.
    v0:                     float, default 1.0
                            Velocity module.
    nsteps:                 int, default 1000
                            Number of simulation steps.
    checkpoint_interval:    int, default 0
                            Save checkpoint trajectory at selected interval.
    config_number:          int, default 0
                            Number of trajectories to save.
    verbose:                bool, default False
                            Enable verbose logging.
    seed:                   int, default 1
                            Seed for the random number generator.
    seed_inp:               string, default 'data/seed.txt'
                            Seed file path. It has priority over `seed` variable.
    restart:                bool, default False
                            Enable simulation restarting from checkpoint.
    dry:                    bool, default False
                            Enable dry run. No simulation is performed.
    log:                    bool, default True
                            Enable system parameters logging in path given by `file_out + '.param'`.
    """

    # Initialize seed
    if os.path.exists(seed_inp):
        f = open(seed_inp, 'r')
        seed = int(f.read())
    random.seed(seed)
    numpy.random.seed(seed)

    # Initialize directory structure
    mkdir(os.path.dirname(file_out))

    # Always log to file
    if not restart:
        rmf(file_out + '.log')
    setup_logging(level=20, filename=file_out + '.log')
    if verbose:
        setup_logging(level=20)

    # Build system or read initial state, depending on user action
    L = np.sqrt(npart/rho)
    system = _initialize_system(dim, L, npart, file_inp, load=load, save=save)

    # Simulation backend
    bck = Vicsek(system, eta, v0, noise=noise)

    # Neighbor search method
    # TODO: evaluate whether to keep or remove pseudo-factory VicsekNeighbors
    # by moving method selection over here
    neighs = VicsekNeighbors(system, method=neighbors)
    bck.neighbors = neighs

    # Simulation
    sim = Simulation(bck, output_path=file_out, steps=nsteps,
                     enable_speedometer=True, restart=restart,
                     checkpoint_interval=checkpoint_interval)
    sim.checkpoint_variables = ['position', 'orientation', 'velocity']

    # Trajectory class instantiation with proper metadata
    trajectory = TrajectoryXYZ(file_out, mode='w')
    trajectory.metadata = {'eta': eta, 'v0': v0, 'neighbors': neighbors}

    # Writing trajectory file
    if config_number == 0:
        if len(block) > 0:
            sim.add(write_trajectory, Scheduler(block=[int(_) for _ in block.split(',')]),
                    variables=['position', 'orientation', 'velocity'],
                    trajectory=trajectory)
    else:
        sim.add(write_trajectory, Scheduler(calls=config_number),
                variables=['position', 'orientation', 'velocity'],
                trajectory=trajectory)

    # Get order parameter
    # TODO: evaluate whether to move in postprocessing or to keep in API;
    # it's a useful measure of how "correct" the simulation is at a glance

    # TODO: fix write to file - cbk tuple doesn't work properly
    # cbk = ('phi', _order_parameter)
    # sim.add(write, Scheduler(calls=config_number), cbk, suffix='phi')

    # Create/update parameter log
    if log:
        uuid = _random_choice_id(length=16)
        with open(file_out+'.param', 'a') as f:
            write = csv.writer(f)
            # Add header if file is empty
            if os.stat(data_log).st_size == 0:
                write.writerow(['npart', 'rho', 'eta', 'v0', 'nsteps', 'noise', 'seed', 'uuid'])
            write.writerow([npart, rho, eta, v0, nsteps, noise, seed, uuid])

    # Run
    if not dry:
        sim.run()
        _clear_logging()

    return sim


if __name__ == '__main__':
    argh.dispatch_command(vm)
