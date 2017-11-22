import tushare as ts
import pandas as pd
import global_value

local_position = global_value.local_position


def update_stock_code():
    stock_basics = ts.get_stock_basics()
    stock_basics.to_csv(local_position + 'stock_basics.csv', encoding='GBK')


update_stock_code()


