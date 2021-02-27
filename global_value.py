import os

import tushare as ts

ts.set_token('9fc3acfd6cff62a93f42ad8abfdc34448192fed0e49857cabf45b095')

pro = ts.pro_api()

module_path = os.getcwd().replace("\\", "/")
father_path = os.path.abspath(os.path.dirname(module_path)+os.path.sep+".").replace("\\", "/")

local_position = module_path + '/data/'
old_data_position = father_path + '/trading-data.20171107/stock_data'

print("local_position: " + local_position)
print("old_data_position: " + old_data_position)

HEADER_DATE = 'date'
HEADER_CLOSE = 'close'
HEADER_HIGH = 'high'
HEADER_LOW = 'low'
HEADER_VOLUME = 'volume'
