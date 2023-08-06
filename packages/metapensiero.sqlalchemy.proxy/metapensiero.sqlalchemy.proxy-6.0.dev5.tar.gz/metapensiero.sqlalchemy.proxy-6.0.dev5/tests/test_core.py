# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests for ProxiedQuery
# :Created:   mer 03 feb 2016 11:34:16 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2013, 2014, 2015, 2016, 2017, 2018, 2020, 2021, 2023 Lele Gaifax
#

from datetime import date

import pytest
from sqlalchemy import Date, desc, exists, func, literal_column, select, text
from sqlalchemy.exc import StatementError
from sqlalchemy.sql import bindparam

from metapensiero.sqlalchemy.proxy.core import ProxiedQuery
from metapensiero.sqlalchemy.proxy.utils import SQLALCHEMY_VERSION

from fixture import Complex, Pet, PairedPets, persons


def test_slots(sa_session):
    proxy = ProxiedQuery(persons.select())

    for slotname in ('success', 'message', 'count', 'metadata'):
        for value in (True, 'true', 'True'):
            for resultvalue in (False, 'false', 'False', 'None', ''):
                res = proxy(sa_session, **{'result': resultvalue, slotname: value})
                assert slotname in res
                assert resultvalue not in res

        for value in (False, 'false', 'False', 'None', ''):
            res = proxy(sa_session, **{'result': 'root', slotname: value})
            assert slotname not in res
            assert value not in res


def test_query_metadata(sa_session):
    proxy = ProxiedQuery(persons.select())

    res = proxy(sa_session, result=False, metadata='metadata')
    assert res['metadata']['primary_key'] == 'id'
    fields = res['metadata']['fields']
    assert [f['default'] for f in fields if f['name'] == 'smart'] == [True]
    assert [f['default'] for f in fields if f['name'] == 'somevalue'] == [42]

    proxy = ProxiedQuery(Complex.__table__.select())
    res = proxy(sa_session, result=False, metadata='metadata')
    assert res['metadata']['primary_key'] == ('id1', 'id2')

    proxy = ProxiedQuery(persons.select(), dict(id=False))
    res = proxy(sa_session, result=False, metadata='metadata')
    assert 'id' not in (f['name'] for f in res['metadata']['fields'])


def test_simple_select(sa_session):
    proxy = ProxiedQuery(persons.select())

    assert 'SELECT ' in str(proxy)

    res = proxy(sa_session, result='root',
                filter_col='lastname', filter_value="foo")
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    res = proxy(sa_session, result='root', only_cols='firstname,lastname',
                filter_col='lastname', filter_value="foo")
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    try:
        res = proxy(sa_session, result='root', only_cols='foo,bar',
                    filter_col='lastname', filter_value="foo")
    except ValueError:
        pass
    else:
        assert False, "Should raise a ValueError"

    res = proxy(sa_session, result='result',
                filter_col='lastname', filter_value="=foo")
    assert res['message'] == 'Ok'
    assert len(res['result']) == 0

    res = proxy(sa_session, result='result',
                filter_col='firstname', filter_value="Lele")
    assert res['message'] == 'Ok'
    assert len(res['result']) == 1

    res = proxy(sa_session, result='result',
                filters=[dict(property='title', value="perito%")])
    assert res['message'] == 'Ok'
    assert len(res['result']) == 0

    res = proxy(sa_session, result='result',
                filters=[dict(property='title', value="perito%", operator='STARTSWITH')])
    assert res['message'] == 'Ok'
    assert len(res['result']) == 0

    res = proxy(sa_session, result='result',
                fields='firstname', query="Lele")
    assert res['message'] == 'Ok'
    assert len(res['result']) == 1

    res = proxy(sa_session, persons.c.firstname == 'Lele', result='result')
    assert res['message'] == 'Ok'
    assert len(res['result']) == 1

    res = proxy(sa_session, persons.c.firstname == 'Lele', persons.c.lastname == 'Gaifax',
                result='result')
    assert res['message'] == 'Ok'
    assert len(res['result']) == 0

    res = proxy(sa_session, result='result', count='count',
                filter_by_firstname="Lele")
    assert res['message'] == 'Ok'
    assert len(res['result']) == res['count']

    for none in (None, 'None', 'False', 'false'):
        res = proxy(sa_session, result=none, count='count')
        assert res['message'] == 'Ok'
        assert none not in res
        assert 'result' not in res
        assert res['count'] > 1

    res = proxy(sa_session, result='result', count='count', start=1, limit=1)
    assert res['message'] == 'Ok'
    assert len(res['result']) == 1
    assert res['count'] > 1

    res = proxy(sa_session, result=True, asdict=True)
    assert len(res) == 2
    assert 'goodfn' in res[0]
    assert isinstance(res[0], dict)

    for none in (None, 'None', 'False', 'false'):
        res = proxy(sa_session, result=True, asdict=none)
        assert len(res) == 2
        assert getattr(res[0], 'goodfn') == 'foo'
        assert not isinstance(res[0], dict)

    res = proxy(sa_session, result=None, metadata='metadata')
    assert res['message'] == 'Ok'
    assert res['metadata']['fields']

    res = proxy(sa_session, result='True', sort_col="firstname")
    assert res[1].firstname > res[0].firstname

    res = proxy(sa_session, sort_col="firstname", sort_dir="DESC")
    assert res[0].firstname > res[1].firstname


