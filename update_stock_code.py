import global_value
import os
import pandas as pd

local_position = global_value.local_position


def update_stock_code():
    stock_basics = global_value.pro.stock_basic(exchange='', list_status='L',
                                                fields='ts_code,symbol,name,area,industry,list_date')
    stock_basics.to_csv(local_position + 'stock_basics.csv', encoding='GBK')


def get_stock_codes():
    if os.path.exists(local_position + 'stock_basics.csv'):
        stock_basics = pd.read_csv(local_position + 'stock_basics.csv', encoding='GBK')
    else:
        update_stock_code()
        stock_basics = pd.read_csv(local_position + 'stock_basics.csv', encoding='GBK')
    codes = stock_basics.iloc[:, 1]
    return codes
