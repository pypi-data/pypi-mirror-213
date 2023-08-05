#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from sys import maxsize as MAXSIZE
from collections import UserDict
from typing import Generator, Optional, TYPE_CHECKING, Union, Callable, ClassVar
from lmdb import Transaction as TXN, MapResizedError, NotFoundError, IncompatibleError
from struct import pack, unpack
from orbit_database.index import Index
from orbit_database.doc import Doc, JournalType
from orbit_database.compression import Compression, CompressionType
from orbit_database.serialiser import Serialiser, SerialiserType
from orbit_database.cursor import Cursor
from orbit_database.objectid import ObjectId
from orbit_database.filterresult import FilterResult, MatchResult
from orbit_database.decorators import wrap_reader, wrap_reader_yield, WriteTransaction, wrap_writer
from orbit_database.exceptions import IndexAlreadyExists, DocumentDoesntExist, InvalidKeySpecifier, NoSuchIndex
from orbit_database.types_ import Config, OID, OIDS
from pathlib import Path
from operator import gt as greater, lt as less
from json import load, dump

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover


ZERO = 0


if TYPE_CHECKING:
    from .database import Database  # pragma: no cover


class Table(UserDict, Compression, Serialiser):
    """
    The Table class is used to wrap access to individual database tables and
    incorporates semi-transparent compression / decompression on a per table
    basis. Compression libraries are pluggable and implemented in the
    Compression class.

    o APPEND_MODE - when appending a record we know that the new key will be the
                    highest value in the table so we can take advantage of LMDB's
                    "append" mode. If you never want to use this option, set
                    orbit-database.Table.APPEND_MODE to False.

                    NOTE: compatibility issue, we've switched to our own version
                    of "ObjectId", if you set this to True and have data that
                    uses both BSON/ObjectId and the new ObjectId, you will have
                    a problem. (data loss)
    """
    APPEND_MODE = False

    def __init__(self, database: Database, name: str, cls: ClassVar=Doc) -> None:
        """
        Intantiate a table instance bases on the name of the table required. A
        reference to the containing database is also required so the table
        can back-reference the database environment.

        database - a reference to the containing database object
        name - the name of the table to reference
        """
        self.name = name
        self.env = database.env
        self._database = database
        self._cls = cls
        self._db = None
        self._oid = None
        self._meta = database.meta
        UserDict.__init__(self)
        Compression.__init__(self)

    def __setitem__(self, name: str, conf: Config) -> None:
        """
        Create an entry for an index with the specified name

        name - the name of the index to create
        conf - configuration options for the index we're creating
        """
        if name in self.data:
            raise IndexAlreadyExists(name)
        self.data[name] = Index(self, name, conf)

    def __repr__(self) -> str:
        """
        Generate a string representation of this object, by default we include the
        table name and the table status, i.e. whether it is open or not.
        """
        return f'<{__name__}.Table instance> name="{self.name}" status={"open" if self.isopen else "closed"}'

    @property
    def oid (self) -> ObjectId:
        return self._oid

    @property
    def isopen(self) -> bool:
        """
        Return True if this table is open
        """
        return False if self._db is None else True

    @wrap_reader
    def records(self, txn: Optional[TXN]=None) -> int:
        """
        Return the number of records in this table

        txn - an transaction to wrap the operation
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        return transaction.stat(self._db).get('entries', 0)

    @wrap_reader
    def stat(self, txn: Optional[TXN]=None) -> int:
        """
        Get the stat() buffer for this table

        txn - an transaction to wrap the operation
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        return transaction.stat(self._db)

    @property
    def read_transaction(self) -> TXN:
        """
        Use with "with" to begin a Read-Only transaction
        """
        # return ReadTransaction(self._database)

        try:
            return self.env.begin()     # TODO: Need multiple processes to test this
        except MapResizedError:         # pragma: no cover
            self.env.set_mapsize(0)     # pragma: no cover
            return self.env.begin()     # pragma: no cover

    @property
    def write_transaction(self) -> TXN:
        """Return a write transaction for this database (compatibility only)"""
        return WriteTransaction(self._database)

    @wrap_reader
    def storage_used(self, txn: Optional[TXN]=None) -> int:
        """
        Return the amount of storage space used by data contained within this table

        txn - optional transaction to wrap this operation
        """
        stat = txn.stat(self._db)
        return stat['psize'] * (stat['leaf_pages'] + stat['branch_pages'] + stat['overflow_pages'] + 2)

    @wrap_writer
    def open(
            self,
            compression_type: Optional[CompressionType]=CompressionType.NONE,
            compression_level: Optional[int]=None,
            codec: SerialiserType=SerialiserType.NONE,
            integerkey: int=False,
            compress_existing: bool=False,
            auditing: bool=False,
            callback: Callable=None,
            txn: Optional[TXN|WriteTransaction]=None) -> Table:
        """
        Open this table and make it available for use, if the compression type is set to
        anything other than NONE, the following the call the table will be set to read and
        write data using the selected compression mechanism, and any data in the table will
        be compressed.

        compression_type - the type of compression to use
        compression_level - the compression level to set
        txn - an optional transaction to wrap this request
        """
        if self.isopen:
            return self

        transaction = txn if isinstance(txn, TXN) else txn.txn
        create = False
        self._compression_type = compression_type
        self._compression_level = compression_level
        self._codec = codec
        self.integerkey = integerkey
        self._auditing = auditing

        if not self.name.startswith('@@') and self._database.index_version == 2:
            self._oid = name = self._database._cat.get_table_id(self.name, txn)
        else:
            self._oid = self.name

        try:
            self._db = self.env.open_db(
                # self.name.encode() if isinstance(self.name, str) else self.name,
                self._oid.encode(),
                create=False,
                integerkey=integerkey,
                txn=transaction)
        except NotFoundError:
            create = True
            self._db = self.env.open_db(
                # self.name.encode(),
                self._oid.encode(),
                integerkey=integerkey,
                txn=transaction)
        except IncompatibleError as e:
            log.error(f'{self.name} => {self._oid}:: {str(e)}')
            return self

        try:
            Serialiser.__init__(self, codec, txn=transaction)
            if not self._meta:
                return self
            for index_name in self.indexes(txn=transaction):
                if index_name in self.data:
                    # means the index is open so we're doing a 're-open'
                    self.data[index_name].open(txn=transaction)  # pragma: no cover
                else:
                    if self._database.index_version == 1:
                        doc = self._meta.fetch_index(self.name, index_name, txn=transaction)
                        if not doc['conf']:
                            break  # pragma: no cover
                        self.__setitem__(index_name, doc['conf'])
                    else:
                        # log.success(f'get meta: {self.name}/{index_name} => {self._database._cat.get_metadata(self.name, index_name)}')
                        self.__setitem__(index_name, self._database._cat.get_metadata(self.name, index_name))
                    
                    self.data[index_name].open(txn=transaction)
            if compression_type and compression_type != CompressionType.NONE:
                do_compress = self.compression_select(compression_type, compression_level, txn=transaction)
                Compression.open(self, txn=transaction)
                if compress_existing and do_compress and self.records(txn=transaction):
                    self.compress_existing_data(txn=transaction)
            else:
                Compression.open(self, txn=transaction)
            if auditing:
                self._database._auditor.watch(self.name, callback)
            
        except Exception:
            try:
                self.close()  # pragma: no cover
            except Exception:  # pragma: no cover
                pass
            raise

        return self

    @wrap_writer
    def droptable(self, txn: Optional[TXN|WriteTransaction]=None) -> None:
        """
        Drop the current table, this will empty the table, remove all the indexes,
        remote the table itself, and remove all associated metadat.

        txn - a write transaction to wrap this operation
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        for index_name in self.data:
            self.data[index_name].drop(txn=txn)

        transaction.drop(self._db, True)
        self._database._cat.drop(self.name, txn)
        # if self._database.index_version == 2:
        #     self._database._catalog.delete(self.name, txn=txn)
        self._meta.remove(self.name, txn=txn)

    def close(self) -> None:
        """
        Close a table by essentially losing all references to it
        """
        # log.error(f'close table: {self.name}')
        # if self._database._auditor:
        #     self._database._auditor.close()
        self._db = None
        self.data.clear()
        Compression.close(self)

    @wrap_writer
    def reopen(
        self,
        auditing: bool=False,
        callback: Callable=None,
        txn: Optional[TXN|WriteTransaction]=None) -> None:
        """
        ReOpen a table, used following a change to the map size. Everything should be the
        same, we just need new database handles.
        """
        self.close()
        self.env = self._database.env
        self.open(
            self._compression_type,
            self._compression_level,
            self._codec,
            self.integerkey,
            auditing = auditing,
            callback = callback,
            txn=txn)

    @wrap_reader_yield
    def indexes(self, txn: Optional[TXN]=None) -> Generator[str, None, None]:
        """
        Generate a list if indexs (names) available for this table

        txn - an optional transaction
        """
        if self.name.startswith('@@'):
            return []
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if self._database.index_version == 1:
            metadata = self._database.table('__metadata__', txn=transaction)
            index_key = Index.index_path(self.name, '')
            offset = len(index_key)
            with transaction.cursor(db=metadata._db) as cursor:
                cursor.set_range(index_key.encode())
                name = cursor.key().decode()
                while name.startswith(index_key):
                    yield name[offset:]
                    if not cursor.next():
                        break  # pragma: no cover
                    name = cursor.key().decode()
        elif self._database.index_version == 2:
            for name in self._database._cat.indexes(self.name, transaction):
                yield name
            # catalog = self._database._catalog.get(self.name, txn=transaction)
            # for name in catalog._indexes or []:
            #     yield name


    @wrap_writer
    def ensure(
            self,
            index_name: str,
            func: str=None,
            duplicates: bool=False,
            force: bool=False,
            lower: bool=False,
            iwx: bool=False,
            progress: Optional[Callable]=None,
            txn: Optional[TXN|WriteTransaction]=None) -> Index:
        """
        Ensure that the specified index exists, if it does by default do nothing. If the
        index does not exist, or if the 'force' flag is true, the index will be (re)created
        using the new index function.

        index_name - the name of the required index
        func - a description of how index keys should be generated
        duplicates - whether this is a duplicate index or not
        force - whether to re-index the index if it already exists
        iwx - true if this index is an inverted word index
        txn - an optional transaction

        The "func" parameter can take one of two forms, it can either be a Python format
        string (the only option in v1) or it can be a complete python function if prefixed
        with a 'def'. So for example as a format string;
        ```
        func = '{name}'         # index by name
        func = '{name}|{age}'   # index by name + age
        func = '{age:03d}'      # index by age with leading zero for correct numerical sort order
        ```
        Or if you want to use a function which allows for more flexibility;
        ```
        func = 'def func(doc): return "{:03d}".format(doc["age"]).encode()'
        ```
        For a complete working example, the natural order is in descending on age,
        but when iterating using either of the example indexes, you should see the order
        as ascending order of age.
        ```
        #!/usr/bin/env python
        from orbit-database import Manager, Doc
        from shutil import rmtree
        rmtree('.database')
        db = Manager().database('database', '.database')
        people = db.table('people')
        people.append(Doc({'name': 'Tom', 'age': 21}))
        people.append(Doc({'name': 'Harry', 'age': 19}))
        people.ensure('by_age_fs', '{age:03d}')
        people.ensure('by_age_func', 'def func(doc): return "{:03d}".format(doc["age"]).encode()')
        [print(person.doc) for person in people.find()]
        print('--')
        [print(person.doc) for person in people.find('by_age_fs')]
        print('--')
        [print(person.doc) for person in people.find('by_age_func')]
        ```
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if self._database.index_version == 2 and iwx:
            if index_name not in self.data or force:
                if index_name in self.data:
                    self.drop(index_name, txn=transaction)

                catalog = self._database._cat.ensure(self.name, index_name, iwx, transaction)
                conf = catalog._indexes[index_name]
                self.__setitem__(index_name, conf)
                self.data[index_name].open(txn=transaction)
            return self.data[index_name]
        #
        #   Abstract get old conf
        #   Abstract store_index
        #

        if self._database.index_version == 1:
            old_conf = self._meta.fetch_index(self.name, index_name, txn=transaction)
            if not old_conf._conf:
                old_conf = {'key': Index.index_path(self.name, index_name)}
            else:
                old_conf = old_conf._conf
        else:
            old_conf = self._database._cat.get_metadata(self.name, index_name)
            if not old_conf:
                old_conf = { 'key': str(ObjectId()) }

        new_conf = {
            'key': old_conf['key'],
            'dupsort': duplicates,
            'create': True,
            'func': func,
            'iwx': iwx,
            'lower': lower
        }
        force = old_conf != new_conf or force
        if index_name not in self.data or force:
            if index_name in self.data:
                self.drop(index_name, txn=transaction)
            self.__setitem__(index_name, new_conf)
            self.data[index_name].open(txn=transaction)
            if force:
                if self._database.index_version == 1:
                    self._meta.store_index(self.name, index_name, Doc({'conf': new_conf}), txn=transaction)
                else:
                    self._database._cat.store_index(self.name, index_name, new_conf, txn=transaction)
                self.reindex(index_name, progress=progress, txn=transaction)
        self.data[index_name].reindexed = force
        return self.data[index_name]

    @wrap_writer
    def reindex(self, index_name: str, progress: Optional[Callable]=None, txn: Optional[TXN]=None) -> None:
        """
        Reindex the named index, assuming the index exists. The index is first emptied
        and then each record is reindexed, for a large table this can take some time
        and will lock the database while in progress.

        index_name - the name of the index to reindex
        txn - a write transaction to wrap the operation
        """
        # log.warning(f'Running reindex for {index_name} in {self.name}')
        if index_name not in self.data:
            raise NoSuchIndex
        transaction = txn if isinstance(txn, TXN) else txn.txn
        self.data[index_name].empty(txn=transaction)
        with transaction.cursor(self._db) as cursor:
            while cursor.next():
                if progress:
                    progress.update(1)  # pragma: no cover
                self.data[index_name].put_cursor(cursor, txn=transaction)

    @wrap_writer
    def append(self, doc: Doc, txn: Optional[TXN|WriteTransaction]=None) -> Doc:
        """
        Append a new record to this table

        doc - the data to append
        txn - an optional transaction object
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if not doc.oid:
            if self.integerkey:
                with transaction.cursor(db=self._db) as cursor:
                    if not cursor.last():
                        oid = 0
                    else:
                        oid = unpack('=Q', cursor.key())[0] + 1
                    doc.oid = pack('=Q', oid)
            else:
                doc.oid = str(ObjectId()).encode()
        transaction.put(doc.oid, self._compressor(doc), db=self._db)
        if self._auditing:
            self._database._auditor.append(self, doc, txn)
        for index_name in self.data:
            self.data[index_name].put(doc, txn=transaction)
        return doc

    @wrap_writer
    def save(self, doc: Doc, txn: Optional[TXN, WriteTransaction]=None) -> None:
        """
        Update the current record in the table

        doc - the record to update
        txn - an optional transaction
        """
        if not doc.oid:
            raise DocumentDoesntExist
        transaction = txn if isinstance(txn, TXN) else txn.txn
        old_doc = Doc(None, doc.oid).get(self, txn=transaction)
        if self._auditing:
            if old_doc:
                self._database._auditor.save(self, old_doc, txn)
            else:
                log.error(f'Audit: no old document for oid: {doc.oid}')
        transaction.put(doc.oid, self._compressor(doc), db=self._db)
        for index_name in self.data:
            self.data[index_name].save(old_doc, doc, txn=transaction)


    @wrap_reader_yield
    def find(
            self,
            index_name: str=None,
            expression: str=None,
            limit: int = MAXSIZE,
            txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Find records in this table either in natural (date) order, or in index order

        index_name - an optional index name for ordering
        expression - the expression to filter the sort on
        limit - the maximum number of records to return
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        #
        with txn.cursor(db) as cursor:
            count = 0
            while count < limit and cursor.next():
                count += 1
                record = cursor.value()
                if index_name:
                    key = record
                    record = txn.get(record, db=self._db)
                else:
                    key = cursor.key()

                record = self._decompressor(record)
                if callable(expression) and not expression(record):
                    continue
                yield Doc(None, key, record)

    @wrap_reader
    def get(self, oid: [bytes, str], txn: Optional[TXN, WriteTransaction]=None) -> Doc:
        """
        Recover a single record from the database based on it's primary key

        oid - primary key of record to recover
        txn - an optional active transaction
        """
        try:
            transaction = txn if isinstance(txn, TXN) else txn.txn
            return Doc(None, pack('=Q', oid) if self.integerkey else oid).get(self, txn=transaction)
        except Exception as e:  # pragma: no cover
            log.exception(e)  # pragma: no cover
            log.error(f'key was: {oid}')  # pragma: no cover

    @wrap_writer
    def delete(self, keyspec: Union[OID, OIDS, Doc], txn: Optional[TXN]=None) -> None:
        """
        Delete one or more records from the database based on a key specification that
        should reference one or more records by primary key.

        keyspec - we accept either a key, a list of keys or a Doc, keys may be str or bytes
        txn - an optional transaction
        """
        if isinstance(keyspec, str):
            keys = [keyspec]
        elif isinstance(keyspec, list):
            keys = keyspec
        elif isinstance(keyspec, Doc):
            keys = [keyspec.oid]
        elif isinstance(keyspec, bytes):
            keys = [keyspec]
        elif isinstance(keyspec, int) and self.integerkey:
            keys = [keyspec]
        else:
            raise InvalidKeySpecifier(keyspec)

        transaction = txn if isinstance(txn, TXN) else txn.txn
        for key in keys:
            if isinstance(key, str):
                key = key.encode()
            doc = self.get(key, txn=transaction)
            if doc:
                transaction.delete(doc.oid, db=self._db)
                # if self.replicated(txn):
                #     txn.journal.append(doc.journal_entry(JournalType.DELETE, self.name))

                if self._auditing:
                    self._database._auditor.delete(self, doc, txn)

                for index_name in self.data:
                    self.data[index_name].delete(doc, txn=transaction)
            else:
                log.error(f'unable to delete key: "{key}" from table "{self.name}"')  # pragma: no cover

    @wrap_writer
    def empty(self, txn: Optional[TXN|WriteTransaction]=None) -> None:
        """
        Remove all data from the current table leaving the indexing structure in-tact

        txn - an optional transaction
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        transaction.drop(self._db, False)

        # if self.replicated(txn):
        #     doc = Doc({
        #         'delete': False
        #     })
        #     txn.journal.append(doc.journal_entry(JournalType.REMOVE, self.name))

        for index_name in self.data:
            self.data[index_name].empty(txn=transaction)

    @wrap_writer
    def drop(self, index_name: str, txn: Optional[TXN, WriteTransaction]=None) -> None:
        """
        Drop an index from the current table

        index_name - the name of the index to drop
        txn - an optional transaction
        """
        if index_name not in self.data:
            raise NoSuchIndex(index_name)

        transaction = txn if isinstance(txn, TXN) else txn.txn
        index = self.data[index_name]
        del self.data[index_name]
        index.drop(txn=transaction)
        self._database._cat.drop_index(self.name, index_name, txn)

    @wrap_reader_yield
    def tail(self, key: Optional[OID]=None, txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Generates a sequence of records starting from the key after the primary key supplied. If no
        key is supplied, all records are returned, if a misssing key is supplied, no records are
        returned. Typically use this against the last-seen key to access new keys since the last
        check.

        key - the key to start from
        txn - an optional transaction

        TODO: add index to allow tailing based on indexes
        """
        with txn.cursor(db=self._db) as cursor:
            if key:
                if not isinstance(key, bytes):
                    key = key.encode()
                #
                #   We need this behaviour, when someone empties the table, tail needs to know
                #   to go back to the start of the table and continue, rather then being left
                #   on a non-existant key forever ...
                #
                if not cursor.get(key):
                    if not cursor.first():
                        return None
                elif not cursor.next():
                    return None

            for key, val in cursor.iternext(keys=True, values=True):
                yield Doc(None, key, self._decompressor(val))

    @wrap_reader
    def first(
            self, index_name: Optional[str]=None,
            doc: Optional[Doc]=None,
            txn: Optional[TXN]=None) -> Optional[Doc]:
        """
        Return the first record in the table or None if there are no records

        index_name - the name of the index to use (defaults to primary)
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        with txn.cursor(db=db) as cursor:
            if not cursor.first():
                return None
            if index_name:
                if doc:
                    index_entry = self.data[index_name].get(doc, txn=txn)
                else:
                    index_entry = cursor.value()
                doc = txn.get(index_entry, db=self._db)
                return Doc(None, cursor.value(), self._decompressor(doc), integerkey=self.integerkey)
            else:
                return Doc(None, cursor.key(), self._decompressor(cursor.value()), integerkey=self.integerkey)

    @wrap_reader
    def last(
            self,
            index_name: Optional[str]=None,
            doc: Optional[Doc]=None,
            txn: Optional[TXN]=None) -> Optional[Doc]:
        """
        Return the last record in the table or None if there are no records

        index_name - the name of the index to use (defaults to primary)
        txn - an optional transaction
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        with transaction.cursor(db=db) as cursor:
            if not cursor.last():
                return None
            if index_name:
                if doc:
                    index_entry = self.data[index_name].get_last(doc, txn=txn)
                    if not index_entry:
                        return None  # pragma: no cover
                else:
                    index_entry = cursor.value()
                doc = transaction.get(index_entry, db=self._db)
                return Doc(None, cursor.value(), self._decompressor(doc), integerkey=self.integerkey)
            else:
                return Doc(None, cursor.key(), self._decompressor(cursor.value()), integerkey=self.integerkey)

    @wrap_reader_yield
    def range(
            self,
            index_name: Optional[str]=None,
            lower: Optional[Doc]=None,
            upper: Optional[Doc]=None,
            keyonly: bool=False,
            inclusive: bool=True,
            limit: int=MAXSIZE,
            page_number: int=0,
            nodups: bool=False,
            txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Find all records within a range of keys, optionally including keys at each end
        and optionally returning just the keys rather than the entire record.

        index_name - an optional index name, if no index is supplied, use primary keys
        lower - the record at the lower end of the range
        upper - the record at the upper end of the range
        keyonly - if set to True, only returns keys rather than the entire records
        inclusive - if set to True, include the keys at each end, i.e. use <=|=> rather than <|>
        limit - maximum number of records to return
        page_number - index of the page (starts from 0) with a size `limit` to return results from
        nodups - no duplicate keys, return only unique key values and ignore duplicates
        txn - an optional transaction
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex()
            index = self.data[index_name]
            db = index._db

            lower_keys = index.map_key(lower) if lower else [None]
            upper_keys = index.map_key(upper) if upper else [None]

            if not isinstance(lower_keys, list):
                lower_keys = [lower_keys]
            if not isinstance(upper_keys, list):
                upper_keys = [upper_keys]

        else:
            db = self._db
            lower_keys = [lower.oid] if lower else [None]
            upper_keys = [upper.oid] if upper else [None]

        skip = page_number * limit

        with transaction.cursor(db) as cursor:
            for lower_key in lower_keys:
                upper_key = upper_keys.pop(0)
                next_record = cursor.next_nodup if nodups else cursor.next
                cursor.set_range(lower_key) if lower_key else cursor.first()
                if cursor.key() == lower_key and not inclusive:
                    next_record()
                count = 0
                while cursor.key() and count < limit:
                    if upper_key and (cursor.key() > upper_key or (cursor.key() == upper_key and not inclusive)):
                        break
                    if skip:
                        skip -= 1
                    else:
                        count += 1
                        if not index_name:
                            yield cursor.key().decode() if keyonly else Doc(None,
                                cursor.key(), self._decompressor(cursor.value()))
                        else:
                            yield Cursor(index, cursor) if keyonly else Doc(
                                None, cursor.value()).get(self, txn=transaction)
                    next_record()

    @wrap_reader
    def seek_one(self, index_name: str, doc: Doc, txn: Optional[TXN]=None) -> Doc:
        """
        Find the first matching record from an index

        index_name - the name of the index to search
        doc - the template record to find
        txn - an optional transaction
        """
        txn = txn if isinstance(txn, TXN) else txn.txn
        if index_name not in self.data:
            raise NoSuchIndex()
        index_entry = self.data[index_name].get(doc, txn=txn)
        return self._cls(None, index_entry).get(self, txn=txn) if index_entry else None

    def seek(
            self,
            index_name: str,
            doc: Doc,
            limit: int=MAXSIZE,
            page_number: int=0,
            keyonly: bool = False,
            txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Return a selection of records from the selected table matching the template record provided in "doc".
        Should return a maximum of 1 record for unique indexes.
        index_name - the name of the index to search
        doc - the template record to find
        limit - the maximum number of results to return
        page_number - index of the page (starts from 0) with a size `limit` to return results from
        keyonly - return a Cursor object relating to the key instead of the data item
        txn - an optional transaction
        """
        return self.range(
            index_name=index_name,
            lower=doc,
            upper=doc,
            limit=limit,
            page_number=page_number,
            keyonly=keyonly,
            txn=txn)

    @wrap_reader_yield
    def filter(
            self,
            index_name: Optional[str]=None,
            lower: Optional[Doc]=None,
            upper: Optional[Doc]=None,
            expression: Optional[Callable[[Doc], bool]]=None,
            context: Optional[FilterResult]=None,
            page_size: Optional[int]=0,
            inclusive: Optional[bool]=True,
            suppress_duplicates: Optional[bool]=False,
            reverse: Optional[bool]=False,
            txn: Optional[TXN]=None) -> Generator[FilterResult, None, None]:
        """
        Filter the table specified based on a criteria defined by the parameters passed.

        * Paging  To use the paging function, you need to supply both a page_size and context. If the
                  context is None and the page_size is positive, paging will start from the begininning
                  of theindex, and if the context is None and the page size is negative, paging will start
                  from the end. A positive page_size moves forwards through the index based on the context
                  and a negative page size moves backwards. For forward paging, the context will be the
                  last result from the previous page, and for moving backwards, the context will be the
                  first result from the previous page.
        * lambda  The "expression" parameter should be a lambda (or function) which will receive the
                  document and return a True/False based on whether the document should be included in
                  the search results. For example;
        ```
            filter(expression=lambda doc: doc['age'] > 19)
        ```

        index_name - the name of an index to search on, or None to use the primary key
        lower - the record at the lower end of the range
        upper - the record at the upper end of the range
        expression - an lambda expression to filter the results
        context - a paging context to determine where to start tge next page (see comments)
        page_size - maximum number of records to return
        inclusive - if set to True, include the keys at each end, i.e. use <=|=> rather than <|>
        suppress_duplicates - no duplicate keys, return only unique key values and ignore duplicates
        reverse - navigate the index in reverse order
        txn - an optional transaction
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if index_name is not None:
            if index_name not in self.data:
                raise NoSuchIndex()
            index = self.data[index_name]
            db = index._db
            lower_keys = index.map_key(lower) if lower else [None]
            upper_keys = index.map_key(upper) if upper else [None]
            if not isinstance(lower_keys, list):
                lower_keys = [lower_keys]
            if not isinstance(upper_keys, list):
                upper_keys = [upper_keys]
        else:
            db = self._db
            index = None
            lower_keys = [None] if lower is None else [lower.oid]
            upper_keys = [None] if upper is None else [upper.oid]

        with transaction.cursor(db) as cursor:
            next_record = cursor.next_nodup if suppress_duplicates else cursor.next
            prev_record = cursor.prev_nodup if suppress_duplicates else cursor.prev
            if reverse:
                prev_record, next_record = next_record, prev_record
                lower_keys, upper_keys = upper_keys, lower_keys
                first = cursor.last
                greater_than = less
                less_than = greater
            else:
                first = cursor.first
                greater_than = greater
                less_than = less

            for lower_key in lower_keys:
                upper_key = upper_keys.pop(0)
                if index is None:
                    if not context:
                        first()
                    else:
                        cursor.set_key(context._oid)
                        if not next_record():
                            return
                else:
                    if not context:
                        if lower_key is None or not cursor.set_range(lower_key):
                            first()
                        else:
                            # welcome to duplicate key hell!
                            # if in reverse mode, for duplicates we're on the first matching dup
                            # and we need to be on the last, so skip to the next non-dup, then skip
                            # back 1. If next nodup failes, we're at the end of the index ...
                            if reverse:
                                cursor.last_dup()
                                if cursor.key() != upper_key:
                                    cursor.prev_nodup()
                    else:
                        if index.duplicates:
                            cursor.set_key_dup(context.key, context._oid)
                        else:
                            cursor.set_key(context.key)
                        if not next_record():
                            return

                if lower_key:
                    if cursor.key() and (less_than(cursor.key(), lower_key) or (cursor.key() == lower_key and not inclusive)):
                        next_record()
                        if cursor.key() and less_than(cursor.key(), lower_key):
                            return

                results = 0
                while cursor.key() and not (page_size and results == page_size) and not (
                    upper_key and (greater_than(cursor.key(), upper_key) or (cursor.key() == upper_key and not inclusive))):
                    result = FilterResult(self, index, cursor, txn=transaction)
                    if not callable(expression) or expression(result.doc):
                        results += 1
                        yield result
                    next_record()

    @wrap_reader_yield
    def match(
            self,
            index_name: str = None,
            text: str = None,
            start: Optional[int] = 0,
            limit: Optional[int] = 0,
            countonly: bool=False,
            txn: Optional[TXN]=None) -> Generator[MatchResult, None, None]:
        """
        """
        if index_name is None or index_name not in self.data:
            raise NoSuchIndex()  # pragma: no cover
        index = self.data[index_name]
        transaction = txn if isinstance(txn, TXN) else txn.txn
        return index.ftx_query(text, start, limit, countonly, txn=transaction)

    @wrap_reader
    def lexicon(
            self,
            index_name: str = None,
            text: str = None,
            max: int=0,
            txn: Optional[TXN]=None) -> Generator[(str, int), None, None]:
        """
        """
        if index_name is None or index_name not in self.data:
            raise NoSuchIndex()  # pragma: no cover
        index = self.data[index_name]
        transaction = txn if isinstance(txn, TXN) else txn.txn
        return index.iwx_lexicon(text, max=max, txn=transaction)

    def dump(self, index_name, debug=False):
        """
        """
        index = self.data[index_name]
        return index.dump(debug)

    def watch(self, callback: Callable=None, txn: Optional[TXN|WriteTransaction]=None) -> None:
        self._database._auditor.watch(self.name, callback)

    def unwatch(self, callback: Callable=None, txn: Optional[TXN|WriteTransaction]=None) -> None:
        self._database._auditor.unwatch(self.name, callback)

    def export_to_file (self, filename, force=False):
        path = Path(filename)
        if path.exists() and not force:
            raise FileExistsError
        with open(filename, 'w') as io:
            count = 0
            io.write('{\n')
            for result in self.filter():
                if count: io.write(',\n')
                io.write('  "' + result.doc.key + '": ')
                dump(result.doc.doc, io)
                count += 1
            io.write('\n}\n')
        return count

    def import_from_file (self, filename):
        path = Path(filename)
        if not path.exists():
            raise FileNotFoundError
        with open(filename, 'r') as io:
            data = load(io)
            for key in data:
                doc = Doc(dict(data[key], **{'key': key}))
                self.append(doc)
        return len(data)