def test_simple_select_decl(sa_session):
    proxy = ProxiedQuery(Pet.__table__.select())

    res = proxy(sa_session, result='root', filter_col='name', filter_value="foo")
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    res = proxy(sa_session, filter_by_name='Yacu')
    assert len(res) == 1

    res = proxy(sa_session, filter_by_='Yacu')
    assert len(res) > 1

    res = proxy(sa_session, filter_by_timestamp="2009-12-07T19:00:00,2009-12-07T19:00:00",
                result=False, count='count')
    assert res['count'] == 2

    proxy = ProxiedQuery(persons.select())

    res = proxy(sa_session, filter_by_timestamp="2009-12-07T19:00:00,2009-12-07T19:00:00",
                result=False, count='count')
    assert res['count'] == 1

    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(select(persons.c.firstname.label('FN')))
    else:
        proxy = ProxiedQuery(select([persons.c.firstname.label('FN')]))

    res = proxy(sa_session, result=False, metadata='metadata')
    fields = res['metadata']['fields']
    assert len(fields) == 1
    assert fields[0]['label'] == 'First name'


def test_with_join(sa_session):
    pets = Pet.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(
            select(persons.c.firstname, func.count(pets.c.id).label('number'))
            .select_from(persons.outerjoin(pets)).group_by(persons.c.firstname),
            dict(number=dict(label='Number',
                             hint='Number of pets')))
    else:
        proxy = ProxiedQuery(
            select([persons.c.firstname, func.count(pets.c.id).label('number')],
                   from_obj=persons.outerjoin(pets)).group_by(persons.c.firstname),
            dict(number=dict(label='Number',
                             hint='Number of pets')))

    res = proxy(sa_session, result='root', metadata='metadata')
    assert len(res['root']) == 2
    fields = res['metadata']['fields']
    assert fields[0]['label'] == 'First name'
    assert fields[1]['label'] == 'Number'

    res = proxy(sa_session, sort_col="number")
    assert res[0].firstname == 'Lallo'

    res = proxy(sa_session, sort_col="number", sort_dir="DESC")
    assert res[0].firstname == 'Lele'

    res = proxy(sa_session, sorters=('[{"property":"number","direction":"DESC"}'
                              ',{"property":"non-existing","direction":"ASC"}]'))
    assert res[0].firstname == 'Lele'

    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(
            select(persons.c.id, persons.c.birthdate, pets.c.birthdate)
            .select_from(persons.outerjoin(pets)))
    else:
        proxy = ProxiedQuery(
            select([persons.c.id, persons.c.birthdate, pets.c.birthdate],
                   from_obj=persons.outerjoin(pets)))

    res = proxy(sa_session, result=False, count='count', filter_by_birthdate=None)
    assert res['count'] == 0

    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(
            select(persons.c.firstname)
            .select_from(persons.outerjoin(pets)))
    else:
        proxy = ProxiedQuery(
            select([persons.c.firstname],
                   from_obj=persons.outerjoin(pets)))

    res = proxy(sa_session, result=False, count='count', filter_by_persons_id=-1)
    assert res['count'] == 0

    res = proxy(sa_session, result=False, count='count', filter_by_weight=1)
    assert res['count'] == 0

    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(
            select(persons.c.firstname, pets.c.name)
            .select_from(persons.outerjoin(pets)))
    else:
        proxy = ProxiedQuery(
            select([persons.c.firstname, pets.c.name],
                   from_obj=persons.outerjoin(pets)))

    res = proxy(sa_session, result=False, count='count', filter_by_birthdate=None)
    assert res['count'] == 0


