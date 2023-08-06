from pathlib import Path
from ase import io
from cogef.efei import EFEIpair


def test_break_H4(H4):
    df = 0.1
    dmax = 2

    a1 = 1
    a2 = 2
    efei = EFEIpair(a1, a2)
    assert efei.name == f'efeipair_{a1}_{a2}'

    efei.images = [H4]

    # first run until maxsteps
    maxsteps = 10
    efei.scan(df, dmax=dmax, maxsteps=maxsteps)

    traj = io.Trajectory(Path(efei.name) / 'cogef.traj')
    assert len(traj) == maxsteps + 1

    # finish run
    efei.scan(df, dmax=dmax)

    traj = io.Trajectory(Path(efei.name) / 'cogef.traj')
    # all images should have only one constraint
    for image in traj[1:]:
        assert len(image.constraints) == 1
