# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- python-rapidjson glue
# :Created:   gio 04 dic 2008 13:56:51 CET
# :Author:    Lele Gaifax <lele@nautilus.homeip.net>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2012, 2013, 2014, 2016, 2017, 2020, 2021 Lele Gaifax
#


class JSON:
    """
    Namespace-class to make it easier replacing the actual implementation of the methods using
    a different JSON library instead of the default one based on `python-rapidjson`__.

    __ https://pypi.python.org/pypi/python-rapidjson
    """

    @staticmethod
    def decode(s):
        """Parse `s`, a JSON encoded string, and return the equivalent Python structure.

        This is implemented on top of `python-rapidjson`__, to handle ``UUID``, ``datetime``,
        ``date`` and ``Decimal`` data types.

        __ https://pypi.org/project/python-rapidjson/
        """

        from rapidjson import Decoder, DM_ISO8601, NM_DECIMAL, UM_CANONICAL

        json2py = Decoder(datetime_mode=DM_ISO8601,
                              number_mode=NM_DECIMAL,
                              uuid_mode=UM_CANONICAL).__call__
        JSON.decode = staticmethod(json2py)
        return json2py(s)

    @staticmethod
    def encode(o):
        """Encode `o`, an arbitrary Python object, into a JSON encoded string.

        This is implemented on top of `python-rapidjson`__, to handle ``UUID``, ``datetime``,
        ``date`` and ``Decimal`` data types.

        __ https://pypi.org/project/python-rapidjson/
        """

        from rapidjson import Encoder, DM_ISO8601, NM_DECIMAL, UM_CANONICAL

        py2json = Encoder(datetime_mode=DM_ISO8601,
                          number_mode=NM_DECIMAL,
                          uuid_mode=UM_CANONICAL,
                          ensure_ascii=False).__call__
        JSON.encode = staticmethod(py2json)
        return py2json(o)


def register_json_decoder_encoder(decode, encode):
    "Replace the JSON `decode` and `encode` functions."

    JSON.decode = decode if isinstance(decode, staticmethod) else staticmethod(decode)
    JSON.encode = encode if isinstance(encode, staticmethod) else staticmethod(encode)