def test_one_foreign_key(sa_session):
    pets = Pet.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(select(pets.c.name, pets.c.person_id,
                                    persons.c.firstname)
                             .select_from(pets.join(persons)))
    else:
        proxy = ProxiedQuery(select([pets.c.name, pets.c.person_id,
                                     persons.c.firstname],
                                    from_obj=pets.join(persons)))

    res = proxy(sa_session, result=False, metadata='metadata')
    fields = res['metadata']['fields']
    assert len(fields) == 3
    assert fields[0]['label'] == 'Pet name'
    assert fields[1]['label'] == 'Person_id'
    assert fields[1]['foreign_keys'] == ('persons.id',)
    assert fields[2]['label'] == 'First name'


def test_two_foreign_keys(sa_session):
    p1 = Pet.__table__.alias('p1')
    p2 = Pet.__table__.alias('p2')
    paired_pets = PairedPets.__table__

    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(
            select(paired_pets.c.id,
                   paired_pets.c.pet1_id,
                   p1.c.name,
                   paired_pets.c.pet2_id,
                   p2.c.name)
            .select_from(paired_pets
                         .join(p1, p1.c.id == paired_pets.c.pet1_id)
                         .join(p2, p2.c.id == paired_pets.c.pet2_id)))
    else:
        proxy = ProxiedQuery(
            select([paired_pets.c.id,
                    paired_pets.c.pet1_id,
                    p1.c.name,
                    paired_pets.c.pet2_id,
                    p2.c.name],
                   from_obj=paired_pets
                   .join(p1, p1.c.id == paired_pets.c.pet1_id)
                   .join(p2, p2.c.id == paired_pets.c.pet2_id)))

    res = proxy(sa_session, result=False, metadata='metadata')
    fields = res['metadata']['fields']
    assert len(fields) == 5
    assert fields[1]['name'] == 'pet1_id'
    assert fields[1]['foreign_keys'] == ('pets.id',)
    assert fields[2]['label'] == 'Pet name'
    assert fields[3]['name'] == 'pet2_id'
    assert fields[3]['foreign_keys'] == ('pets.id',)
    assert fields[4]['label'] == 'Pet name'


def test_with_aliased_join(sa_session):
    persons_alias = persons.alias('prs')
    pets_alias = Pet.__table__.alias('pts')
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(select(persons_alias.c.firstname, pets_alias.c.name)
                             .select_from(persons_alias.join(pets_alias)))
    else:
        proxy = ProxiedQuery(select([persons_alias.c.firstname, pets_alias.c.name],
                                    from_obj=persons_alias.join(pets_alias)))

    res = proxy(sa_session, result='root', metadata='metadata')
    assert len(res['root']) == 2
    assert res['metadata']['fields'][0]['label'] == 'First name'
    assert res['metadata']['fields'][1]['label'] == 'Pet name'


