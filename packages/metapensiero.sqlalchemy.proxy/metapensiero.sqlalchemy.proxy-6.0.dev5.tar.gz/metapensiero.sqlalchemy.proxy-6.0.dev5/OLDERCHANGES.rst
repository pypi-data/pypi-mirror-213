Older changes
-------------

5.14 (2020-04-25)
~~~~~~~~~~~~~~~~~

* Silently assume ASCending direction in sort criteria


5.13 (2020-02-08)
~~~~~~~~~~~~~~~~~

* Remove deprecated call to pyramid.i18n.get_localizer()


5.12 (2018-11-06)
~~~~~~~~~~~~~~~~~

* Fix deprecated import of abstract classed directly from the collections module


5.11 (2018-09-09)
~~~~~~~~~~~~~~~~~

* Fix deprecation warning related to collections abstract classes import


5.10 (2018-07-01)
~~~~~~~~~~~~~~~~~

* Fix failure extracting metadata of a column associated to a Sequence


5.9 (2018-07-01)
~~~~~~~~~~~~~~~~

* Rename the ``async`` module to ``asyncio`` for Python 3.7 compatibility


5.8 (2018-04-13)
~~~~~~~~~~~~~~~~

* Align the async layer with latest changes related to ``CompoundSelect`` support, now almost
  complete


5.7 (2018-04-13)
~~~~~~~~~~~~~~~~

* Extend last fix to the Pyramid ``expose()`` decorator (yes, I know, I should *really* invest
  some time in writing some tests for that...)


5.6 (2018-04-12)
~~~~~~~~~~~~~~~~

* Handle ``CompoundSelect`` such as ``SELECT 'foo' UNION SELECT 'bar'``


5.5 (2018-04-09)
~~~~~~~~~~~~~~~~

* Fix... last fix :-|


5.4 (2018-04-09)
~~~~~~~~~~~~~~~~

* Fix regression that broke using a generator as an expose() function


5.3 (2018-03-15)
~~~~~~~~~~~~~~~~

* The Pyramid ``expose()`` decorator now forwards unrecognized keyword arguments to the proxy
  call


5.2 (2018-03-12)
~~~~~~~~~~~~~~~~

* Handle extraction of metadata from a ``BinaryExpression`` such as ``SELECT jsonfield['attr']``


5.1 (2018-03-08)
~~~~~~~~~~~~~~~~

* When a column has a *default* value, and it is directly computable (i.e. it is not a server
  side default), then extract it into its metadata


5.0 (2017-07-22)
~~~~~~~~~~~~~~~~

.. warning:: This release **breaks** backward compatibility in several ways!

* More versatile way to add/override basic metadata information (see
  ``register_sa_type_metadata()``)

* More versatile way to use different JSON library or encode/decode settings (see
  ``register_json_decoder_encoder()``): although the default implementation is still based on
  nssjson__, it is *not* required by default anymore at install time

