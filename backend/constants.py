from Transaction import LogisticsTransaction, ProductionTransaction, SaleTransaction


TRANSACTION_DICT = {
    'production' : ['timestamp', 'product_id', 'batch_number', 'production_date', 'factory', 'origin_place'],
    'logistics': ['timestamp', 'product_id', 'from_address', 'to_address', 'carrier', 'tracking_number', 'start_time', 'end_time', 'status'],
    'sale': ['timestamp', 'product_id', 'seller', 'buyer', 'price']
}

TRANSACTION_CLASS_DICT = {
    'production' : ProductionTransaction,
    'logistics': LogisticsTransaction,
    'sale': SaleTransaction
}

AUTHORITY_NODES = ['127.0.0.1']