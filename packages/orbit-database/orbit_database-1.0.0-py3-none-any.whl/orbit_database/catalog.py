from lmdb import Transaction, NotFoundError
from orbit_database.table import Table
from orbit_database.doc import Doc
from orbit_database.objectid import ObjectId
from orbit_database.exceptions import NoSuchIndex
from orbit_database.metadata import MetaData

class Catalog:

    @property
    def version (self):
        return self._version

    def __init__(self, version):
        self._table = None
        self._version = version

    def open (self, database, txn=None):
        if not self._version:
            self._version = 1
            try:
                database.env.open_db(b'@@catalog@@', create=False, txn=txn)
                self._version = 2
            except NotFoundError:
                if txn.stat(database._db).get('entries', 0) == 0:
                    self._version = 2
                    database.env.open_db(b'@@catalog@@', create=True, txn=txn)
        if self._version == 2:
            self._table = Table(database, '@@catalog@@', CatalogEntry).open(txn=txn)
        return self
   
    def drop (self, name, txn):
        if self._version == 2:
            self._table.delete(name, txn=txn)

    def drop_index (self, table_name, index_name, txn):
        if not table_name.startswith('@@') and self._version == 2:
            catalog = self._table.get(table_name, txn=txn)
            if not catalog or not catalog._indexes:
                raise Exception(NotFoundError)
            if index_name not in catalog._indexes:
                raise Exception(NoSuchIndex)
            catalog._indexes.pop(index_name)
            self._table.save(catalog, txn=txn)

    def indexes (self, name, txn):
        catalog = self._table.get(name, txn=txn)
        if catalog:
            for name in catalog._indexes or []:
                yield name

    def ensure (self, table_name, index_name, iwx, txn):
        catalog = self._table.get(table_name, txn=txn)
        if not catalog:
            raise Exception(NotFoundError)
        if not catalog._indexes:
            catalog._indexes = {}
        if index_name not in catalog._indexes:
            if iwx:
                catalog._indexes[index_name] = {
                    'iwx': True,
                    'lexicon': str(ObjectId()),
                    'docindx': str(ObjectId()),
                    'docrindx': str(ObjectId()),
                    'bitmap': str(ObjectId()),
                    'words': str(ObjectId())
                }
            else:
                catalog._indexes[index_name] = {
                    'key': str(ObjectId())
                }
            self._table.save(catalog, txn=txn)
        return catalog
    
    def store_index (self, table_name, index_name, conf, txn=None):
        catalog = self._table.get(table_name, txn=txn)
        if not catalog:
            raise Exception(NotFoundError)
        if not catalog._indexes:
            catalog._indexes = {}
        catalog._indexes[index_name] = conf
        self._table.save(catalog, txn=txn)

    def get_metadata (self, table_name, index_name, txn=None):
        catalog = self._table.get(table_name, txn=txn)
        if not catalog:
            raise Exception(NotFoundError)
        if not catalog._indexes:
            catalog._indexes = {}
        return catalog._indexes.get(index_name, {})

    def get_table_id (self, name, txn):
        doc = self._table.get(name)
        if not doc:
            doc = Doc({'id': str(ObjectId())}, oid=name)
            self._table.append(doc, txn=txn)
        return doc._id


class CatalogEntry (Doc):
    pass
