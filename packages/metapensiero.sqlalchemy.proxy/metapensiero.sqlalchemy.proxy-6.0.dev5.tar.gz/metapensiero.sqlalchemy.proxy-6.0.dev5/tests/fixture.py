# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests fixtures
# :Created:   mer 03 feb 2016 11:26:04 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2018, 2020, 2021, 2023 Lele Gaifax
#

from datetime import date, datetime

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer, MetaData,
                        Numeric, Sequence, String, Text, Table, orm)
from sqlalchemy.types import TypeDecorator

from metapensiero.sqlalchemy.proxy.utils import SQLALCHEMY_VERSION


if SQLALCHEMY_VERSION > (1, 4):
    mapper = orm.registry().map_imperatively
else:
    mapper = orm.mapper


class Title(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value and value.title()


def birthdate_info(name):
    return {
        'min': date(1980, 1, 1),
        'max': lambda fname, iname: date.today()
    }


metadata = MetaData()


persons = Table('persons', metadata,
                Column('id', Integer, primary_key=True),
                Column('firstname', String,
                       info=dict(label="First name",
                                 hint="The first name of the person")),
                Column('lastname', String),
                Column('birthdate', Date, info=birthdate_info),
                Column('timestamp', DateTime),
                Column('smart', Boolean, default=True),
                Column('somevalue', Integer, default=lambda: 42),
                Column('title', Title),
                Column('WeirdFN', String, key='goodfn'),
                )


if SQLALCHEMY_VERSION > (2, 0):
    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        metadata = metadata
else:
    from sqlalchemy.orm import declarative_base

    Base = declarative_base(metadata=metadata)


class Person:
    def __init__(self, firstname, lastname, birthdate, timestamp, smart, title, goodfn):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.timestamp = timestamp
        self.smart = smart
        self.somevalue = 0
        self.title = title
        self.goodfn = goodfn


mapper(Person, persons)


class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True,
                info=dict(label='id', hint='the pet id'))
    name = Column(String, info=dict(label='Pet name', hint='The name of the pet'))
    person_id = Column(Integer, ForeignKey('persons.id'))
    birthdate = Column(Date, info=birthdate_info)
    weight = Column(Numeric(5, 2),
                    info=dict(label='weight', hint='the weight'))
    notes = Column(Text, info=dict(label='notes', hint='random notes'))

    person = orm.relationship(Person, backref=orm.backref('pets', order_by=id))


class Complex(Base):
    __tablename__ = 'complex'

    id1 = Column(Integer, primary_key=True,
                 info=dict(label='id1', hint='the first part of id'))
    id2 = Column(Integer, primary_key=True,
                 info=dict(label='id2', hint='the second part of id'))
    name = Column(String)


class PairedPets(Base):
    __tablename__ = 'paired_pets'

    id = Column(Integer, Sequence('gen_paired_pet_id', optional=True),
                primary_key=True,
                info=dict(label='id', hint='the pairing id'))
    pet1_id = Column(Integer, ForeignKey('pets.id'))
    pet2_id = Column(Integer, ForeignKey('pets.id'))

    pet1 = orm.relationship(Pet, foreign_keys=pet1_id)
    pet2 = orm.relationship(Pet, foreign_keys=pet2_id)
