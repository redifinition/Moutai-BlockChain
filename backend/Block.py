'''
@Description: 
@Author: lyq
@Date: 2024-04-01 16:45:31
@LastEditTime: 2024-04-01 19:59:02
@LastEditors: lyq
'''
import time
import hashlib
import json

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index  # 区块的索引
        timestamp = time.time()
        local_time = time.localtime(timestamp)
        format_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        self.timestamp = format_time  # 区块创建的时间戳
        self.transactions = transactions  # 区块包含的交易列表
        self.previous_hash = previous_hash  # 前一个区块的哈希值
        self.hash = self.calculate_hash()  # 当前区块的哈希值

    def calculate_hash(self):
        """
        计算并返回区块的哈希值，基于区块的主要属性。
        """
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        """
        将区块信息转换为字典格式，便于之后的处理和存储。
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }
