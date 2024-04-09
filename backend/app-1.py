# 实例化我们的节点；加载 Flask 框架
from argparse import ArgumentParser
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

from BlockChain import Blockchain
from constants import TRANSACTION_CLASS_DICT, TRANSACTION_DICT


app = Flask(__name__)
CORS(app)  # 允许所有域的跨域请求
# 为我们的节点创建一个随机名称
node_identifier = str(uuid4()).replace('-', '')

# 实例化 Blockchain 类
blockchain = Blockchain()


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # 将请求参数解析为JSON格式
    values = request.get_json()

    # 检查交易类型字段是否存在
    if 'type' not in values:
        return 'Missing transaction type', 400
    if values['type'] not in TRANSACTION_DICT.keys():
        return 'Invalid transaction type', 400
    required = TRANSACTION_DICT[values['type']]
    if not all(k in values for k in required):
            return 'Missing values', 400
    transaction = TRANSACTION_CLASS_DICT[values['type']](**{k: values[k] for k in required})
    # 创建新交易并获取应添加到的区块的索引
    index = blockchain.new_transaction(transaction)
    response = {'message': f'Transaction will be added to Block {index}',         'code': 20000,}
    return jsonify(response), 201



@app.route('/mine', methods=['GET'])
def mine():
    node_identifier = request.remote_addr
    last_block = blockchain.last_block
    previous_hash = last_block.to_dict()['hash']
    block = blockchain.new_block(validator=node_identifier, previous_hash=previous_hash)

    if block is None:
        response = {'message': 'New Block Forbidden'}
        return jsonify(response), 403

    # # 由于找到了证据，我们会收到一份奖励
    # # sender为“0”，表示此节点已挖掘了一个新货币
    # blockchain.new_transaction(
    #     sender="0",
    #     recipient=node_identifier,
    #     amount=1,
    # )

    response = {
        'message': "New Block Forged",
        'code': 20000,
        'index': block.to_dict()['index'],
        'transactions': block.to_dict()['transactions'],
        'previous_hash': block.to_dict()['previous_hash'],
    }
    return jsonify(response), 200

# 创建 /chain 端点，它是用来返回整个 Blockchain类
@app.route('/chain', methods=['GET'])
# 将返回本节点存储的区块链条的完整信息和长度信息。
def full_chain():
    blockchain_chain = [block.to_dict() for block in blockchain.chain]
    response = {
        'code': 20000,
        'chain': blockchain_chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# 注册节点
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'code': 20000,
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


# 添加节点解决冲突的路由
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    # 解决多个区块链网络节点间的节点冲突，更新为区块链网络中最长的那条链条-
    replaced = blockchain.resolve_conflicts()
    # 如果使用的本节点的链条，那么返回如下
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'code': 20000,
            'new_chain': [block.to_dict() for block in blockchain.chain]
        }
    # 如果更新别的节点的链条，那么返回如下：
    else:
        response = {
            'message': 'Our chain is authoritative',
            'code': 20000,
            'chain': [block.to_dict() for block in blockchain.chain]
        }

    return jsonify(response), 200  # jsonify()序列化把返回信息变成字符

# 溯源查询
@app.route('/product/history', methods=['GET'])
def get_product_history():
    product_id = request.args.get('product_id')
    if not product_id:
        return jsonify({'message': 'Missing product_id'}), 400
    
    product_history = []
    # 假设blockchain变量是您区块链的实例
    for block in blockchain.chain:
        for transaction in block.transactions:
            if transaction['product_id'] == product_id:
                product_history.append(transaction)
    response = {
            'code': 20000,
            'transactions': product_history
        }
    return jsonify(response), 200

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    parser = ArgumentParser()  # 创建一个参数接收的解释器，由此对象（这里是：parser)来负责解释参数信息
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()  # 通过parse_args()方法尝试对收到的参数关键字进行解释
    port = args.port  # 从args对象中取出其中的参数关键字--port 参数的内容，也可能是获取到预设的默认值

    # 提前调用api
    api_url = "http://127.0.0.1:5001/transactions/new"
    response = requests.get(api_url)
    app.run(host='0.0.0.0', port=5001)
