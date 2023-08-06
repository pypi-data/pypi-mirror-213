import numpy as np
from pathlib import Path

from ase.neb import NEB, interpolate
from ase import io
from ase.autoneb import AutoNEB
from ase.optimize import BFGS
from ase.parallel import world

from cogef.neb import write_trajectory


class Fixed2DNEB:
    """NEB class for Fixed2D"""
    def __init__(self, propagator, nebcls=NEB, nebkwargs={}):
        self.prop = propagator
        self.nebcls = nebcls
        self.nebkwargs = nebkwargs

        clsname = nebcls.__name__.lower()
        self.fname = Path(self.prop.name) / (clsname + '.traj')
        self.frestart = Path(self.prop.name) / (clsname + '_restart.traj')

    def energies(self):
        if self.fname.is_file():
            images = [image for image in io.Trajectory(self.fname)]
        else:
            if self.frestart.is_file():
                images = [self.prop.initialize(image)
                          for image in io.Trajectory(self.frestart)]
            else:
                # initialize inner images and delete propagator constraint
                images = self.prop.images

                # XXX NEB does not like changing unit cells -> fix there ?
                cell = images[-1].cell  # assume last to be the largest

                assert self.prop.initialize is not None
                for j, image in enumerate(self.prop.images[:-1]):
                    self.prop.remove_my_constraint(image)

                    images[j] = self.prop.initialize(image)

                    # XXX NEB does not like changing unit cells
                    # -> fix there ?
                    images[j].cell = cell

            def write_restart_file(images):
                write_trajectory(self.frestart, images)

            if self.nebcls == AutoNEB:
                prefix = Path(self.prop.name) / 'autoneb' / 'neb'
                prefix.parent.mkdir(exist_ok=True)

                additional = self.nebkwargs.pop('additional', 5)

                kwargs = {
                    'prefix': prefix,
                    'optimizer': BFGS,
                    'n_simul': 1,
                    'fmax': self.prop.fmax,
                    'k': 0.5,
                    'n_max': len(images) + additional,
                    'parallel': False,
                    }
                kwargs.update(self.nebkwargs)

                for ii, image in enumerate(images):
                    # XXX why do we need this and does it hurt?
                    image.get_potential_energy()
                    with io.Trajectory(
                            f'{prefix}{ii:03}.traj', 'w') as traj:
                        traj.write(image)

                def attach_calculators(images):
                    for i, image in enumerate(images):
                        images[i] = self.prop.initialize(image)

                autoneb = AutoNEB(attach_calculators,
                                  **kwargs)
                autoneb.run()

                images = autoneb.all_images

            else:  # we assume "normal" NEB
                kwargs = {
                    'method': 'eb',
                    'allow_shared_calculator': True}
                kwargs.update(self.nebkwargs)

                neb = self.nebcls(images, **kwargs)
                optimizer = self.prop.optimizer(neb)
                optimizer.attach(write_restart_file, 1, images)
                optimizer.run(self.prop.fmax)

            with io.Trajectory(self.fname, 'w') as traj:
                for image in images:
                    traj.write(image)

        return np.array([image.get_potential_energy()
                         for image in images])

    def refine(self, n, i=None):
        """Refine neb trajectory

        n: number of images to introduce left and right around chosen i
        i: index or None, maximum is used if None

        Removes converged neb and changes length of the restart file.
        """
        assert self.fname.is_file(), f'{self.fname} must exist'

        images = [image for image in io.Trajectory(self.fname)]
        energies = np.array([image.get_potential_energy()
                             for image in images])
        if world.rank == 0:
            self.fname.unlink()
        world.barrier()

        if i is None:
            imax = energies.argmax()
        else:
            imax = i

        # add images with larger indices
        for i in range(n):
            newimage = self.prop.initialize(images[imax + 1].copy())
            images.insert(imax + 1, newimage)
        interpolate(images[imax:imax + n + 2], apply_constraint=False)

        # add images with smaller indices
        for i in range(n):
            newimage = self.prop.initialize(images[imax - 1].copy())
            images.insert(imax, newimage)
        interpolate(images[imax - 1:imax + n + 1], apply_constraint=False)

        # write restart file
        with io.Trajectory(self.frestart, 'w') as traj:
            for image in images:
                image.get_forces()
                traj.write(image)
