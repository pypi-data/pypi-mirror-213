# Copyright (C) 2016-2019
# See accompanying license files for details.

import sys
import os
from subprocess import Popen
from os.path import abspath, dirname, join, isdir
from pathlib import Path

from ase.utils import import_module, search_current_git_hash


testdir = Path(__file__).parent
datadir = (testdir / 'data').resolve()


def print_cogef_info():
    versions = []
    for name in ['cogef']:
        try:
            module = import_module(name)
        except ImportError:
            versions.append((name, 'no'))
        else:
            # Search for git hash
            githash = search_current_git_hash(module)
            if githash is None:
                githash = ''
            else:
                githash = '-{:.10}'.format(githash)
            versions.append((name + '-' + module.__version__ + githash,
                             module.__file__.rsplit(os.sep, 1)[0] + os.sep))

    for a, b in versions:
        print('{:25}{}'.format(a, b))


def main():
    assert (sys.argv[1] == 'test'), \
        'Command "cogef test" only available.'

    directory = join(dirname(dirname(abspath(__file__))), 'test')
    assert isdir(directory), 'Cannot find test folder: ' + directory
    sys.argv.append(directory)

    print_cogef_info()

    pytest_args = sys.argv[2:]

    # We run pytest through Popen rather than pytest.main().
    #
    # This is because some ASE modules were already imported and
    # would interfere with code coverage measurement.
    # (Flush so we don't get our stream mixed with the pytest output)
    sys.stdout.flush()
    proc = Popen([sys.executable, '-m', 'pytest'] + pytest_args,
                 cwd=str(testdir))
    exitcode = proc.wait()
    sys.exit(exitcode)
