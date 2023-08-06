COnstrained Geometries simulate External Force
==============================================

COGEF is an ASE based module which contains tools for simulating force-induced
bond-breaking reactions based on the COnstrained Geometries simulate External
Force (COGEF) method (Beyer, M. K. J. Chem. Phys. 2000, 112, 7307).
The initial version was developped by Oliver Brügner.

Website: https://cogef.gitlab.io/cogef


Requirements
------------

* Python_ 3.7
* NumPy_ 1.16
* ASE_ 3.18


Installation
------------

* Installation with pip::

  $ python3 -m pip install --upgrade pip
  $ python3 -m pip install --upgrade ase
  $ python3 -m pip install --upgrade ase-cogef

* Developer installation with git (when there is no need for merge requests)

  Clone the repository (you need ssh keys)::

    $ git clone git@gitlab.com:cogef/cogef.git

  or if you do not have and do not want to create ssh keys, use::

    $ git clone https://gitlab.com/cogef/cogef.git

  In any case, add ``cogef`` folder to the $PYTHONPATH environment variable.
  Add ``cogef/bin`` folder to the $PATH environment variable.

* Developer installation with git (when you may want to create merge requests)

  Go to https://gitlab.com/cogef/cogef and fork the project, then clone it
  with your gitlab account name (you need ssh keys)::

    $ git clone git@gitlab.com:your-user-name/cogef.git

  Add ``cogef`` folder to the $PYTHONPATH environment variable.
  Add ``cogef/bin`` folder to the $PATH environment variable.

Testing
-------

Please run the tests::

  $ cogef test


Contact
-------

Functional Nanosystems group::

  https://www.functional-nanosystems.uni-freiburg.de/People/PDWalter

Contact::

  mcoywalter@gmail.com


Example
-------

See https://cogef.gitlab.io/cogef/tutorials/cogef.

Coverage
--------

See https://cogef.gitlab.io/cogef/coverage-html.

.. _Python: http://www.python.org/
.. _NumPy: http://docs.scipy.org/doc/numpy/reference/
.. _ASE: http://wiki.fysik.dtu.dk/ase
