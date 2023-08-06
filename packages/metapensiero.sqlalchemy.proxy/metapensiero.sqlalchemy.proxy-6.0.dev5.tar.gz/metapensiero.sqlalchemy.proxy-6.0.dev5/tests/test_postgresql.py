# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- PG specific tests
# :Created:   sab 24 ott 2015 12:52:33 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015, 2016, 2017, 2018, 2020, 2021, 2022, 2023 Lele Gaifax
#

import datetime
import os
import uuid

import pytest
from psycopg2.extras import DateRange
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sapg

from metapensiero.sqlalchemy.proxy.core import ProxiedQuery
from metapensiero.sqlalchemy.proxy.orm import ProxiedEntity
from metapensiero.sqlalchemy.proxy.filters import extract_filters
from metapensiero.sqlalchemy.proxy.utils import SQLALCHEMY_VERSION

if SQLALCHEMY_VERSION > (1, 4):
    from sqlalchemy.orm import declarative_base
else:
    from sqlalchemy.ext.declarative import declarative_base


def __getattr__(name):
    if name == 'SA_URI':
        # See .gitlab-ci.yml and Justfile
        pg_host = os.getenv('POSTGRES_HOST', 'localhost')
        pg_port = os.getenv('POSTGRES_PORT', '65432')
        pg_dbname = os.getenv('POSTGRES_DB', 'mp_sa_proxy_test')
        pg_user = os.getenv('POSTGRES_USER', 'proxy')
        pg_pwd = os.getenv('POSTGRES_PASSWORD', 'proxy')

        dburi = 'postgresql://'
        if pg_user and pg_pwd:
            dburi += f'{pg_user}:{pg_pwd}@'
        return dburi + f'{pg_host}:{pg_port}/{pg_dbname}'

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


SQLFUNC = """\
CREATE OR REPLACE FUNCTION bigintfunc()
RETURNS bigint AS $$

SELECT 1234567890::bigint * 1234567890::bigint

$$ LANGUAGE sql
"""

metadata = sa.MetaData()

if SQLALCHEMY_VERSION > (2, 0):
    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        metadata = metadata
else:
    from sqlalchemy.orm import declarative_base

    Base = declarative_base(metadata=metadata)


class Product(Base):
    __tablename__ = 'products'

    id = sa.Column(sapg.UUID(as_uuid=True), primary_key=True,
                   info=dict(label='id', hint='the product id'))
    brand = sa.Column(sa.String(64),
                      info=dict(label='brand', hint='the product brand'))
    description = sa.Column(sapg.HSTORE,
                            info=dict(label='description', hint='the product description'))
    other_description = sa.Column(sa.UnicodeText(),
                                  info=dict(label='other description',
                                            hint='alternative description'))
    availability = sa.Column(sapg.DATERANGE,
                             info=dict(label='availability', hint='period of availability'))
    quantity = sa.Column(sa.BigInteger,
                         info=dict(label='quantity', hint='items in store'))
    delivery = sa.Column(sa.Interval,
                         info=dict(label='delivery', hint='max delivery time'))
    details = sa.Column(sapg.JSONB(),
                        info=dict(label='DETS', hint='arbitrary details'))


def PUUID(s):
    return uuid.uuid3(uuid.NAMESPACE_OID, s)

@pytest.fixture(scope='module')
def sa_session(sa_SessionMaker, sa_engine):
    metadata.create_all(sa_engine)

    with sa_SessionMaker() as sas:
        sas.execute(sa.text(SQLFUNC))

        p = Product(id=PUUID('frizione'), brand='Allga San®',
                    description={'it': 'Frizione', 'de': 'Einreibung'},
                    other_description='Lorem ipsum')
        sas.add(p)

        p = Product(id=PUUID('orologio'), brand='Breitling',
                    description={'it': 'Orologio', 'en': 'Watch'})
        sas.add(p)

        p = Product(id=PUUID('fragole'), brand='Km0',
                    description={'it': 'Fragole', 'en': 'Strawberries'},
                    availability=DateRange(datetime.date(2017, 3, 23),
                                           datetime.date(2017, 4, 24)))
        sas.add(p)

        sas.commit()

        yield sas

    metadata.drop_all(sa_engine)


