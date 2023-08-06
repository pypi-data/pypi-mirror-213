from pathlib import Path
from typing import List, Union

from ase.neb import NEB
from ase import io, Atoms

from . import COGEF1D


def write_trajectory(filename: Union[Path, str],
                     images: List[Atoms]) -> None:
    with io.Trajectory(filename, 'w') as traj:
        for image in images:
            traj.write(image)


def apply_neb(cogef: COGEF1D,
              trajname: str = 'neb.traj',
              restartname: str = 'neb_restart.traj') -> List[Atoms]:
    """Apply NEB on the images"""
    # get a copy of all images
    images = [cogef.images[0]]
    for image in cogef.images[1:-1]:
        atoms = cogef.initialize(image.copy())
        cogef.remove_my_constraint(atoms)
        images.append(atoms)
    images.append(cogef.images[-1])

    def write_restart_file(images):
        filename = Path(cogef.name) / restartname
        write_trajectory(filename, images)

    neb = NEB(images)
    opt = cogef.optimizer(neb, logfile=cogef.txt)
    opt.attach(write_restart_file, 1, images)
    opt.run(fmax=cogef.fmax)

    filename = Path(cogef.name) / trajname
    write_trajectory(filename, neb.images)

    return neb.images
