"""
               _       _ _
 ___  ___ _ __(_) __ _| (_)___  ___ _ __
/ __|/ _ \\ '__| |/ _` | | / __|/ _ \\ '__|
\\__ \\  __/ |  | | (_| | | \\__ \\  __/ |
|___/\\___|_|  |_|\\__,_|_|_|___/\\___|_|

Copyright &copy;2020 - Mad Penguin Consulting Limited
"""
from __future__ import annotations
from typing import Optional
from enum import Enum
from lmdb import Transaction as TXN
from json import loads, dumps
from orbit_database.doc import Doc
from orbit_database.exceptions import InvalidSerialiser

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover

try:
    import ujson
except Exception:   # pragma: no cover
    pass            # pragma: no cover

try:
    import orjson
except Exception:   # pragma: no cover
    pass            # pragma: no cover


class SerialiserType(Enum):
    """
    Serialisers are pluggable via this module, currently we support the following;

    o UJSON     the default historical serialiser
    o ORJSON    the new guy on the block
    """
    JSON = 'json'
    UJSON = 'ujson'
    ORJSON = 'orjson'
    RAW = 'raw'
    NONE = 'none'


def raw_dumps(doc):
    return doc

def raw_loads(doc):
    return doc


class Serialiser:
    """
    All attempts to serialise or de-serialise data come through this point. Any new serialiser
    that supports "loads" and "dumps" can simplu be imported and plugged into __init__ and that
    should be all there is to it.
    """

    def __init__(self, codec: Optional[SerialiserType]=SerialiserType.NONE, txn: TXN=None):
        """
        Set up handlers for serialisation and de-serialisation.

        codec - module that will supply "dumps" and "loads" methods
        """
        if not self._meta:
            self._generic_loads = loads
            self._generic_dumps = dumps
            self._codec = SerialiserType.JSON
            return
        #
        #   Sentinel - make sure we don't use a serialiser on data that's already been
        #              written with a different serialsier.
        #
        config = self._meta.fetch_config(self.name, txn=txn)
        if codec and codec != SerialiserType.NONE:
            if 'codec' in config:
                if codec.value != config._codec:
                    raise InvalidSerialiser(f'trying to use "{codec.value}" but data encoded with "{config._codec}"')
        else:
            if 'codec' in config:
                codec = SerialiserType(config['codec'])
            elif 'ujson' in globals():
                codec = SerialiserType.UJSON
            elif 'orjson' in globals():         # pragma: no cover
                codec = SerialiserType.ORJSON   # pragma: no cover
            else:
                codec = SerialiserType.JSON
            
        if 'codec' not in config:
            config._codec = codec.value
            self._meta.store_config(self.name, config, txn=txn)

        if codec == SerialiserType.UJSON:
            self._generic_dumps = ujson.dumps
            self._generic_loads = ujson.loads
        elif codec == SerialiserType.ORJSON:
            self._generic_dumps = orjson.dumps
            self._generic_loads = orjson.loads
        elif codec == SerialiserType.RAW:
            self._generic_dumps = raw_dumps
            self._generic_loads = raw_loads
        elif codec == SerialiserType.JSON:
            self._generic_dumps = dumps
            self._generic_loads = loads
        else:
            raise InvalidSerialiser(f'invalid serialised "{codec.value}"')
        
        self._codec = codec


                       
        # if 'codec' not in config:
        #     config._codec = self._codec.value
        #     self._meta.store_config(self.name, config, txn=txn)
        # else:
        #     if self._codec.value != config._codec:
        #         if config._codec == 'raw':
        #             self._codec = SerialiserType.RAW
        #         else:
        #             raise InvalidSerialiser(f'trying to use "{self._codec.value}" but data encoded with "{config._codec}"')


        # log.error(f'Codec={codec} self.codec={self._codec}')

        # if not codec or codec == SerialiserType.NONE:
        #     if 'ujson' in globals():
        #         codec = SerialiserType.UJSON
        #     elif 'orjson' in globals():         # pragma: no cover
        #         codec = SerialiserType.ORJSON   # pragma: no cover

        # if codec == SerialiserType.UJSON:
        #     self._generic_dumps = ujson.dumps
        #     self._generic_loads = ujson.loads
        # elif codec == SerialiserType.ORJSON:
        #     self._generic_dumps = orjson.dumps
        #     self._generic_loads = orjson.loads
        # elif codec == SerialiserType.RAW:
        #     self._generic_dumps = raw_dumps
        #     self._generic_loads = raw_loads
        # elif codec != SerialiserType.JSON:
        #     codec = self._codec  # pragma: no cover
        # #
        # self._codec = codec
        #
        #   Sentinel - make sure we don't use a serialiser on data that's already been
        #              written with a different serialsier.
        #
        # config = self._meta.fetch_config(self.name, txn=txn)
        # if 'codec' not in config:
        #     config._codec = self._codec.value
        #     self._meta.store_config(self.name, config, txn=txn)
        # else:
        #     if self._codec.value != config._codec:
        #         if config._codec == 'raw':
        #             self._codec = SerialiserType.RAW
        #         else:
        #             raise InvalidSerialiser(f'trying to use "{self._codec.value}" but data encoded with "{config._codec}"')

    def serialise(self, doc: dict) -> bytes:
        """
        Generic serialiser interface
        """
        try:
            dump = self._generic_dumps(doc)
            return dump if isinstance(dump, bytes) else dump.encode()
        except Exception as e:
            log.error(f'Error on table: {self.name}')
            log.error(f'Doc={doc}')
            log.error(f'Doc={doc.doc}')
            raise
        
        # dump = self._generic_dumps(doc)
        # try:
        #     return dump.encode() if isinstance(dump, dict) else dump
        # except Exception as e:
        #     print(f'Error: {str(e)}')
        #     print(f'Dump is {dump} {type(dump)}')
        #     raise

    def deserialise(self, blob: bytes) -> dict:
        """
        Generic deserialiser interface
        """
        try:
            return self._generic_loads(blob)
        except Exception:
            log.error(f'Error: codec={self._codec}')
            log.error(f'Error: {self._generic_loads}')
            return blob

    @property
    def codec(self) -> SerialiserType:
        """
        Return the serialiser currently in use for this table
        """
        return self._codec