* Basic metadata changed:

  - the `width` slot for all fields is gone, it's more reasonably computed by the actual UI
    framework in use: it was rather arbitrary anyway, and set to ``length * 10`` for String
    columns

  - the `length` slot is present only for ``String`` columns

  - the `type` slot now basically follows the SQLAlchemy nomenclature, in particular:

    Integer
      is now ``integer`` instead of ``int``

    BigInteger
      is now ``integer``, instead of ``int`` with an arbitrarily different ``width`` than the
      one used for Integer

    Numeric
      is now ``numeric`` instead of ``float``

    DateTime
      is now ``datetime`` instead of ``date`` with `timestamp` set to ``True``

    Time
      is now ``time`` instead of ``date`` with `time` set to ``True``

    Interval
      is now ``interval`` instead of ``string`` with ``timedelta`` set to ``True``

    Text
      is now ``text`` instead of ``string`` with an arbitrary `width` of ``50``

    UnicodeText
      is now ``text```

    Unicode
      is now ``string``

  - the `format` slot for DateTime, Date and Time fields is gone, as it was ExtJS specific

__ https://pypi.python.org/pypi/nssjson


4.8 (2017-06-17)
~~~~~~~~~~~~~~~~

* Use a tuple instead of a list for the `foreign_keys` slot in metadata, and for the
  `primary_key` too when it is composed by more than one column


4.7 (2017-05-18)
~~~~~~~~~~~~~~~~

* Properly recognize SA Interval() columns


4.6 (2017-05-08)
~~~~~~~~~~~~~~~~

* Handle big integers in metadata information


4.5 (2017-04-10)
~~~~~~~~~~~~~~~~

* Fix a crash when applying a filter on a non-existing column in a statement selecting from a
  function


4.4 (2017-04-01)
~~~~~~~~~~~~~~~~

* Rename filter operator ``CONTAINED`` to ``CONTAINS``, and reimplement it to cover different
  data types, in particular PostgreSQL's ranges


4.3 (2017-03-22)
~~~~~~~~~~~~~~~~

* Minor tweak, no externally visible changes


4.2 (2017-03-10)
~~~~~~~~~~~~~~~~

* Reduce clutter, generating a simpler representation of Operator and Direction enums


4.1 (2017-02-13)
~~~~~~~~~~~~~~~~

* Fix an oversight in Filter tuple slots positions, to simplify Filter.make() implementation


4.0 (2017-02-13)
~~~~~~~~~~~~~~~~

* From now on, a Python3-only package

* Backward incompatible sorters and filters refactor, to make interaction easier for code using
  the library

* Drop obsolete Pylons extension


3.6 (2017-01-11)
~~~~~~~~~~~~~~~~

* New Sphinx documentation

* Field's metadata now carries also information about foreign keys

* Handle literal columns in core queries


3.5 (2016-12-29)
~~~~~~~~~~~~~~~~

* Fix incompatibility issue with SQLAlchemy 1.1.x when using ORM


3.4 (2016-03-12)
~~~~~~~~~~~~~~~~

* Better recognition of boolean argument values, coming from say an HTTP channel as string
  literals

* Use tox to run the tests


3.3 (2016-02-23)
~~~~~~~~~~~~~~~~

* Handle the case when the column type cannot be determined


3.2 (2016-02-19)
~~~~~~~~~~~~~~~~

* Fix corner case with queries ordered by a subselect


3.1 (2016-02-07)
~~~~~~~~~~~~~~~~

* Fix metadata extraction of labelled columns on joined tables

* Adjust size of time fields and align them to the right


3.0 (2016-02-03)
~~~~~~~~~~~~~~~~

* Internal, backward incompatible code reorganization, splitting the main module into smaller
  pieces

* Handle corner cases with joined queries involving aliased tables


2.8 (2015-08-02)
~~~~~~~~~~~~~~~~

* Use py.test instead of nosetests

* Remove workaround to an async issue caused by a bug fixed in ``arstecnica.sqlalchemy.async``


2.7 (2015-07-16)
~~~~~~~~~~~~~~~~

* Reasonably working asyncio variant of ProxiedQuery (Python 3.4 only, and using the
  yet-to-be-released ``arstecnica.sqlalchemy.async``)


2.6 (2014-11-05)
~~~~~~~~~~~~~~~~

* Handle ``NULL`` in the multi-valued ``IN`` comparisons

* Minor doc tweaks, added request examples section to the README

* Honor both "filter" and "filters" request parameters


2.5 (2014-09-14)
~~~~~~~~~~~~~~~~

* Honor the "key" of the columns in ProxiedQuery result dictionaries


2.4 (2014-03-22)
~~~~~~~~~~~~~~~~

* Use nssjson instead of simplejson


2.3 (2014-02-28)
~~~~~~~~~~~~~~~~

* Explicitly require simplejson

* Improved test coverage

* Fix SQLAlchemy and_() usage


2.2 (2014-02-02)
~~~~~~~~~~~~~~~~

* Easier syntax to sort on multiple fields


2.1 (2014-01-19)
~~~~~~~~~~~~~~~~

* Fix TypeDecorators in compare_field()


2.0 (2013-12-23)
~~~~~~~~~~~~~~~~

* The generator function may yield a tuple with modified params and
  other conditions

* Simple Makefile with common recipes


1.9.6 (2013-12-12)
~~~~~~~~~~~~~~~~~~

* Encoding issue on package meta data


1.9.5 (2013-12-12)
~~~~~~~~~~~~~~~~~~

* First official release on PyPI


1.9.4 (2013-12-12)
~~~~~~~~~~~~~~~~~~

* Pyramid expose() can decorate a generator function too


1.9.3 (2013-08-04)
~~~~~~~~~~~~~~~~~~

* Use setuptools instead of distribute


1.9.2 (2013-06-09)
~~~~~~~~~~~~~~~~~~

* New replaceable ``extract_parameters(request)`` static method on
  Pyramid's `expose` decorator

* **Backward incompatible change**: fix handling of bindparams in
  ProxiedQuery, which shall be passed as a dictionary with the
  `params` keyword instead as of individual keywords

* Fix handling of SQLAlchemy custom types


1.9.1 (2013-04-17)
~~~~~~~~~~~~~~~~~~

* Fix and test handling of ORM queries

* Fix Pyramid exposure of ORM queries


1.9 (2013-04-08)
~~~~~~~~~~~~~~~~

* Minor adjustments for SQLAchemy 0.8

* Compatibility tweaks for Python 2.7 and Python 3.3

* Improved test coverage


1.8.7 (2013-03-18)
~~~~~~~~~~~~~~~~~~

* For backward compatibility check for “filters” too

* Ignore the filter condition if the comparison value is missing


1.8.6 (2013-03-08)
~~~~~~~~~~~~~~~~~~

* Use the ExtJS default name, “filter”, not the plural form, “filters”
  for the filter parameter


1.8.5 (2013-02-28)
~~~~~~~~~~~~~~~~~~

* Factor out the extraction of filtering conditions, so it can be used
  by other packages


1.8.4 (2013-01-28)
~~~~~~~~~~~~~~~~~~

* Field metadata information can be a callable returning the actual
  dictionary


1.8.3 (2013-01-26)
~~~~~~~~~~~~~~~~~~

* **Backward incompatible change**: pass the request also the the
  ``save_changes`` function, it may need it to determine if the user
  is allowed to make the changes


1.8.2 (2013-01-21)
~~~~~~~~~~~~~~~~~~

* More generic way of specifying an handler for non-GET request
  methods


1.8.1 (2013-01-09)
~~~~~~~~~~~~~~~~~~

* **Backward incompatible change**: pass the request to the adaptor
  function, it may need it to do its job


1.8 (2012-12-19)
~~~~~~~~~~~~~~~~

* SQLAlchemy 0.8 compatibility


1.7.12 (2012-11-17)
~~~~~~~~~~~~~~~~~~~

* Properly recognize TIME type


1.7.11 (2012-10-22)
~~~~~~~~~~~~~~~~~~~

* Fix exception


1.7.10 (2012-10-22)
~~~~~~~~~~~~~~~~~~~

* Small code tweaks


1.7.9 (2012-10-20)
~~~~~~~~~~~~~~~~~~

* Attempt to extract the primary key fields of a ProxiedQuery


1.7.8 (2012-10-19)
~~~~~~~~~~~~~~~~~~

* More versatile way of injecting the SA session maker


1.7.7 (2012-09-26)
~~~~~~~~~~~~~~~~~~

* Multicolumns sort


1.7.6 (2012-09-25)
~~~~~~~~~~~~~~~~~~

* Better error reporting


1.7.5 (2012-09-21)
~~~~~~~~~~~~~~~~~~

* Rework how filters are passed

* Emit more compact JSON


1.7.4 (2012-09-14)
~~~~~~~~~~~~~~~~~~

* Tweak the Pyramid ``expose`` to work on selectables


1.7.3 (2012-09-12)
~~~~~~~~~~~~~~~~~~

* New ``expose`` decorator for Pyramid


1.7.2 (2012-08-18)
~~~~~~~~~~~~~~~~~~

* Ability to skip a field, setting its metadata info to ``False``

* Extract the primary key fields of a ProxiedEntity


1.7.1 (2012-08-13)
~~~~~~~~~~~~~~~~~~

* Pyramid glue


1.7 (2012-08-08)
~~~~~~~~~~~~~~~~

* Drop cjson support


1.6 (2010-11-14)
~~~~~~~~~~~~~~~~

* Depend on distribute


1.5 (2010-08-04)
~~~~~~~~~~~~~~~~

* Handle bindparams


1.4 (2010-07-15)
~~~~~~~~~~~~~~~~

* Support filtering on boolean fields

* Better jsonification


1.3 (2010-04-06)
~~~~~~~~~~~~~~~~

* Support Interval

* Prefer metapensiero.webapp.cjson


1.2 (2010-01-30)
~~~~~~~~~~~~~~~~

* Support DateTime

* Restore the test suite


1.1 (2009-04-30)
~~~~~~~~~~~~~~~~

* Initial version, factored out from SoL 1.7
