
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests
from Block import Block
from constants import AUTHORITY_NODES


class Blockchain(object):
    # 区块链初始化
    def __init__(self):
        self.chain = []  # 此列表表示区块链对象本身。
        self.currentTransaction = []  # 此列表用于记录目前在区块链网络中已经经矿工确认合法的交易信息，等待写入新区块中的交易信息。
        self.nodes = set()  # 建立一个无序元素集合。此集合用于存储区块链网络中已发现的所有节点信息
        # 在 __init__ 方法中初始化权威节点集合
        self.authorities = set(AUTHORITY_NODES)
        # Create the genesis block(创建创世区块)
        self.new_block(validator=AUTHORITY_NODES[0], previous_hash=1) # 保证创世节点都相同


    # 注册节点
    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        # 检查节点的格式，通过urlparse方法将这个节点的url分割成六个部分
        parsed_url = urlparse(address)
        # 如果网络地址不为空，那么就添加没有http://之类修饰的纯的地址，如：www.baidu.com
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        # 如果网络地址为空，那么就添加相对Url的路径
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')  # 说明这是一个非标准的Url

    # 验证区块链有效性（检查bockchain是否有效，即检查是否每个区块都合法）
    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """
        # 这里取得的是创世区块，意味着必须从头检查整个区块链上从创世区块到链上最后一个区块为止的所有区块的链接关系
        last_block = chain[0]
        # 下面的while循环就是为了检查链上每一个区块与其连接的前一个区块是否合法相关，通过 检查 previous_hash 来判断
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            last_block_hash = last_block['hash']
            # 检查块的哈希是否正确
            if block['previous_hash'] != last_block_hash:
                return False  # 如果发现当前在检查的区块的previous_hash值与它实际连接的前一区块的hash值不同，则证明此链条有问题，终止检查
            last_block = block  # 让当前区块变成前一个区块，以迭代到一下次循环
            current_index += 1  # 让下一个区块区区块号+1

        return True

    # 解决冲突
    def resolve_conflicts(self):
        """
        解决区块链节点之间的冲突，用网络中最长的链替换我们的链。
        :return: True if our chain was replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None

        # 本节点的存储的区块链条的长度（即有多少 个区块）
        max_length = len(self.chain)

        # 获取所有已知区块链网络中的节点中存储的区块链条，并分析其是否比本节点的链条长度要长
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')  # 到每个节点的chain页面去获取此节点的区块链条信息，返回结果包含了一个chain对象本身和它的长度信息
            # HTTP状态码等于200表示请求成功
            if response.status_code == 200:
                length = response.json()['length']  # 通过json类把返回的对象取出来
                chain = response.json()['chain']

                # 如果此节点的区块链长度比本节点区块链长度长，且链条合法，则证明是值得覆盖本节点链条的合法链条
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = [Block.dict_to_block(block) for block in chain]

        # 用找到的比本节点区块链链条长的链条覆盖本节点的旧链条
        if new_chain:
            self.chain = new_chain
            return True

        return False   # 如果没有发现别的节点上的链条比本节点的链条更长，那么 就返回 FALSE
    
    def new_block(self, validator, previous_hash=None):
        # 确认验证者是否是权威节点
        if validator not in self.authorities:
            return None # 或者抛出异常
        block = Block(len(self.chain) + 1, self.currentTransaction, previous_hash or self.chain[-1].calculate_hash())
        self.currentTransaction = []
        self.chain.append(block)
        return block

    # 创建新交易
    def new_transaction(self, transaction):
        """
        添加一个新的交易到交易列表中。
        :param transaction: 一个交易实例，该实例应该是Transaction类或其子类的实例。
        :return: 将包含此交易的区块的索引。
        """
        # 将交易对象转换为字典格式并添加到当前交易列表
        self.currentTransaction.append(transaction.to_dict())

        # 下一个待挖的区块中
        return self.last_block.to_dict()['index'] + 1


    

    @property
    def last_block(self):
        return self.chain[-1]  # 区块链的最后一个区块



