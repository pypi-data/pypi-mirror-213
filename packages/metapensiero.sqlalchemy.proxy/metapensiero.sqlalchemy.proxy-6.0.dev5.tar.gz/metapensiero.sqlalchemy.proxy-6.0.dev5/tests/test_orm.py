# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests for ProxiedEntity
# :Created:   dom 19 ott 2008 00:04:34 CEST
# :Author:    Lele Gaifax <lele@nautilus.homeip.net>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2013, 2014, 2015, 2016, 2017, 2018, 2020, 2021, 2023 Lele Gaifax
#

from datetime import date

import pytest
from sqlalchemy.orm import Query, contains_eager, joinedload

from metapensiero.sqlalchemy.proxy.orm import ProxiedEntity
from metapensiero.sqlalchemy.proxy.utils import SQLALCHEMY_VERSION
from fixture import Complex, Person, PairedPets, Pet


def test_basic(sa_session):
    proxy = ProxiedEntity(Person, 'id,firstname,title'.split(','))

    res = proxy(sa_session, result='root', count='count',
                filter_col='lastname', filter_value='foo')
    assert res['message'] == 'Ok'
    assert res['count'] == 0

    res = proxy(sa_session, result='root', count='count',
                filter_by_lastname='foo', filter_by_firstname='bar')
    assert res['message'] == 'Ok'
    assert res['count'] == 0

    res = proxy(sa_session, Person.firstname == 'Lele', result='root', count='count')
    assert res['message'] == 'Ok'
    assert res['count'] == len(res['root'])
    assert res['root'][0].title == "Perito Industriale"

    res = proxy(sa_session, Person.firstname == 'Lele', Person.lastname == 'Gaifax',
                result='root', count='count')
    assert res['message'] == 'Ok'
    assert res['count'] == 0

    res = proxy(sa_session, result='root', count="count",
                filter_col='firstname', filter_value='Lele')
    assert res['message'] == 'Ok'
    assert res['count'] == len(res['root'])
    assert res['root'][0].title == "Perito Industriale"


def test_boolean(sa_session):
    proxy = ProxiedEntity(Person, 'id,firstname'.split(','))

    res = proxy(sa_session, result='root', count='count', filter_by_smart='true')
    assert res['message'] == 'Ok'
    assert res['count'] == 1

    res = proxy(sa_session, result='root', count="count", filter_by_smart='false')
    assert res['message'] == 'Ok'
    assert res['count'] == len(res['root'])
    assert res['root'][0].firstname == 'Lele'

    res = proxy(sa_session, result=False, only_cols='["firstname","lastname"]')
    assert res['message'] == 'Ok'


def test_basic_decl(sa_session):
    proxy = ProxiedEntity(Pet)

    res = proxy(sa_session, result='root', count='count',
                filter_col='name', filter_value='Yacu')
    assert res['message'] == 'Ok'
    assert res['count'] == 1


def test_metadata(sa_session):
    proxy = ProxiedEntity(Person, 'id,smart,title'.split(','),
                          dict(smart=dict(label='Some value',
                                          hint='A value from a set',
                                          default=False,
                                          dictionary=((0, 'low'),
                                                      (1, 'medium'),
                                                      (2, 'high')))))

    res = proxy(sa_session, success='success', result=None, metadata='metadata')
    assert res['success'] is True
    assert res['metadata'].get('root_slot') is None
    fields = res['metadata']['fields']
    assert len(fields) == 3
    assert fields[1]['default'] is False
    assert fields[1]['dictionary'] == [[0, 'low'],
                                       [1, 'medium'],
                                       [2, 'high']]
    assert fields[2]['type'] == 'string'

    proxy = ProxiedEntity(
        Person,
        'id,firstname,lastname,birthdate,somevalue'.split(','),
        dict(firstname=dict(label='First name',
                            hint='First name of the person'),
             lastname=lambda fname: dict(label='Foo'),
             somevalue=dict(label='Some value',
                            hint='A value from a set',
                            dictionary={0: 'low',
                                        1: 'medium',
                                        2: 'high'})))
    proxy.translate = lambda msg: msg.upper()

    res = proxy(sa_session, success='success', result='root', count='count',
                metadata='metadata', filter_by_firstname='Lele', asdict=True)
    assert res['success'] is True
    assert res['message'] == 'Ok'
    assert res['count'] == 1
    fields = res['metadata']['fields']
    assert len(fields) == 5
    assert fields[1]['label'] == 'FIRST NAME'
    assert fields[2]['label'] == 'FOO'
    assert fields[3]['min'] == date(1980, 1, 1)
    assert fields[3]['max'] == date.today()
    assert fields[4]['dictionary'] == {0: 'LOW', 1: 'MEDIUM', 2: 'HIGH'}
    assert res['metadata']['count_slot'] == 'count'
    assert res['metadata']['root_slot'] == 'root'
    assert res['metadata']['success_slot'] == 'success'
    assert isinstance(res['root'][0], dict)

    proxy = ProxiedEntity(Pet, 'id,name,birthdate,weight,notes'.split(','),
                          dict(name=dict(label='Pet name',
                                         hint='The name of this pet')))

    res = proxy(sa_session, result=False, metadata='metadata')
    assert res['message'] == 'Ok'
    fields = res['metadata']['fields']
    assert len(fields) == 5
    assert fields[0]['label'] == 'id'
    assert fields[0]['hint'] == 'the pet id'
    assert fields[1]['label'] == 'Pet name'
    assert fields[1]['hint'] == 'The name of this pet'
    assert fields[2]['min'] == date(1980, 1, 1)
    assert fields[2]['max'] == date.today()
    assert fields[3]['decimals'] == 2
    assert res['metadata']['primary_key'] == 'id'

    proxy = ProxiedEntity(Complex)
    res = proxy(sa_session, result=False, metadata='metadata')
    assert res['metadata']['primary_key'] == ('id1', 'id2')

    proxy = ProxiedEntity(Pet)
    res = proxy(sa_session, result=False, metadata='metadata')
    fields = res['metadata']['fields']
    assert fields[4]['name'] == 'weight'
    assert fields[4]['decimals'] == 2
    assert fields[5]['name'] == 'notes'
    assert fields[5]['type'] == 'text'

    proxy = ProxiedEntity(PairedPets)
    res = proxy(sa_session, result=False, metadata='metadata')
    assert res['metadata']['primary_key'] == 'id'
    fields = res['metadata']['fields']
    assert fields[0]['name'] == 'id'
    assert 'default' not in fields[0]
    assert fields[1]['name'] == 'pet1_id'
    assert fields[1]['foreign_keys'] == ('pets.id',)


