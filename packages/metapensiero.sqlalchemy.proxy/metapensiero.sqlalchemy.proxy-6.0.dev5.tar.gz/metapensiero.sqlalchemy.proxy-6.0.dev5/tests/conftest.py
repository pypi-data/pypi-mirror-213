# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy — Pytest fixtures
# :Created:   sab 10 giu 2023, 10:50:37
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2023 Lele Gaifax
#

from datetime import date, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope='module')
def sa_engine(request):
    sa_uri = getattr(request.module, 'SA_URI', 'sqlite:///:memory:')
    return create_engine(sa_uri, echo=True)


@pytest.fixture(scope='module')
def sa_SessionMaker(sa_engine):
    return sessionmaker(autoflush=False, autocommit=False, bind=sa_engine)


@pytest.fixture(scope='module')
def sa_session(sa_SessionMaker, sa_engine):
    from fixture import PairedPets, Person, Pet, metadata

    metadata.create_all(sa_engine)

    with sa_SessionMaker() as sas:
        me = Person('Lele', 'Gaifas', date(1968, 3, 18),
                    datetime(2009, 12, 7, 19, 0, 0), False,
                    "perito industriale", "foo")
        sas.add(me)

        bro = Person('Lallo', 'Gaifas', date(1955, 9, 21),
                     datetime(2009, 12, 7, 20, 0, 0), True,
                     "ingegnere", "bar")
        sas.add(bro)

        yaku = Pet(name='Yacu')
        sas.add(yaku)
        yaku.person = me

        laika = Pet(name='Laika')
        sas.add(laika)
        laika.person = me

        pair = PairedPets()
        sas.add(pair)
        pair.pet1 = yaku
        pair.pet2 = laika

        sas.commit()

        yield sas

    metadata.drop_all(sa_engine)
