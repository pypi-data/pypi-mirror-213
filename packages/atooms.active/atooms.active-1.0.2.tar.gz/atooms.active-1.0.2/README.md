# active 

[![license](https://img.shields.io/pypi/l/atooms.svg)](https://en.wikipedia.org/wiki/GNU_General_Public_License)
[![pipeline status](https://framagit.org/activematter/active/badges/master/pipeline.svg)](https://framagit.org/activematter/active/-/commits/master)
[![coverage report](https://framagit.org/activematter/active/badges/master/coverage.svg)](https://framagit.org/activematter/active/-/commits/master)

**active** is a simulation backend for [atooms](https://framagit.org/atooms/atooms), a high-level framework for particle-based simulations. This backend implements active matter systems, e.g. the Vicsek model as described in [Vicsek _et al._ (1995)](https://doi.org/10.1103/PhysRevLett.75.1226) and in [Grégoire _and_ Chaté (2004)](https://doi.org/10.1103/PhysRevLett.92.025702).

## Quick start
Here we have a simulation of an active matter system based on the Vicsek model. First of all, we need to setup a 2D _atooms_ system.

```python
import numpy
import atooms
from atooms.system import System

n = 200
dim = 2
system = System(N = n)
system.cell = [32. for i in range(dim)]
for p in system.particle:

	p.orientation = numpy.random.uniform(-numpy.pi,numpy.pi)
	p.position = [L*numpy.random.uniform() for i in range(dim)]
	p.fold(system.cell)
```

Having done so, we can run a simple Vicsek model simulation as follows. We need to provide the system size _n_, its noise amplitude _eta_, velocity _v0_, and density _rho_. 
```python
from atooms.active.vicsek import Vicsek
from atooms.active.neighbors import VicsekNeighbors
from atooms.simulation import Simulation

eta = 0.4
v0 = 0.5
rho = 0.5

backend = Vicsek(system, eta, v0, noise='vectorial')
neighbors = VicsekNeighbors(system, method='kdtree')
bck.neighbors = neighbors

Simulation(backend).run(10)
```

This simulation employs the so-called 'vectorial' noise implementation (discussed in Grégoire and Chaté) and the _scipy_-based kD-tree neighbor search algorithm.

A basic API is also available. We can run the same simulation as follows

```python
from atooms.active.api import vm

vm('input.xyz', 'output.xyz', npart=2048, eta=0.4, rho=2.0, nsteps=1000, config_number=10)
```

or, from the command line 

```python
api.py input.xyz output.xyz --npart 2048 --eta 0.4 --rho 2.0 --nsteps 1000 --config-number 10
```

## Features

- Seamless integration with _atooms_ framework
- Various nearest neighbors algorithms available
- Easy extension to new variations of the Vicsek model
- Support for user-provided code

## Dependencies

- gfortran 11.3.0 
- python 3.10
	- argh  0.28.1
	- atooms 3.17.0
	- f2py-jit 0.9.2
	- numpy
	- scipy (optional)
 
## Documentation

Check out the [tutorial](https://atooms.frama.io/active/tutorial) for more detailed examples and the [public API](https://atooms.frama.io/active/api/atooms/active/) for more detail.

## Installation
From the code repository:

```
git clone https://framagit.org/atooms/active.git
cd active
make install
```

## Authors

Iacopo Ricci: https://iricci.frama.io/

Huge thanks to Prof. Daniele Coslovich for his careful supervision and for his profound insights.