def test_query(sa_session):
    proxy = ProxiedEntity(Person)

    res = proxy(sa_session, query="Lele", fields="firstname,lastname,nickname")
    assert len(res) == 1

    res = proxy(sa_session, query="Lele", fields="firstname")
    assert len(res) == 1

    res = proxy(sa_session, query="perito")
    assert len(res) == 1

    res = proxy(sa_session, query="aifa", fields="firstname,lastname,nickname")
    assert len(res) > 1


def test_filters(sa_session):
    proxy = ProxiedEntity(Person)

    res = proxy(sa_session, filters=[dict(property='firstname', value="=Lele")])
    assert len(res) == 1

    res = proxy(sa_session, filters=[dict(property='firstname')])
    assert len(res) > 1

    res = proxy(sa_session, filters=[dict(value='=Lele')])
    assert len(res) > 1

    res = proxy(sa_session, filters=[dict(property='firstname', value="Lele",
                                   operator='=')])
    assert len(res) == 1

    res = proxy(sa_session, filters=[dict(property='lastname', value="aifa")])
    assert len(res) > 1

    res = proxy(sa_session, filters=[dict(property='lastname', value="aifa",
                                   operator='~')])
    assert len(res) > 1


def test_dict(sa_session):
    proxy = ProxiedEntity(Person, 'id,firstname,lastname,goodfn'.split(','))

    res = proxy(sa_session, limit=1, asdict=True)
    assert len(res) == 1
    p = res[0]
    for f in ('id', 'firstname', 'lastname', 'goodfn'):
        assert f in p
    assert 'birthdate' not in p


def test_plain_entities(sa_session):
    proxy = ProxiedEntity(Person)

    res = proxy(sa_session, filter_by_firstname='Lele')
    assert len(res) == 1
    p = res[0]
    assert p.firstname == 'Lele'
    assert isinstance(p, Person)


def test_sort(sa_session):
    proxy = ProxiedEntity(Person)

    res = proxy(sa_session, sort_col="firstname")
    assert res[0].firstname < res[1].firstname

    res = proxy(sa_session, sort_col="lastname,firstname")
    assert res[0].firstname < res[1].firstname

    res = proxy(sa_session, sort_col="firstname", sort_dir="DESC")
    assert res[0].firstname > res[1].firstname

    res = proxy(sa_session, sorters='[{"property":"firstname","direction":"DESC"}]')
    assert res[0].firstname > res[1].firstname

    res = proxy(sa_session, sorters=dict(property="firstname", direction="DESC"))
    assert res[0].firstname > res[1].firstname


def test_sort_multiple(sa_session):
    proxy = ProxiedEntity(Person)

    res = proxy(sa_session, sorters=[dict(property="firstname", direction="ASC")])
    assert res[0].firstname < res[1].firstname

    res = proxy(sa_session, sorters=[dict(property="firstname", direction="DESC")])
    assert res[0].firstname > res[1].firstname

    res = proxy(sa_session, sorters=[dict(property="somevalue"),
                              dict(property="birthdate", direction="DESC")])
    assert res[0].birthdate > res[1].birthdate


def test_orm_queries(sa_session):
    query = Query([Pet])
    proxy = ProxiedEntity(query)

    res = proxy(sa_session, sort_col="name")
    assert res[0].name < res[1].name

    query = Query([Pet])
    proxy = ProxiedEntity(query, fields=['name', 'birthdate'])
    res = proxy(sa_session, success='success', result=None, metadata='metadata')
    assert res['success'] is True
    assert res['metadata'].get('root_slot') is None
    assert len(res['metadata']['fields']) == 2
    assert res['metadata']['fields'][0]['label'] == "Pet name"


@pytest.mark.xfail(SQLALCHEMY_VERSION > (2, 0),
                   reason="joinload() creates anonymous join alias")
def test_orm_joinedload(sa_session):
    query = Query([Pet]).options(joinedload(Pet.person).load_only(Person.firstname))
    proxy = ProxiedEntity(query)
    res = proxy(sa_session, sort_col="firstname")
    assert res[0].person.firstname == res[1].person.firstname


def test_orm_contains_eager(sa_session):
    query = Query([Pet]).join(Pet.person).options(contains_eager(Pet.person)
                                                  .load_only(Person.firstname))
    proxy = ProxiedEntity(query)
    res = proxy(sa_session, sort_col="firstname")
    assert res[0].person.firstname == res[1].person.firstname
