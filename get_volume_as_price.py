import tushare as ts
import os
import csv
import pandas as pd
import time
import datetime
import global_value
import update_stock_code
import matplotlib.pyplot as plt

local_position = global_value.local_position
price_volume_postion = local_position + 'price_volume/'
daily_data_position = global_value.local_position + 'daily_data/'
fig_position = local_position + 'fig/'
current_time = datetime.datetime.now() 

filename = daily_data_position + '000001.csv'
df_000001 = pd.read_csv(filename)
date_times = []
for i in range(0, len(df_000001)):
    date_times.append(df_000001.iat[i,0])

if os.path.exists(local_position + 'stock_basics.csv'):
    stock_basics = pd.read_csv(local_position + 'stock_basics.csv', encoding='GBK')
    codes = stock_basics.iloc[:,0]
else:
    update_stock_code.update_stock_code()
length = len(codes)


def dateframe_is_equal(df1, df2):
    if len(df1) != len(df2):
        return False
    for x in range(0, len(df1)):
        if df1.iat[x,1] != df2.iat[x,1]:
            return False
    return True


def get_price_voulme_old_api(code, days):
    price_volume = {}
    i = 0
    while i < days:
        old_time = current_time + datetime.timedelta(days=-i)
        old_time = old_time.strftime('%Y-%m-%d')
        df_current = ts.get_tick_data(code, date=old_time)
        if len(df_current) < 6:
            continue
        else:
            i += 1
        print(str(i) + ': ' + old_time + '-------' + str(len(df_current)))
        for j in range(0, len(df_current)):
            current_price = float("%.2f" % df_current.iat[j,1])
            current_volume = df_current.iat[j,3]
            if current_price in price_volume.keys():
                price_volume[current_price] += current_volume
            else:
                price_volume[current_price] = current_volume
    # 对字典进行排序，按照关键字升序。reverse默认为False，表示升序  
    # 排序的对象，后面的是个匿名函数。 
    price_volume = sorted(price_volume.items(), key=lambda abs:abs[0], reverse=False)
    return price_volume


def get_price_voulme_new_api(code, days):
    # 获取连接备用
    cons = ts.get_apis()
    price_volume = {}
    for i in range(0, days):
        # 股票tick,type:买卖方向，0-买入 1-卖出 2-集合竞价成交
        df_current = ts.tick(code, conn=cons, date=date_times[i])
        print(str(i) + ': ' + date_times[i] + '-------' + str(len(df_current)))
        for j in range(0, len(df_current)):
            curret_pirce = float("%.2f" % df_current.iat[j,1])
            current_volume = df_current.iat[j,2]
            if curret_pirce in price_volume.keys():
                price_volume[curret_pirce] += current_volume
            else:
                price_volume[curret_pirce] = current_volume
    # 对字典进行排序，按照关键字升序。reverse默认为False，表示升序  
    # 排序的对象，后面的是个匿名函数。 
    price_volume = sorted(price_volume.items(), key=lambda abs:abs[0], reverse=False)
    return price_volume


# 处理，price_volume，使得价格间隔变大如：9.1-9.3一段
def price_volume_deal(price_volume, gap):
    new_price_volume = {}
    current_price = price_volume[0][0]
    new_price_volume[current_price] = price_volume[0][1]
    for i in range(0, len(price_volume)):
        if price_volume[i][0] < current_price:
            new_price_volume[current_price] += price_volume[i][1]
        else:
            current_price += gap
            current_price = float("%.2f" % current_price)
            new_price_volume[current_price] = price_volume[i][1]
    # 对字典进行排序，按照关键字升序。reverse默认为False，表示升序 
    new_price_volume = sorted(new_price_volume.items(), key=lambda abs:abs[0], reverse=False)
    return new_price_volume


def plot_price_volume(price_volume, code, bar_width):
    x = []
    y = []
    for i in range(0, len(price_volume)):
        x.append(price_volume[i][0])
        y.append(price_volume[i][1])
    plt.bar(x, y, width=bar_width, color="green")
    plt.savefig(fig_position + code + '.png')
    plt.close()


codes = ['002254', '002500']
names = ['泰和新材', '山西证券']
for code in codes:
    price_volume = get_price_voulme_new_api(code, 60)
    # price_volume = price_volume_deal(price_volume, 0.1)
    print(price_volume)
    plot_price_volume(price_volume, code, 0.01)


print('end')
