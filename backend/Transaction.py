'''
@Description: 
@Author: lyq
@Date: 2024-04-01 19:01:17
@LastEditTime: 2024-04-02 12:31:14
@LastEditors: lyq
'''
# 基础交易类
import hashlib


class Transaction:
    def __init__(self, timestamp: str, product_id: int):
        self.timestamp = timestamp
        self.product_id = product_id
        self.transaction_id = self.generate_transaction_id()

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "product_id": self.product_id
        }
    
    def generate_transaction_id(self):
        # 将交易信息转换为字符串，这里仅使用timestamp和product_id作为示例
        transaction_string = f'{self.timestamp}{self.product_id}'.encode()
        # 使用SHA-256哈希函数生成交易ID
        return hashlib.sha256(transaction_string).hexdigest()
    
# 生产交易类：记录生产信息
class ProductionTransaction(Transaction):
    def __init__(self, timestamp: str, product_id: int,
                    batch_number: int, production_date: str, factory: str, origin_place: str):
        super().__init__(timestamp, product_id)
        self.batch_number = batch_number # 批次号
        self.production_date = production_date # 生产日期
        self.factory = factory # 工厂
        self.origin_place = origin_place # 原材料或生产地的位置

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "type": "production",
            "details": {
                "batch_number": self.batch_number,
                "production_date": self.production_date,
                "factory": self.factory,
                "origin_place": self.origin_place
            }
        })
        return base_dict
    
class LogisticsTransaction(Transaction):
    def __init__(self, timestamp: str, product_id: int,
                 from_address: str, to_address: str, carrier: str, tracking_number: int,
                 start_time: str, end_time: str=None, status: str="in_progress"):
        super().__init__(timestamp, product_id)
        self.from_address = from_address
        self.to_address = to_address
        self.carrier = carrier
        self.tracking_number = tracking_number
        self.start_time = start_time
        self.end_time = end_time  # 可能为空，如果运输尚未完成
        self.status = status  # 表示运输状态，如"in_progress", "completed"等

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "type": "logistics",
            "details": {
                "from_address": self.from_address,
                "to_address": self.to_address,
                "carrier": self.carrier,
                "tracking_number": self.tracking_number,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "status": self.status
            }
        })
        return base_dict

    def update_status(self, new_status: str, end_time: str=None):
        self.status = new_status
        if end_time:
            self.end_time = end_time

class SaleTransaction(Transaction):
    def __init__(self, timestamp: str, product_id: int,
                 seller: str, buyer: str, price: float):
        super().__init__(timestamp, product_id)
        self.seller = seller
        self.buyer = buyer
        self.price = price

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "type": "sale",
            "details": {
                "seller": self.seller,
                "buyer": self.buyer,
                "price": self.price
            }
        })
        return base_dict