def test_with_labelled_aliased_join(sa_session):
    persons_alias = persons.alias('prs')
    pets_alias = Pet.__table__.alias('pts')
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(select(persons_alias.c.firstname.label('Person'),
                                    pets_alias.c.name.label('PetName'))
                             .select_from(persons_alias.join(pets_alias)))
    else:
        proxy = ProxiedQuery(select([persons_alias.c.firstname.label('Person'),
                                     pets_alias.c.name.label('PetName')],
                                    from_obj=persons_alias.join(pets_alias)))

    res = proxy(sa_session, result='root', metadata='metadata')
    assert len(res['root']) == 2
    fields = res['metadata']['fields']
    assert fields[0]['label'] == 'First name'
    assert fields[1]['name'] == 'PetName'
    assert fields[1]['label'] == 'Pet name'


def test_select_with_bindparams(sa_session):
    if SQLALCHEMY_VERSION > (1, 4):
        query = select(persons.c.firstname).where(
            persons.c.birthdate == bindparam('birth', type_=Date,
                                             value=date(1955, 9, 21)))
    else:
        query = select([persons.c.firstname],
                       persons.c.birthdate == bindparam('birth', type_=Date,
                                                        value=date(1955, 9, 21)))
    proxy = ProxiedQuery(query)

    res = proxy(sa_session, result='root')
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lallo'

    res = proxy(sa_session, result=False, count='count')
    assert res['count'] == 1

    res = proxy(sa_session, result=False, count='count',
                params=dict(birth=date(2000, 1, 1)))
    assert res['count'] == 0

    res = proxy(sa_session, result='root',
                params=dict(birth=date(1968, 3, 18)))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lele'

    res = proxy(sa_session, result='root',
                params=dict(birth=date(2000, 1, 1), foo=1))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    res = proxy(sa_session, result='root', params=dict(birth="1968-03-18"))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lele'


def test_select_with_typeless_bindparams(sa_session):
    if SQLALCHEMY_VERSION > (1, 4):
        query = select(persons.c.firstname).where(persons.c.birthdate == bindparam('birth'))
    else:
        query = select([persons.c.firstname],
                       persons.c.birthdate == bindparam('birth'))

    proxy = ProxiedQuery(query)

    res = proxy(sa_session, result='root', params=dict(birth=None))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 0

    res = proxy(sa_session, result=False, count='count', params=dict(birth=None))
    assert res['count'] == 0

    res = proxy(sa_session, result='root', params=dict(birth=date(1968, 3, 18)))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lele'

    res = proxy(sa_session, result='root', params=dict(birth="1968-03-18"))
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['root'][0][0] == 'Lele'

    res = proxy(sa_session, result=False, count='count',
                params=dict(birth="1968-03-18"))
    assert res['message'] == 'Ok'
    assert res['count'] == 1

    res = proxy(sa_session, result=False, count='count',
                params=dict(birth="1968-03-18",
                            foo="bar"))
    assert res['message'] == 'Ok'
    assert res['count'] == 1

    try:
        proxy(sa_session, result=False, count='count')
    except StatementError:
        pass
    else:
        if SQLALCHEMY_VERSION < (1, 4):
            assert False, "Should raise a StatementError"


def test_select_ordered_on_subselect(sa_session):
    pets = Pet.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        query = (select(persons.c.firstname,
                        exists()
                        .where(pets.c.person_id == persons.c.id)
                        .label("Petted"))
                 .order_by(desc("Petted")))
    else:
        query = (select([persons.c.firstname,
                         exists()
                         .where(pets.c.person_id == persons.c.id)
                         .label("Petted")])
                 .order_by(desc("Petted")))

    proxy = ProxiedQuery(query)

    res = proxy(sa_session, result='root', count='count')
    assert res['count'] == 2
    assert getattr(res['root'][0], 'firstname') == 'Lele'


