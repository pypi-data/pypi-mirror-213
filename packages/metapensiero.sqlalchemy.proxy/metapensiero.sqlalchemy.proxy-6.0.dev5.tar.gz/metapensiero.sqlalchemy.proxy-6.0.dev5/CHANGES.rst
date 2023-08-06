Changes
-------

6.0.dev5 (2023-06-11)
~~~~~~~~~~~~~~~~~~~~~

* Drop support for SQLAlchemy 1.3.x in the test suite, exercise them against 1.4.x and 2.0.x,
  under both Python 3.10 and Python 3.11: note that this does not necessarily mean that the
  library won't work with Python 3.9 and SA 1.3.x


6.0.dev4 (2022-07-21)
~~~~~~~~~~~~~~~~~~~~~

* Another round against Python packaging tools madness, replace hatchling with pdm-pep517__

  __ https://pypi.org/project/pdm-pep517/


6.0.dev3 (2022-07-20)
~~~~~~~~~~~~~~~~~~~~~

* Fix RTD rendering


6.0.dev2 (2022-06-27)
~~~~~~~~~~~~~~~~~~~~~

* Fight with Python packaging tools idiosyncrasies, replace flit with hatchling__

  __ https://hatch.pypa.io/latest/config/build/#build-system


6.0.dev1 (unreleased)
~~~~~~~~~~~~~~~~~~~~~

* Renew development environment:

  - modernized packaging using `PEP 517`__ and flit__
  - replaced tox__ with nix__

  __ https://peps.python.org/pep-0517/
  __ https://flit.readthedocs.io/en/latest/
  __ https://tox.wiki/en/latest/
  __ https://nixos.org/guides/how-nix-works.html


6.0.dev0 (2021-10-17)
~~~~~~~~~~~~~~~~~~~~~

* Target Python 3.9+

* Do not emit ``length=1`` in the metadata of unlimited ``text`` fields

* Drop the asyncio variant of the proxies: if/when needs arise I shall reimplement them on top
  of new SA 1.4+ functionality


Previous changes are here__.

__ https://gitlab.com/metapensiero/metapensiero.sqlalchemy.proxy/-/blob/master/OLDERCHANGES.rst
