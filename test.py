import tushare as ts
import pandas as pd
import global_value
import os
import time
import datetime
import matplotlib.pyplot as plt

daily_data_position = global_value.local_position + 'daily_data/'
filename = daily_data_position + '000001.csv'


def get_price_voulme_new_api(code, days):
    df_000001 = pd.read_csv(filename)
    date_times = []
    for i in range(0, days):
        date_times.append(df_000001.iat[i,0])
    # 获取连接备用
    cons = ts.get_apis()
    price_volume = {}
    for i in range(0 ,days):
        # 股票tick,type:买卖方向，0-买入 1-卖出 2-集合竞价成交
        df_current = ts.tick(code, conn=cons, date=date_times[i])
        print(str(i) + ': ' + date_times[i] + '-------' + str(len(df_current)))
        for j in range(0,len(df_current)):
            curret_pirce = float("%.2f" % df_current.iat[j,1])
            current_volume = df_current.iat[j,2]
            if curret_pirce in price_volume.keys():
                price_volume[curret_pirce] += current_volume
            else :
                price_volume[curret_pirce] = current_volume
    # 对字典进行排序，按照关键字升序。reverse默认为False，表示升序  
    # 排序的对象，后面的是个匿名函数。 
    price_volume = sorted(price_volume.items(),key=lambda abs:abs[0],reverse=False)
    return price_volume


print(get_price_voulme_new_api('600000', 60))