def test_select_with_aggregate_function(sa_session):
    pets = Pet.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        query = (select(persons.c.id,
                        persons.c.firstname,
                        func.group_concat(pets.c.name).label("Pets"))
                 .where(pets.c.person_id == persons.c.id)
                 .group_by(persons.c.id))
    else:
        query = (select([persons.c.id,
                         persons.c.firstname,
                         func.group_concat(pets.c.name).label("Pets")],
                        pets.c.person_id == persons.c.id)
                 .group_by(persons.c.id))

    proxy = ProxiedQuery(query)

    res = proxy(sa_session, result='root', count='count', metadata='metadata')
    assert res['count'] == 1
    assert getattr(res['root'][0], 'firstname') == 'Lele'
    fields = res['metadata']['fields']
    assert fields[1]['label'] == 'First name'
    assert fields[2]['label'] == 'Pets'
    assert fields[2]['type'] == 'string'


def test_literal_column(sa_session):
    for lc in (literal_column, text):
        if SQLALCHEMY_VERSION > (1, 4):
            query = select(lc("'foo'"))
        else:
            query = select([lc("'foo'")])
        proxy = ProxiedQuery(query)

        res = proxy(sa_session, result='root', count='count', metadata='metadata')
        assert res['count'] == 1
        assert res['root'][0][0] == 'foo'
        assert res['metadata']['fields'][0]['label'] == "'foo'"


def test_union(sa_session):
    if SQLALCHEMY_VERSION > (1, 4):
        query1 = select(persons.c.id, persons.c.firstname).where(
            persons.c.firstname == 'Lele')
        query2 = select(persons.c.id, persons.c.firstname).where(
            persons.c.firstname == 'Lallo')
    else:
        query1 = select([persons.c.id, persons.c.firstname],
                        persons.c.firstname == 'Lele')
        query2 = select([persons.c.id, persons.c.firstname],
                        persons.c.firstname == 'Lallo')

    proxy = ProxiedQuery(query1.union_all(query2))

    res = proxy(sa_session, result='root', count='count', metadata='metadata')
    assert res['count'] == 2
    assert res['root'][0][1] == 'Lele'
    assert res['root'][1][1] == 'Lallo'
    expected_label = 'First name' if SQLALCHEMY_VERSION > (1, 4) else 'Firstname'
    assert res['metadata']['fields'][1]['label'] == expected_label

    res = proxy(sa_session, result='root', count='count', filter_by_firstname='Lele')
    assert res['message'] == 'Ok'
    assert res['count'] == 1
    assert len(res['root']) == 1

    res = proxy(sa_session, result='root', fields='firstname', query="Lele")
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1

    res = proxy(sa_session, result='root',
                filters=[dict(property='firstname', value="L", operator='STARTSWITH')])
    assert res['message'] == 'Ok'
    assert len(res['root']) == 2

    res = proxy(sa_session, result='root', only_cols='firstname', metadata='metadata')
    assert res['message'] == 'Ok'
    assert len(res['root']) == 2
    assert res['root'][0][0] == 'Lele'
    assert res['root'][1][0] == 'Lallo'
    assert res['metadata']['fields'][0]['label'] == expected_label

    res = proxy(sa_session, result='root', count='count', start=1, limit=1)
    assert res['message'] == 'Ok'
    assert len(res['root']) == 1
    assert res['count'] > 1


@pytest.mark.skipif(SQLALCHEMY_VERSION < (1, 4),
                    reason="v2 query style not supported")
def test_v2_style(sa_session):
    query = select(persons.c.id, persons.c.firstname)
    proxy = ProxiedQuery(query)

    res = proxy(sa_session, result='root', count='count', metadata='meta')
    assert res['count'] == 2
    assert len(res['meta']['fields']) == 2
