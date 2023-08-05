#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from pathlib import Path
from collections import UserDict
from lmdb import Environment, Transaction as TXN, MapResizedError, NotFoundError
from typing import Optional, Generator, Dict, Callable, ClassVar, Tuple
from orbit_database.doc import Doc
from orbit_database.table import Table
from orbit_database.audit import Auditor
from orbit_database.serialiser import SerialiserType
from orbit_database.compression import CompressionType
from orbit_database.decorators import wrap_reader_yield, wrap_reader, WriteTransaction, transparent_resize
from orbit_database.exceptions import NoSuchTable
from orbit_database.types_ import Config
from orbit_database.metadata import MetaData
from orbit_database.catalog import Catalog, CatalogEntry

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover


class Database(UserDict):
    """
    The Database object models the top-level container for a collection of tables and indexes, each Database
    object maps to an LMDB database object. When you open a database there are a variety of low-level (LMDB)
    database settings that can be applied, it's worth understanding what some of them do as when you come to
    productionise your system, they will make a difference. Specifically you will want to tweak 'map_size'
    which is the maximum allowable size of your database, and possibly max_dbs if you are going to open large
    numbers of tables at the same time.
    ---
    sync:        If False, don’t flush system buffers to disk when committing a transaction. This optimization means
                 a system crash can corrupt the database or lose the last transactions if buffers are not yet flushed
                 to disk. The risk is governed by how often the system flushes dirty buffers to disk and how often
                 sync() is called. However, if the filesystem preserves write order and writemap=False, transactions
                 exhibit ACI (atomicity, consistency, isolation) properties and only lose D (durability). I.e.
                 database integrity is maintained, but a system crash may undo the final transactions. Note that
                 sync=False, writemap=True leaves the system with no hint for when to write transactions to disk,
                 unless sync() is called. map_async=True, writemap=True may be preferable.

    lock:        If False, don’t do any locking. If concurrent access is anticipated, the caller must manage all
                 concurrency itself. For proper operation the caller must enforce single-writer semantics, and must
                 ensure that no readers are using old transactions while a writer is active. The simplest approach is
                 to use an exclusive lock so that no readers may be active at all when a writer begins.

    subdir:      If True, path refers to a subdirectory to store the data and lock files in, otherwise it refers to
                 a filename prefix.

    create:      False, do not create the directory path if it is missing.

    writemap:    If True, use a writeable memory map unless readonly=True. This is faster and uses fewer mallocs, but
                 loses protection rom application bugs like wild pointer writes and other bad updates into the database.
                 Incompatible with nested transactions. Processes with and without writemap on the same environment do
                 not  cooperate well.

    metasync:    If False, flush system buffers to disk only once per transaction, omit the metadata flush. Defer that
                 until the system flushes files to disk, or next commit or sync(). This optimization maintains database
                 integrity, but a system crash may undo the last committed transaction. I.e. it preserves the ACI
                 (atomicity, consistency, isolation) but not D (durability) database property.

    readahead:   If False, LMDB will disable the OS filesystem readahead mechanism, which may improve random read
                 performance when a database is larger than RAM.

    map_async:   When writemap=True, use asynchronous flushes to disk. As with sync=False, a system crash can then
                 corrupt the database or lose the last transactions. Calling sync() ensures on-disk database integrity
                 until next commit.

    max_readers: Maximum number of simultaneous read transactions. Can only be set by the first process to open an
                 environment, as it affects the size of the lock file and shared memory area. Attempts to
                 simultaneously start more than this many readtransactions will fail.

    max_dbs:     Maximum number of databases available. If 0, assume environment will be used as a single database.

    map_size:    Maximum size database may grow to; used to size the memory mapping. If database grows larger than
                 map_size, an exception will be raised and the user must close and reopen Environment. On 64-bit there
                 is no penalty for making this huge (say 1TB). Must be <2GB on 32-bit.
    ---
    Default values for these settings come from the CONFIG class variable, please note that currently we do NOT
    support the 'readonly' option. It does not appear that this option works properly with transactions on sub-databases
    and until we can work out why, please avoid read-only databases.
    """

    CONFIG = {
        'sync': True,
        'lock': True,
        'subdir': True,
        'create': True,
        'writemap': True,
        'metasync': False,
        'readahead': True,
        'map_async': True,
        'max_readers': 512,
        'max_dbs': 512,
        # 'map_size': 2147483648
    }

    @property
    def auditor (self):
        return self._auditor

    def __init__(self) -> None:
        """
        Initialise this object
        """
        super().__init__()
        self.reset()
        
    def reset (self):
        self.meta = None
        self.auto_resize = False
        self._conf = dict(self.CONFIG)
        self._auditor = None
        self._auditing = None
        # self._index_version = 1
        # self._catalog = None
        self._path = None
        self._cat = None
        self._db = None
        self.env = None
        self.data = {}

    def __getitem__(self, name: str) -> Table:
        """
        Shortcut to self.table

        name - the name of the table to recover
        """
        if name not in self.data:
            self.data[name] = Table(self, name)
        return self.data[name]

    def __repr__(self) -> str:
        """
        Return a string representation of a Database object
        """
        return f'<{__name__}.Database instance> path="{self._path}" status={"open" if self.isopen else "closed"}'

    def table(self,
              table_name: str,
              codec: SerialiserType=SerialiserType.NONE,
              compression_type=CompressionType.NONE,
              compression_level=None,
              integerkey: bool=False,
              auditing: bool=False,
              callback: Callable=None,
              txn: Optional[TXN]=None,
              cls: Optional[Doc]=Doc,
              defer: Callable=False) -> Table:
        """
        Returns the table associated with the supplied name

        table_name - the name of the table to recover
        """
        if table_name not in self.data:
            cls.table = self.data[table_name] = Table(self, table_name, cls)
        if not defer:
            cls.table = self.data[table_name]
            if not self.data[table_name].isopen:
                self.data[table_name].open(
                    codec=codec,
                    compression_type=compression_type,
                    compression_level=compression_level,
                    integerkey=integerkey,
                    auditing=auditing,
                    callback=callback,
                    txn=txn)
        return self.data[table_name]

    @property
    def isopen(self) -> bool:
        """
        Return True is the database is currently open
        """
        return True if hasattr(self, '_db') and self._db else False

    @property
    def map_size(self) -> int:
        """
        Return the currently mapped database size
        """
        return self.env.info()['map_size']

    @wrap_reader
    def storage_used(self, txn: Optional[TXN]=None) -> Tuple[int, Dict[str, int]]:
        """
        Return a tuple that represents the amount of storage space consumed by this database.
        The first entry in the tuple is the number of bytes occupied by data, the second is
        a tuple representing the size (in bytes) and name of each table in the database.

        txn - an optional transaction to wrap this operation
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        total_bytes = 0
        results = {}
        for name in self.tables(all=True, txn=transaction):
            used = self.table(name).storage_used()
            total_bytes += used
            results[name] = used
        return total_bytes, results

    @property
    def storage_allocated(self):
        """
        Return the amount of storage space pre-allocated to this database, assuming the
        underlying filesystem supports 'sparse' storage, this allocation will not reflect
        the amount of disk space 'actually' used. (see 'storage_used')
        """
        path = Path(self._path) / ("data.mdb" if self._conf.get('subdir') else "")
        return path.stat().st_size

    @wrap_reader_yield
    def tables(self, all: bool=False, txn: Optional[TXN]=None) -> Generator[str, None, None]:
        """
        Generate a list of tables available in this database

        all - if True also show hidden / structural tables
        txn - an optional transaction
        """
        if self.index_version == 1:
            transaction = txn if isinstance(txn, TXN) else txn.txn
            with transaction.cursor(self._db) as cursor:
                while cursor.next():
                    try:
                        name = cursor.key().decode()
                    except UnicodeDecodeError:
                        continue
                    if (name[0] not in ['_', '~', '@']) or all:
                        yield name
        elif self.index_version == 2:
            if all:
                transaction = txn if isinstance(txn, TXN) else txn.txn
                with transaction.cursor(self._db) as cursor:
                    while cursor.next():
                        try:
                            name = cursor.key().decode()
                        except UnicodeDecodeError:
                            continue
                        if name.startswith('@@'):
                            yield name
            for result in self.table('@@catalog@@').filter():
                yield result.oid.decode()

    def sync(self, force: bool=True) -> None:
        """
        Force a database sync

        force - if True make the flush synchronous
        """
        self.env.sync(force)

    # @property
    # def name(self):
    #     """Return the unique name (uuid) of this database for replication"""
    #     return self.replication.uuid

    @property
    def index_version (self) -> int:
        return self._cat.version if self._cat else 0

    @property
    def write_transaction(self) -> TXN:
        """Return a write-transaction for this database"""
        return WriteTransaction(self)

    @property
    def read_transaction(self) -> TXN:
        """
        Return a read-only transaction for use with "with"
        """
        try:
            return self.env.begin()  # TODO: need multiple processes to test this
        except MapResizedError:      # pragma: no cover
            self.env.set_mapsize(0)  # pragma: no cover
            return self.env.begin()  # pragma: no cover

    def configure(self, config: Config) -> Database:
        """
        Adjust the database configuration
        Return a reference to the current database instance
        """
        if not config:
            config = {}
        else:
            config = dict(config)
        if 'auditing' in config:
            self._auditing = config.get('auditing')
            del config['auditing']
            
        self.auto_resize = config.get('auto_resize', False)

        for param in ['replication', 'journal', 'auto_resize', 'defer_fulltext', 'reindex', 'auditing', 'version']:
            # log.debug(f'Setting: flag_{param} = {config.get(param, False)}')
            if param in config:
                setattr(self, f'flag_{param}', config.get(param, False))
            if param in config:
                del config[param]

        self._conf = dict(self._conf, **config)
        return self

    def open(self, path: str, name: str=None) -> Database:
        """
        Open the database

        path - the location of the database files

        Returns a reference to the Database object
        """
        if self.isopen:
            return self
        self._path = path
        self._name = name
        self.env = Environment(path, **self._conf)
        self._cat = Catalog(getattr(self, 'flag_version', None))
        self._db = self.env.open_db()
        with TXN(env=self.env, write=True) as txn:
            self._cat.open(self, txn=txn)
            self.meta = MetaData(self).open(txn=txn)
        self._auditor = Auditor(self).open(self._auditing)
        return

    def close(self) -> None:
        """Close this database if it is open"""
        if self._auditor:
            self._auditor.close()
            self._auditor = None
        if self.isopen:
            try:
                for table_name in list(self.tables()):
                    if table_name in self.data:
                        if self.data[table_name].isopen:
                            self.data[table_name].close()
            except Exception as e:
                log.warning(f'unable to close all tables: {str(e)}')
                log.exception(e)
        if hasattr(self, 'env') and self.env:
            self.env.close()
        self.reset()

    def reopen(self) -> None:
        """
        Reopen a database and all of it's tables

        After calling set_mapsize to resize the database, individual database handles
        are potentially invalidated, hence the save option is to reopen everything.
        """
        @transparent_resize
        def openup(db, txn=None):
            self._db = self.env.open_db()
            if self.meta:
                self.meta.reopen(txn=txn)

        # self.open(self._path)
        openup(self)
        for table_name, table in self.data.items():
            table.reopen()

    def drop(self, name: str, txn: Optional[TXN]=None) -> None:
        """
        Drop (delete) a database table

        name - name of table to drop
        txn - an optional transaction
        """
        if name not in self.data:
            raise NoSuchTable
        self.data[name].droptable(txn=txn)
        del self.data[name]

    def register_norm(self, cls: Doc, nogql: Optional[Doc]=None, audit: bool=False, gpg=None):
        cls.reset(self, nogql, audit, gpg)

    def drop_obsolete_indexes(self):
        for table_name in self.tables():
            log.warning(f'> Table > {table_name}')
            table = self.table(table_name)
            for index_name in table:
                log.success(f'> Index > {index_name}')
                index = table[index_name]
                if not hasattr(index, 'reindexed'):
                    log.error(f'Dead Index: {index_name}')