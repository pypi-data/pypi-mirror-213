from pathlib import Path
from ase.parallel import world


def mkparent(filename, comm=world):
    """Check if parent directory is there and create if not"""
    path = Path(filename)
    if comm.rank == 0 and not path.parent.exists():
        path.parent.mkdir(parents=True)
    comm.barrier()


def insubdir(filename, directory):
    """Return path of filename in the directory if finanme is not absolute."""
    if Path(filename).absolute() != Path(filename):
        filename = Path(directory) / filename
    return Path(filename)
