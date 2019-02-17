import tushare as ts
import os
import csv
import pandas as pd
import time
import global_value
import update_stock_code

local_position = global_value.local_position
daily_data_position = global_value.local_position + 'daily_data/'
current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
start_time = '2015-01-01'


if os.path.exists(local_position + 'stock_basics.csv'):
    stock_basics = pd.read_csv(local_position + 'stock_basics.csv', encoding='GBK')
    codes = stock_basics.iloc[:, 0]
else:
    update_stock_code.update_stock_code()
    stock_basics = pd.read_csv(local_position + 'stock_basics.csv', encoding='GBK')
    codes = stock_basics.iloc[:, 0]
length = len(codes)

print(start_time + '  ' + current_time + '  start: ' + str(length))
count = 0
for code in codes:
    try:
        print('%.2f%%' % (count/length*100))
        count = count + 1

        code = str(code).zfill(6)
        filename = daily_data_position + code + '.csv'
        if os.path.exists(filename):
            last_date = start_time
            csv_data = csv.reader(open(filename, encoding='utf-8'))
            df_old = pd.read_csv(filename)
            i = 0
            for row in csv_data:
                if i == 1:
                    last_date = row[1]
                    break
                i = i + 1
            if last_date.replace(".", '').isdigit():
                for row in csv_data:
                    if i == 1:
                        last_date = row[0]
                        break
                    i = i + 1
            df = ts.get_hist_data(code, start=last_date, end=current_time)
            print('code: ' + code + ' last_date: ' + last_date + ' current_time: ' + current_time)
            if df is None:
                print('df is None')
                pass
            else:
                df.to_csv(filename)
            df = pd.read_csv(filename)
            df = df.append(df_old[1:], ignore_index=True)
            if df is None:
                print('df is None')
                pass
            else:
                df.to_csv(filename, index=None)
            # df.to_csv(filename, mode='a', header=None, index=None)
        else:
            df = ts.get_hist_data(code, start=start_time, end=current_time)
            if df is None:
                print('df is None')
                pass
            else:
                df.to_csv(filename)
    except:
        print('error')
print('100%')

