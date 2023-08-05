#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from lmdb import Transaction as TXN, Cursor
from lmdb import BadValsizeError
from typing import TYPE_CHECKING, Optional, Callable
from orbit_database.doc import Doc
from orbit_database.decorators import wrap_reader
from orbit_database.exceptions import DuplicateKey
from orbit_database.types_ import Config
from orbit_database.invertedwordindex import InvertedWordIndex

if TYPE_CHECKING:
    from .table import Table  # pragma: no cover

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover


class Index(InvertedWordIndex):
    """
    The Index class models individual indexes of which a table may have zero or more. There
    are two crucial parameters supplied when setting up an index and are passed via "conf".

    o dupsort    this controls whether the index will allow duplicate values to be inserted
    o func       this is the anonymous function used to generate key values from the date record
    """

    def __init__(self, table: Table, name: str, conf: Config) -> None:
        """
        When we instantiate an Index we primarily need a back-reference to the database we're
        working with, the name of the index we're instantiating, and a definition of the indexing
        function. The indexing function is held in the 'func' item in the conf dictionary. By
        default the indexing function will be a python format string, hoever you can also supply
        a 'proper' python function if you prefix it with 'def '

        database - a reference to the database we're working with
        name - the name of the index we're creating a reference to
        conf - a configuration dict containing information specific to this dictionary
        """
        self._table = table
        self._conf = dict(conf)
        self.env = table.env
        self.name = name
        self._db = None
        self._writer = None
        self._lower = False
        self.func = func = self._conf.get('func')

        if func:
            if func[:4] == 'def ':
                self._func = self.anonymous_full(func)
            else:
                if self._conf.get('lower'):
                    self._lower = True
                    skel = '(r): return "{}".format(**r).lower().encode()'
                else:
                    skel = '(r): return "{}".format(**r).encode()'
                self._func = self.anonymous(skel.format(self._conf.get('func')))
        self.duplicates = self._conf.get('dupsort', False)
        self._conf.pop('func', None)
        self._conf.pop('lower', None)
        super().__init__()

    @property
    def metadata (self):
        return dict(self._conf, **{'func': self.func})

    def open(self, txn: TXN) -> None:
        """
        Open the index and make it available to the table

        txn = an optional transaction
        """
        if self._iwx:
            return super().open(txn)
        options = dict(self._conf, **{'key': self._conf['key'].encode()})
        self._db = self.env.open_db(**options, txn=txn)

    @wrap_reader
    def records(self, txn: Optional[TXN]=None) -> int:
        """
        Return the number of records in this index

        txn - an optional transaction
        """
        if self._iwx:
            return super().iwx_oids(txn)
        else:
            return txn.stat(self._db).get('entries', 0)

    def save(self, old_doc: Doc, new_doc: Doc, txn: TXN) -> None:
        """
        Update a pre-existing index entry, we need both the old version of the record in
        order to remove the old index entries, and the new record to generate and insert
        the new ones.

        old_doc - the previous version of the record
        new_doc - the new version of the record
        txn - an optional transaction
        """
        if not super().save(old_doc, new_doc, txn):
            try:
                old_key = self._func(old_doc.doc)
            except (AttributeError, KeyError, TypeError):  # pragma: no cover
                old_key = []  # pragma: no cover
            try:
                new_key = self._func(new_doc.doc)
            except (AttributeError, KeyError, TypeError):
                new_key = []
                # log.error(f'bad key, index={self.name} table={self._table.name} / {e} / {new_doc.doc}')
                # log.error(f'old={old_key} new={new_key}')
            if old_key != new_key:
                if not isinstance(old_key, list):
                    old_key = [old_key]
                if not isinstance(new_key, list):
                    new_key = [new_key]
                # FIXME: we should find the intersections here and only update as necessary .. (!)
                for key in old_key:
                    if key:
                        txn.delete(key, old_doc.oid, db=self._db)
                for key in new_key:
                    if key:
                        txn.put(key, new_doc.oid, db=self._db)

    def get(self, doc: Doc, txn: TXN) -> Optional[bytes]:
        """
        Get an entry from this index

        doc - the record template for the data to retrieve
        txn - an optional transaction
        """
        return txn.get(self._func(doc.doc), db=self._db) if not self._iwx else None

    def get_last(self, doc: Doc, txn: TXN) -> Optional[bytes]:
        """
        Get the last entry from a duplicate key index

        doc - the record template for the data to retrieve
        txn - an optional transaction
        """
        cursor = Cursor(self._db, txn)
        if not cursor.get(self._func(doc.doc)):
            return None  # pragma: no cover
        if not cursor.last_dup():
            return None  # pragma: no cover
        return cursor.value()

    def put(self, doc: Doc, txn: TXN) -> None:
        """
        Put a new entry in this index, used when createing new records

        doc - the document associated with this index entry
        txn - an optional transaction
        """
        if not super().put(doc, txn):
            try:
                keys = self._func(doc.doc)
            except (KeyError, TypeError, AttributeError):
                return
            # except AttributeError:
            #     log.error(f'func={self._func} doc={doc.doc}')
            #     raise
            # except TypeError:
            #     log.error(f'type error: {self.func} / {doc.doc}')
            #     raise

            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                if key:
                    try:
                        if not txn.put(key, doc.oid, db=self._db, overwrite=self.duplicates):
                            if not self.duplicates:
                                # log.error(f'duplicate on table={self._table.name} index={self.name} key={keys}')
                                raise DuplicateKey(f'trying to add key "{key}"')
                    except BadValsizeError:
                        log.error(f'key error: {keys} / {self.name}')
                        raise


    def put_cursor(self, cursor: Cursor, txn: TXN) -> None:
        """
        Put a new index entry based on a Cursor rather than a Doc object. This is here
        mainly to make "reindex" more elegant / readable.

        cursor - an LMDB Cursor object
        txn - an optional transaction
        """
        if not super().put_cursor(cursor, txn):
            self.put(Doc(self._table.deserialise(cursor.value()), cursor.key()), txn=txn)

    def delete(self, doc: Doc, txn: TXN) -> None:
        """
        Delete an entry from this index

        doc - record associated with the index entry to delete
        txn - an optional transaction
        """
        if not super().delete(doc, txn):
            try:
                keys = self._func(doc.doc)
            except KeyError:  # pragma: no cover
                return        # pragma: no cover
            except AttributeError:
                return
            except TypeError:
                log.error(f'key delete failed for index={self.name} doc={doc.doc}')
                return
            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                if key:
                    try:
                        txn.delete(key, doc.oid, self._db)
                    except BadValsizeError:
                        log.error(f'key delete failed for index={self.name} key={key}')
                        raise

    def empty(self, txn: TXN) -> None:
        """
        Remove all entries from this index

        txn - an optional transaction
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if not super().empty(transaction):
            transaction.drop(self._db, delete=False)

    def drop(self, txn: TXN) -> None:
        """
        Remove all entries from this index and then remove the index

        txn - an optional transaction
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if not super().drop(transaction):
            transaction.drop(self._db, delete=True)
            self._table._meta.remove_index(self._table.name, self.name, txn=txn)

    def map_key(self, doc: Doc) -> str:
        """
        Return the key derived from the supplied record for this particular index

        doc - the record from which we want to derive a key
        """
        return self._func(doc.doc)

    @staticmethod
    def anonymous(text: str) -> Callable:
        """
        An function used to generate anonymous functions for database indecies

        text - a Python lambda function
        """
        scope = {}
        exec('def func{0}'.format(text), scope)
        return scope['func']

    @staticmethod
    def anonymous_full(text: str) -> Callable:
        """
        A function used to generate anonymous functions for database indecies

        text - a Python lambda function
        """
        scope = {}
        exec(text, scope)
        return scope['func']

    @staticmethod
    def index_path(table_name: str, index_name: str) -> str:
        """
        Produce an index "path" name for this index based on the table name and index name
        """
        return f'_{table_name}_{index_name}'
