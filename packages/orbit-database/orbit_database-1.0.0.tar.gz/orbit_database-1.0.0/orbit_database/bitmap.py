from struct import pack, unpack
from lmdb import Transaction as TXN
import re
from functools import reduce

try:
    from loguru import logger as log
except Exception:
    import logging as log


class Bitmap:

    CHUNK_SIZE = 1000
    PAGE_SIZE = CHUNK_SIZE * 8

    def __init__(self, table):
        self._bitmap = table

    def update(self, word_index, document_index, value, transaction: TXN):
        """
        """
        section, offset = divmod(document_index, self.PAGE_SIZE)
        page_key = pack('>LL', word_index, section)
        bitmap = transaction.get(page_key, db=self._bitmap)
        bitmap = bytearray(self.CHUNK_SIZE if not bitmap else bitmap)
        byte, bits = divmod(offset, 8)
        if value:
            bitmap[byte] |= 1 << bits
        else:
            bitmap[byte] &= ~(1 << bits)
        transaction.put(page_key, bitmap, db=self._bitmap)

    def fetch(self, word_index, document_index, value, transaction: TXN):
        section, offset = divmod(document_index, self.PAGE_SIZE)
        page_key = pack('>LL', word_index, section)
        return transaction.get(page_key, db=self._bitmap)

    def find(self, words, transaction: TXN):
        with transaction.cursor(self._bitmap) as cursor:
            word_index = words[0][1]
            if not cursor.set_range(pack('>LL', word_index, 0)):
                return None
            results = []
            for key, val in cursor:
                index, section = unpack('>LL', key)
                if word_index != index:
                    break
                masks = [int.from_bytes(val, 'little')]
                for word in words[1:]:
                    mask = transaction.get(pack('>LL', word[1], section), db=self._bitmap)
                    if not mask:
                        break
                    masks.append(int.from_bytes(mask, 'little'))
                else:
                    #   Here comes the magic ...
                    #   reduce bitwise and's all the bitmaps together
                    #   bin converts the integer binmap to a string of 0's and 1's
                    #   [::-1] reverse sorts the string (endian convert)
                    #   finditer then find's all the 1's
                    #
                    results += [
                        section * self.PAGE_SIZE + i.start() 
                        for i in re.finditer('1', bin(reduce(lambda a,b: a & b, masks))[::-1])
                    ]
            return results

