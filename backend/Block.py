'''
@Description: 
@Author: lyq
@Date: 2024-04-01 16:45:31
@LastEditTime: 2024-04-10 00:50:13
@LastEditors: lyq
'''
import time
import hashlib
import json

class Block:
    def __init__(self, index, transactions, previous_hash, hash = None,timestamp=None):
        self.index = index
        if timestamp is None:
            timestamp = time.time()
            local_time = time.localtime(timestamp)
            format_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            self.timestamp = format_time
        else:
            self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        if hash is None:
            self.hash = self.calculate_hash()
        else:
            self.hash = hash

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

    @staticmethod
    def dict_to_block(data):
        return Block(
            index=data['index'],
            transactions=data['transactions'],
            previous_hash=data['previous_hash'],
            timestamp=data['timestamp'],
            hash=data['hash']
        )
