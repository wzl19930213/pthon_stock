import tushare as ts
import os
import csv
import pandas as pd
import time
import global_value
import update_stock_code

# 趋势选股法
# 根据趋势。。。

local_position = global_value.local_position
daily_data_position = global_value.local_position + 'daily_data/'
current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))


if os.path.exists(local_position + 'stock_basics.csv'):
    stock_basics = pd.read_csv(local_position + 'stock_basics.csv', encoding='GBK')
    codes = stock_basics.iloc[:, 0]
else:
    update_stock_code.update_stock_code()
    stock_basics = pd.read_csv(local_position + 'stock_basics.csv', encoding='GBK')
    codes = stock_basics.iloc[:, 0]
length = len(codes)

print(current_time + '  code length: ' + str(length))
count = 0
codes = ['002500']
for code in codes:
    try:
        print('%.2f%%' % (count/length*100))
        count = count + 1

        code = str(code).zfill(6)
        filename = daily_data_position + code + '.csv'
        if os.path.exists(filename):
            csv_data = csv.reader(open(filename, encoding='utf-8'))
            df_old = pd.read_csv(filename)
            i = 0
            for row in csv_data:
                i = i + 1
                print(row)
    except:
        print('error')
print('100%')

