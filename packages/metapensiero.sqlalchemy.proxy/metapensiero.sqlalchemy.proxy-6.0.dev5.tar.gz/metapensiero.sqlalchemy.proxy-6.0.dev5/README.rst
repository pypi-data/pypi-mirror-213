.. -*- coding: utf-8 -*-
.. :Project:   metapensiero.sqlalchemy.proxy
.. :Created:   gio 30 apr 2009 10:01:20 CEST
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2009, 2010, 2012, 2013, 2014, 2016, 2017, 2018, 2020, 2022 Lele Gaifax
..

===============================
 metapensiero.sqlalchemy.proxy
===============================

Expose SQLAlchemy's queries and their metadata to a webservice
==============================================================

:version: 6
:author: Lele Gaifax <lele@metapensiero.it>
:license: GPLv3

This package contains a few utilities to make it easier applying some filtering to a stock
query and obtaining the resultset in various formats.

See latest documentation at https://metapensierosqlalchemyproxy.readthedocs.io/en/latest/

Tests suite
-----------

The tests suite may be executed with

::

   $ just check

The ``PostgreSQL`` unit requires an existing database called ``mp_sa_proxy_test`` with the
``hstore`` extension, and that the current user can access it without password::

   $ createdb mp_sa_proxy_test
   $ psql -c "create extension hstore;" mp_sa_proxy_test
