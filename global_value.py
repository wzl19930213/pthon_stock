import tushare as ts

ts.set_token('9fc3acfd6cff62a93f42ad8abfdc34448192fed0e49857cabf45b095')

pro = ts.pro_api()

local_position = 'F:/python/pthon_stock/data/'
old_data_position = 'F:/python/trading-data.20171107/stock_data'

HEADER_DATE = 'date'
HEADER_CLOSE = 'close'
HEADER_HIGH = 'high'
HEADER_LOW = 'low'
HEADER_VOLUME = 'volume'
