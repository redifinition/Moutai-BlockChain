'''
@Description: 
@Author: lyq
@Date: 2024-04-09 22:25:48
@LastEditTime: 2024-04-10 00:18:37
@LastEditors: lyq
'''
import random
import requests

from default_data import TRANSACTIONS


def generate_new_transaction(node, data):
    url = f"http://127.0.0.1:{node}/transactions/new"
    response = requests.post(url, json=data)
    print(response)
    
def generate_new_block(node):
    url = f"http://127.0.0.1:{node}/mine"
    response = requests.get(url)

if __name__ == '__main__':
    # 默认创建一些区块和交易
    # 提前调用api
    ports = ['5001','5002']
    for port in ports:
        for transaction_data in TRANSACTIONS:
            generate_new_transaction(port, transaction_data)
            generate_new_block
            random_number = random.randint(0, 1)
            if random_number:
                generate_new_block(port)