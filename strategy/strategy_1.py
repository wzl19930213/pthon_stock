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
current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

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
strategy_high_code = []
strategy_low_code = []
for code in codes:
    print('%.2f%%' % (count / length * 100))
    count = count + 1

    try:
        code = str(code).zfill(6)
        filename = daily_data_position + code + '.csv'
        if os.path.exists(filename):
            csv_data = csv.reader(open(filename, encoding='utf-8'))
            df_old = pd.read_csv(filename)
            i = 0
            for row in csv_data:
                i = i + 1
                data_header = row
                if i == 1:
                    break
            close_index = 0
            date_index = 0
            high_index = 0
            low_index = 0
            temp_close_index = 0
            for name in data_header:
                if name == global_value.HEADER_CLOSE:
                    close_index = temp_close_index
                if name == global_value.HEADER_DATE:
                    date_index = temp_close_index
                if name == global_value.HEADER_HIGH:
                    high_index = temp_close_index
                if name == global_value.HEADER_LOW:
                    low_index = temp_close_index
                temp_close_index = temp_close_index + 1
            closePrice = []
            highPrice = []
            lowPrice = []
            dateTime = []
            for row in csv_data:
                closePrice.append(row[close_index])
                highPrice.append(row[high_index])
                lowPrice.append(row[low_index])
                dateTime.append(row[date_index])
            highestPoint = []
            highestDatePoint = []
            lowestPoint = []
            lowestDatePoint = []
            for i in range(0, len(dateTime)):
                if i == 0 or i == len(highPrice) - 1:
                    continue
                if i > 60:
                    break
                if highPrice[i] > highPrice[i + 1] and highPrice[i] > highPrice[i - 1]:
                    highestPoint.append(highPrice[i])
                    highestDatePoint.append(dateTime[i])
                if lowPrice[i] < lowPrice[i + 1] and lowPrice[i] < lowPrice[i - 1]:
                    lowestPoint.append(lowPrice[i])
                    lowestDatePoint.append(dateTime[i])
            if closePrice[1] < max(highestPoint) < closePrice[0]:
                strategy_high_code.append(code)
            if closePrice[1] > max(lowestPoint) > closePrice[0]:
                strategy_low_code.append(code)
    except:
        print('error')
print('100%')
print(strategy_high_code)
print(strategy_low_code)
