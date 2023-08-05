#####################################################################################
#
#  Copyright (c) 2021 - Mad Penguin Consulting Ltd
#
#####################################################################################
#
#   InvertedWordIndex has two dicrete indexes;
#   a. Lookup by word (inverted index)
#   b. Lookup by document (forward index)
#
#   (a) Will use raw LMDB duplicate indexes, whereas (b) will be a sparse bitmap index
#
from collections import Counter
from struct import pack, unpack
from lmdb import Transaction, Cursor, BadValsizeError
from typing import List
from orbit_database.doc import Doc
from orbit_database.bitmap import Bitmap
from orbit_database.decorators import wrap_writer
from ujson import loads, dumps
from functools import wraps
from time import time
from os import times

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover


class InvertedWordIndex:

    REMOVE_TOKENS = ['iwx']
    MAX_WORDS = 65535
    MAX_WORD_SIZE = 128
    BITMAP_CHUNK = 1000

    def __init__(self, config=None):
        """
        Only initialise if we are a full-text index
        """
        config = getattr(self, '_conf', config or {})
        self._iwx = config.get('iwx')
        self._iwx_cache = None
        for token in dict(config):
            if token in self.REMOVE_TOKENS:
                del config[token]
        self._lexicon = None
        self._docindx = None
        self._docrindx = None
        self._bitmap = None
        self._words = None
        self._map = None

    def open(self, txn: Transaction) -> None:
        if self._iwx:
            if not hasattr(self, 'name') or self._table._database.index_version == 1:
                self._lexicon = self.env.open_db(key=self.iwx_path('lexicon'), txn=txn)
                self._docindx = self.env.open_db(key=self.iwx_path('docindx'), txn=txn)
                self._docrindx = self.env.open_db(key=self.iwx_path('docrindx'), txn=txn)
                self._bitmap = self.env.open_db(key=self.iwx_path('bitmap'), txn=txn)
                self._words = self.env.open_db(key=self.iwx_path('words'), txn=txn)
            else:
                index_name = self.name
                table_name = self._table.name
                catalog = self._table._database._cat
                conf = catalog.get_metadata(table_name, index_name, txn=txn)
                self._lexicon = self.env.open_db(conf['lexicon'].encode(), txn=txn)
                self._docindx = self.env.open_db(conf['docindx'].encode(), txn=txn)
                self._docrindx = self.env.open_db(conf['docrindx'].encode(), txn=txn)
                self._bitmap = self.env.open_db(conf['bitmap'].encode(), txn=txn)
                self._words = self.env.open_db(conf['words'].encode(), txn=txn)

            self._map = Bitmap(self._bitmap)
            return True
        return False

    def empty(self, txn: Transaction) -> None:
        if not self._iwx:
            return False
        return self.iwx_empty(txn, False)

    def drop(self, txn: Transaction) -> None:
        if not self._iwx:
            return False
        txn.drop(self._words, delete=True)
        return self.iwx_empty(txn, True)       

    def save(self, old_doc, new_doc, txn):
        if not self._iwx:
            return False
        Lexicon(self).from_oid(old_doc.oid, transaction=txn).delete(txn)
        # self.iwx_delete(old_doc.oid, txn)
        self.put(new_doc, txn)
        return True

    def delete(self, doc, txn: Transaction):
        if not self._iwx:
            return False
        # self.iwx_delete(doc.oid, txn)
        Lexicon(self).from_oid(doc.oid, transaction=txn).delete(txn)
        return True

    def put(self, doc, txn: Transaction):
        if not self._iwx:
            return False
        # log.warning(f'PUT: {doc.oid} => {doc.words}')
        self.write(doc.oid, doc.words, txn=txn)
        return True

    def put_cursor(self, cursor: Cursor, txn: Transaction) -> None:
        """
        Put a new index entry based on a Cursor rather than a Doc object. This is here
        mainly to make "reindex" more elegant / readable.

        cursor - an LMDB Cursor object
        txn - an optional transaction
        """
        if not self._iwx:
            return False
        self.write(cursor.key(), None, txn=txn)
        return True
    
    def write(self, oid: str, words: List[dict], txn: Transaction):
        transaction = txn if isinstance(txn, Transaction) else txn.txn
        if not words:
            lexicon = Lexicon(self).from_oid(oid, transaction=transaction)
        else:
            lexicon = Lexicon(self).from_words(oid, words, transaction=transaction)
        lexicon.update_words(transaction=transaction)
        if words:
            txn.put(oid, dumps(words).encode(), db=self._words)

    def iwx_counts(self, txn: Transaction):
        txn = txn if isinstance(txn, Transaction) else txn.txn
        return {
            'lexicon':  txn.stat(self._lexicon).get('entries', 0),
            'docindx':  txn.stat(self._docindx).get('entries', 0),
            'docrindx': txn.stat(self._docrindx).get('entries', 0),
            'bitmap':   txn.stat(self._bitmap).get('entries', 0),
            'words':    txn.stat(self._words).get('entries', 0)
        }

    def iwx_empty_words(self, txn: Transaction, delete=False) -> None:
        if self._iwx:
            txn = txn if isinstance(txn, Transaction) else txn.txn
            txn.drop(self._words, delete=False)
            return True
        return False

    def iwx_empty(self, txn: Transaction, delete=False) -> None:
        if self._iwx:
            txn = txn if isinstance(txn, Transaction) else txn.txn
            txn.drop(self._lexicon, delete=delete)
            txn.drop(self._bitmap, delete=delete)
            txn.drop(self._docindx, delete=delete)
            txn.drop(self._docrindx, delete=delete)
            return True
        return False

    def iwx_path(self, name: str) -> str:
        """
        Produce the path for a supplementary table
        """
        if hasattr(self, '_table'):
            return f'_{self._table.name}={self.name}={name}'.encode()
        else:
            return f'_pytest=pytest={name}'.encode()

    def iwx_oids(self, txn: Transaction):
        return txn.stat(self._docindx).get('entries', 0)

    def resolve_idoc(self, idoc, txn):
        key = pack('>L', idoc)
        doc = txn.get(key, db=self._docrindx)
        if not doc:
            return None
        return doc

    def iwx_get_words(self, oid):
        with self.env.begin(db=self._words) as txn:
            raw = txn.get(oid, db=self._words)
            return loads(raw) if raw else []

    def iwx_put_words(self, oid, words):
        with self.env.begin(db=self._words, write=True) as txn:
            try:
                txn.put(oid, dumps(words).encode(), db=self._words)
            except BadValsizeError:
                log.error(f'issue with key or words, key={oid} words={words}')
                log.error('record not indexed!!')

    def iwx_space(self, stat, suffix='B'):
        num = stat['psize'] * (stat['leaf_pages'] + stat['branch_pages'] + stat['overflow_pages'] + 2)
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def iwx_stat_format(self, name, stat):
        return f'{name:10} records={stat["entries"]:10} size={self.iwx_space(stat):>10}'

    def iwx_analysis(self, txn: Transaction):
        txn = txn if isinstance(txn, Transaction) else txn.txn
        return {
            'lexicon':  self.iwx_space(txn.stat(self._lexicon)),
            'docindx':  self.iwx_space(txn.stat(self._docindx)),
            'docrindx': self.iwx_space(txn.stat(self._docrindx)),
            'bitmap':   self.iwx_space(txn.stat(self._bitmap)),
            'words':    self.iwx_space(txn.stat(self._words))
        }

    def dump_words (self):
        count = 0
        with self.env.begin(db=self._words) as txn:
            cursor = txn.cursor()
            while cursor.next():
                print(cursor.key(), cursor.value())
                count += 1
                if count == 5:
                    break

    def dump(self, debug=False):
        lexicon = []
        if debug:
            print('Lexicon')
            print(f'+----------------------+----------+----------+')
            print(f'| Word                 |    Index |     Freq |')
            print(f'+----------------------+----------+----------+')
        with self.env.begin(db=self._lexicon) as txn:
            cursor = txn.cursor()
            while cursor.next():
                key = cursor.key().decode()
                index, count = unpack('>LL', cursor.value())
                lexicon.append([key, count])
                if debug:
                    print(f'| {key.strip():20} | {index:8} | {count:8} |')
        if debug:
            print(f'+----------------------+----------+----------+')

        # print('Index')
        # print(f'+------------------------------+----------+')
        # print(f'| Doc Id                       |    Index |')
        # print(f'+------------------------------+----------+')
        # with self.env.begin(db=self._docindx) as txn:
        #     cursor = txn.cursor()
        #     while cursor.next():
        #         key = cursor.key().decode()
        #         index = unpack('>L', cursor.value())[0]
        #         print(f'| {key.strip():20} | {index:8} |')
        # print(f'+------------------------------+----------+')

        # print('RIndex')
        # print(f'+----------+------------------------------+')
        # print(f'| Index    | Doc Id                       |')
        # print(f'+----------+------------------------------+')
        # with self.env.begin(db=self._docrindx) as txn:
        #     cursor = txn.cursor()
        #     while cursor.next():
        #         key = unpack('>L', cursor.key())[0]
        #         index = cursor.value().decode()
        #         print(f'| {key:8} | {index:20} |')
        # print(f'+----------+-----------------------------+')
        return {'lexicon': lexicon}

    def iwx_lexicon(self, terms, max, txn=None):
        """Recover a list of matches from the Lexicon based on 'term'"""
        words = []
        if not len(terms):
            return []
        term = terms[-1].encode()
        if not len(term):
            return []
        with txn.cursor(self._lexicon) as cursor:
            if not cursor.set_range(term):
                return words
            for key, val in cursor:
                if not key.startswith(term):
                    break
                words.append([key, *unpack('>LL', val)])
                if len(words) > max:
                    break

        prefix = []
        for term in terms[:-1]:
            word = txn.get(term.encode(), db=self._lexicon)
            if not word:
                continue
            prefix.append((term, *unpack('>LL', word)))

        results = []
        for word in words:
            found = self._map.find(prefix + [word], transaction=txn)
            if found:
                results.append((word[0].decode(), len(found)))
            if len(results) >= max:
                break

        results.sort(key=lambda item: item[1], reverse=True)
        return results

    def ftx_query(self, terms, start=0, limit=None, countonly=False, txn=None):
        words = []
        default = (0, [])
        for word in terms:
            item = txn.get(word.encode(), db=self._lexicon)
            if not item:
                log.debug(f'no such term: {word}')
                return default
            words.append((word, *unpack('>LL', item)))

        words.sort(key=lambda item: item[2])
        found = self._map.find(words, transaction=txn)
        self._iwx_cache = found
        notfound = 0
        if countonly:
            return len(found), []
        else:
            newfound = []
            for term in found:
                result = self.resolve_idoc(term, txn)
                if result:
                    newfound.append(result)
                else:
                    notfound += 1
            if notfound:
                log.error(f'SEARCH ERROR: {notfound} unresolved documents')
            return len(newfound), list(filter(lambda term: term, newfound))


