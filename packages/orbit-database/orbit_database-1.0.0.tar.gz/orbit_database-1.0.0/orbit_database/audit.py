from enum import Enum
from uuid import uuid4 as get_uuid
from posix_ipc import Semaphore, ExistentialError, O_CREAT, SignalError
from time import sleep as sync_sleep
from threading import Thread
from orbit_database.doc import Doc
from orbit_database.serialiser import SerialiserType
from struct import pack, unpack
from time import sleep
from getpass import getuser
import asyncio
import hashlib

try:
    from loguru import logger as log
except Exception:
    import logging as log


class AuditEntry(Enum):
    """
    """
    NONE = 0
    APPEND = 1
    SAVE = 2
    DELETE = 3


class Auditor:

    UUID_KEY = '__uuid__'
    MAX_DOCS = 250

    @property
    def uuid (self):
        return self._uuid
    
    def __init__(self, database):
        self._database = database
        self._thread = None
        self._table = None
        self._uuid = None
        self._semaphore = None
        self._handlers = {}
        self._finished = False
        self._auditing = False
        self._tasks = []

    def open(self, auditing=False):
        # doc = self._database.meta.fetch_key(self.UUID_KEY)
        # if doc:
        #     self._uuid = doc._uuid
        # else:
        #     self._uuid = f'{getuser()}_{self._database._name}'
        #     self._database.meta.store_key(self.UUID_KEY, Doc({'uuid': self._uuid}))
        #
        #   Needs to be unique based on path + user ... metadata is an overcomplication
        #
        hObj = hashlib.new('sha1')
        hObj.update(str(self._database._path).encode())
        self._uuid = hObj.hexdigest()
        if self._database.index_version == 1:
            audit_table_name = '__audit_table__'
        elif self._database.index_version == 2:
            audit_table_name = '@@audit_table@@'

        self._table = self._database.table(audit_table_name)
        try:
            self._semaphore = Semaphore(f'/{self._uuid}', flags=O_CREAT)
        except (ExistentialError, ValueError) as e:                   # pragma: no cover
            raise Exception(f'audit error: {str(e)} // {self._uuid}')   # pragma: no cover
        self._auditing = auditing                   
        if auditing:
            self._finished = False
            self._thread = Thread(target=self.callback, args=(asyncio.get_event_loop(),), daemon=True)
            self._thread.start()
        return self

    def callback (self, loop) -> None:
        try:
            while True:
                self._semaphore.acquire()
                if self._finished:
                    break
                while self._table.records():
                    self.flush(loop)
        except KeyboardInterrupt:       # pragma: no cover
            pass                        # pragma: no cover
        except Exception as e:          # pragma: no cover
            log.exception(e)            # pragma: no cover
        finally:
            self._semaphore.close()
            self._table.close()
       
    def flush (self, loop):
        while True:
            results = {}
            to_delete = []
            for result in self._table.filter(page_size=self.MAX_DOCS):
                try:
                    if result.doc._t not in results:
                        results[result.doc._t] = []
                    event = result.doc
                    results[result.doc._t].append(event)
                    to_delete.append(event.key)
                except UnicodeDecodeError:
                    log.error(f'failed to remove audit entry: {event.oid}')
            for table, events in results.items():
                try:
                    if table not in self._handlers:
                        asyncio.run_coroutine_threadsafe(self.default_handler(table, events), loop)
                    else:               
                        for fn in self._handlers[table]:
                            asyncio.run_coroutine_threadsafe(fn(events), loop)
                except Exception as e:      # pragma: no cover
                    log.exception(e)        # pragma: no cover
            self._table.delete(to_delete)
            if len(results) < self.MAX_DOCS:
                break
            
    async def default_handler(self, table, docs):
        # log.warning(f'Handlers2> {table} => {self._handlers.keys()} {table in self._handlers}')
        for doc in docs:
            log.success(f'default[{table}]: {str(doc.doc)}')
            
    def close(self):
        # log.error('** CLOSE AUDIT **')
        self._finished = True
        self._semaphore.release()
        return self
            
    def watch(self, table, callback):
        if callback:
            if table not in self._handlers:
                self._handlers[table] = []
            self._handlers[table].append(callback)
        return self
    
    def unwatch(self, table, callback):
        if table in self._handlers:
            self._handlers[table] = list(filter(lambda entry: entry != callback, self._handlers[table]))
        return self

    def save(self, table, doc, txn):
        return self.put(table, doc, AuditEntry.SAVE.value, transaction=txn)

    def delete(self, table, doc, txn):
        return self.put(table, doc, AuditEntry.DELETE.value, transaction=txn)

    def append(self, table, doc, txn):
        return self.put(table, doc, AuditEntry.APPEND.value, transaction=txn)
    
    def put(self, table, doc, type, transaction=None):
        if not transaction._semaphore:
            transaction._semaphore = self._semaphore
        with transaction.txn.cursor(db=self._table._db) as cursor:
            if not cursor.last():
                oid = 0
            else:
                try:
                    oid = unpack('=Q', cursor.key())[0] + 1
                except Exception as e:                                          # pragma: no cover
                    log.exception(e)                                            # pragma: no cover
                    log.error(f'Key={cursor.key()} / {cursor.value()}')         # pragma: no cover
                    return
            oid = pack('=Q', oid)
            record = Doc({
                't': table.name,
                'o': doc.oid.decode(),
                'e': type,
                'c': '' if table.codec == SerialiserType.RAW else doc.doc
            })
            transaction.txn.put(oid, self._table._compressor(record), db=self._table._db)
    