@pytest.mark.parametrize('column,args,expected_snippet', [
    (Product.__table__.c.description['it'],
     dict(filter_col='description', filter_value='~=bar'),
     ' LIKE '),
    (Product.__table__.c.availability,
     dict(filter=[dict(property='availability', value=datetime.date(2017, 4, 1))]),
     ' @> '),
])
def test_operators(column, args, expected_snippet):
    conds = extract_filters(args)
    assert len(conds) == 1
    cond = conds[0]
    filter = cond.operator.filter(column, cond.value)
    assert expected_snippet in str(filter)


def test_filters(sa_session):
    proxy = ProxiedEntity(Product)

    res = proxy(sa_session, filters=[dict(property='availability',
                                   value=datetime.date(2017, 4, 1))])
    assert res[0].description['it'] == 'Fragole'


def test_sort_1(sa_session):
    proxy = ProxiedEntity(Product)

    res = proxy(sa_session)
    assert res


def test_sort_2(sa_session):
    t = Product.__table__

    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.id, t.c.description['it']))
    else:
        proxy = ProxiedQuery(sa.select([t.c.id, t.c.description['it']]))

    res = proxy(sa_session, sort_col='description')
    assert res[0][1] < res[1][1]

    res = proxy(sa_session, sort_col='description', sort_dir='DESC')
    assert res[0][1] > res[1][1]


def test_select_from_function(sa_session):
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(sa.literal_column('g'))
                             .select_from(sa.text('generate_series(1,10) as g')))
    else:
        proxy = ProxiedQuery(sa.select([sa.literal_column('g')],
                                       from_obj=sa.text('generate_series(1,10) as g')))

    proxy(sa_session, sort_col='g', filter_by_g=2)

    # Non existing field
    proxy(sa_session, sort_col='g', filter_by_foo=2)


def test_bigint_metadata(sa_session):
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.quantity))
    else:
        proxy = ProxiedQuery(sa.select([t.c.quantity]))

    res = proxy(sa_session, result=False, metadata='metadata')
    assert res['metadata']['fields'][0]['type'] == 'integer'


def test_bigint_function_metadata(sa_session):
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(sa.func.bigintfunc(type_=sa.BigInteger)))
    else:
        proxy = ProxiedQuery(sa.select([sa.func.bigintfunc(type_=sa.BigInteger)]))

    res = proxy(sa_session, result=False, metadata='metadata')
    assert res['metadata']['fields'][0]['type'] == 'integer'


def test_interval_metadata(sa_session):
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.delivery))
    else:
        proxy = ProxiedQuery(sa.select([t.c.delivery]))

    res = proxy(sa_session, result=False, metadata='metadata')
    assert res['metadata']['fields'][0]['type'] == 'interval'


def test_brand_metadata(sa_session):
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.brand))
    else:
        proxy = ProxiedQuery(sa.select([t.c.brand]))

    res = proxy(sa_session, result=False, metadata='metadata')
    fmeta = res['metadata']['fields'][0]
    assert fmeta['name'] == 'brand'
    assert fmeta['type'] == 'string'
    assert fmeta['length'] == 64


def test_description_metadata(sa_session):
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.description['foo']))
    else:
        proxy = ProxiedQuery(sa.select([t.c.description['foo']]))

    res = proxy(sa_session, result=False, metadata='metadata')
    fmeta = res['metadata']['fields'][0]
    assert fmeta['name'] == 'description'
    assert fmeta['type'] == 'string'
    assert 'length' not in fmeta
    assert fmeta['label'] == 'description'


def test_other_description_metadata(sa_session):
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.other_description))
    else:
        proxy = ProxiedQuery(sa.select([t.c.other_description]))

    res = proxy(sa_session, result=False, metadata='metadata')
    fmeta = res['metadata']['fields'][0]
    assert fmeta['name'] == 'other_description'
    assert fmeta['type'] == 'text'
    assert 'length' not in fmeta
    assert fmeta['label'] == 'other description'


def test_details_metadata(sa_session):
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.details['foo']))
    else:
        proxy = ProxiedQuery(sa.select([t.c.details['foo']]))

    res = proxy(sa_session, result=False, metadata='metadata')
    fmeta = res['metadata']['fields'][0]
    assert fmeta['name'] == 'details'
    assert fmeta['type'] == 'string'
    assert 'length' not in fmeta
    assert fmeta['label'] == 'DETS'