class Lexicon:

    MAX_WORD_SIZE = 128

    def __init__(self, context):
        self._table_lexicon = context._lexicon
        self._table_words = context._words
        self._table_index = context._docindx
        self._table_rindex = context._docrindx
        self._map = context._map
        self._words = None
        self._oid = None

    def from_oid(self, oid, transaction: Transaction):
        data = transaction.get(oid, db=self._table_words)
        self._words = Counter(loads(data.decode()) if data else [])
        self._oid = oid
        return self

    def from_words(self, oid, words, transaction: Transaction):
        transaction.put(oid, dumps(words).encode(), db=self._table_words)
        self._words = words
        self._oid = oid
        return self

    def lookup_word(self, word: str, transaction: Transaction):
        if len(word) > self.MAX_WORD_SIZE:
            return None
        item = transaction.get(word, db=self._table_lexicon)
        if item:
            return unpack('>LL', item)[0]
        word_index = transaction.stat(db=self._table_lexicon)['entries'] + 1
        try:
            transaction.put(word, pack('>LL', word_index, 0), db=self._table_lexicon)
            return word_index
        except Exception as e:
            log.error(e)
            return None
        
    def lookup_document(self, oid, transaction: Transaction):
        item = transaction.get(oid, db=self._table_index)
        if item:
            return unpack('>L', item)[0]
        document_index = transaction.stat(db=self._table_index)['entries'] + 1
        try:
            transaction.put(oid, pack('>L', document_index), db=self._table_index)
            transaction.put(pack('>L', document_index), oid, db=self._table_rindex)
            return document_index
        except Exception as e:
            log.error(e)
            return None

    def update_words(self, transaction):
        document_index = self.lookup_document(self._oid, transaction)
        for word in self._words:
            if word:
                word_index = self.lookup_word(word.encode(), transaction)
                if not word_index:
                    continue
                word_index, count = unpack('>LL', transaction.get(word.encode(), db=self._table_lexicon))
                transaction.put(word.encode(), pack('>LL', word_index, count + self._words[word]), db=self._table_lexicon)
                self._map.update(word_index, document_index, True, transaction=transaction)
            
    def delete(self, transaction):
        transaction.delete(self._oid, db=self._table_words)
        document_index = self.lookup_document(self._oid, transaction=transaction)
        for word in self._words:
            word_index, count = unpack('>LL', transaction.get(word.encode(), db=self._table_lexicon))
            transaction.put(word.encode(), pack('>LL', word_index, count - self._words[word]), db=self._table_lexicon)
            self._map.update(word_index, document_index, False, transaction=transaction)
