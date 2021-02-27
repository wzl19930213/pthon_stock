
"""
选股策略：MACD 价格背离
"""

import math
import os
import time

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import talib
from matplotlib.pylab import date2num
# pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
from mpl_finance import candlestick_ohlc
from pandas.plotting import register_matplotlib_converters

import global_value
import update_stock_code

register_matplotlib_converters()
'''
上面两句话我也不知道为啥要加，不加会报Warning---
FutureWarning: Using an implicitly registered datetime converter for a matplotlib plotting method. 
The converter was registered by pandas on import. 
Future versions of pandas will require you to explicitly register matplotlib converters.
'''

local_position = global_value.local_position
start_time = "2020-06-01"
current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
daily_data_position = global_value.local_position + 'fig/macd_deviation/' + current_time + '/'


def del_file(path_data):
    for i in os.listdir(path_data):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i  # 当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:  # os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)


# 删除以前的文件
if os.path.exists(daily_data_position):
    del_file(daily_data_position)
else:
    os.mkdir(daily_data_position)

# 使用ggplot样式，好看些
mpl.style.use("ggplot")

codes = update_stock_code.get_stock_codes()
length = len(codes)

print(start_time + '  ' + current_time + '  start: ' + str(length))
count = 0
res_codes = []
message = "-------------------------------result-------------------------------\n"
for code in codes:
    try:
        count = count + 1
        code = str(code).zfill(6)
        print('%.2f%%' % (count / length * 100) + ", code: " + str(code))

        # data = ts.get_k_data(code, start=start_time)
        data = global_value.pro.daily(ts_code=code, start_date=start_time)
        # 将date值转换为datetime类型，并且设置成index
        data.trade_date = pd.to_datetime(data.trade_date)
        data.index = data.trade_date

        # 计算指数移动平均线 EMA
        data["ema22"] = talib.MA(data.close, timeperiod=22)
        data["ema11"] = talib.MA(data.close, timeperiod=11)

        # 计算MACD指标数据
        data["macd"], data["signal"], data["hist"] = talib.MACD(data.close)

        data_len = len(data["low"])
        peak_data = []
        for index in range(data_len):
            if index <= 3 or index >= data_len - 2 or math.isnan(data['hist'][index]):
                continue
            elif (data["high"][index] >= data["high"][index - 1] and data["high"][index] >= data["high"][index - 2]
                  and data["high"][index] >= data["high"][index + 1] and data["high"][index] >= data["high"][index + 2]) \
                    or (data["low"][index] <= data["low"][index - 1] and data["low"][index] <= data["low"][index - 2]
                        and data["low"][index] <= data["low"][index + 1] and data["low"][index] <= data["low"][
                            index + 2]):
                peak_data.append(index)

        curDate = data["trade_date"][data_len - 1]
        curLowPrice = data["low"][data_len - 1]
        curMACD = data["hist"][data_len - 1]

        lastHighPeak = -1
        lastLowPeak = -1

        for index in range(len(peak_data)):
            if lastHighPeak >= 0 and lastLowPeak >= 0:
                break
            curIndex = peak_data[len(peak_data) - 1 - index]
            if lastHighPeak < 0 and data["high"][curIndex] >= data["high"][curIndex - 1]:
                lastHighPeak = len(peak_data) - 1 - index
            elif lastLowPeak < 0 and data["low"][curIndex] <= data["low"][curIndex - 1]:
                lastLowPeak = len(peak_data) - 1 - index

        if 0 <= lastLowPeak < len(peak_data) - 1:
            lastLowPrice = data["low"][peak_data[lastLowPeak]]
            lastLowMACD = data["hist"][peak_data[lastLowPeak]]

            if curLowPrice < lastLowPrice and lastLowMACD < curMACD and data["hist"][peak_data[lastLowPeak + 1]] > 0:
                pickMessage = "code: " + str(code) + ", lastData: " + str(data["trade_date"][peak_data[lastLowPeak]]) \
                              + ", curDate: " + str(curDate) + "\n"
                pickMessage += "lastLowPrice: " + str(lastLowPrice) + ", curLowPrice: " + str(curLowPrice) + "\n"
                pickMessage += "lastLowMACD: " + str(lastLowMACD) + ", curMACD: " + str(curMACD) \
                               + ", preHigh Macd: " + str(data["hist"][peak_data[lastLowPeak + 1]]) + "\n"
                print(pickMessage)
                message += pickMessage
            else:
                continue
        else:
            continue
        print("############################################################################")

        res_codes.append(code)

        # ATR
        data["atr"] = talib.ATR(data.high, data.low, data.close, timeperiod=14)
        data["atr1Plus"] = data["ema11"] + data["atr"]
        data["atr2Plus"] = data["ema11"] + 2 * data["atr"]
        data["atr3Plus"] = data["ema11"] + 3 * data["atr"]
        data["atr1Minus"] = data["ema11"] - data["atr"]
        data["atr2Minus"] = data["ema11"] - 2 * data["atr"]
        data["atr3Minus"] = data["ema11"] - 3 * data["atr"]

        # 绘制第一个图
        fig = plt.figure()
        fig.set_size_inches((16, 10))

        ax_canddle = fig.add_axes((0.04, 0.5, 0.96, 0.5))
        ax_macd = fig.add_axes((0.04, 0.05, 0.96, 0.40))

        data_list = []
        for date, row in data[["open", "high", "low", "close"]].iterrows():
            t = date2num(date)
            open, high, low, close = row[:]
            datas = (t, open, high, low, close)
            data_list.append(datas)

        # 绘制蜡烛图
        candlestick_ohlc(ax_canddle, data_list, colorup='r', colordown='green', alpha=0.7, width=0.8)

        # 将x轴设置为时间类型
        ax_canddle.xaxis_date()
        ax_canddle.plot(data.index, data.ema22, label="EMA11")
        ax_canddle.plot(data.index, data.ema11, label="EMA22")
        ax_canddle.plot(data.index, data.atr1Plus, label="ATR1Plus", linestyle=":")
        ax_canddle.plot(data.index, data.atr2Plus, label="ATR2Plus", linestyle=":")
        ax_canddle.plot(data.index, data.atr3Plus, label="ATR3Plus", linestyle=":")
        ax_canddle.plot(data.index, data.atr1Minus, label="ATR1Minus", linestyle=":")
        ax_canddle.plot(data.index, data.atr2Minus, label="ATR2Minus", linestyle=":")
        ax_canddle.plot(data.index, data.atr3Minus, label="ATR3Minus", linestyle=":")
        ax_canddle.legend()

        # 绘制MACD
        ax_macd.plot(data.index, data["macd"], label="macd")
        ax_macd.plot(data.index, data["signal"], label="signal")
        ax_macd.bar(data.index, data["hist"] * 2, label="hist",
                    color=['red' if hist > 0 else 'green' for hist in data["hist"]])
        ax_macd.legend()

        fig.savefig(daily_data_position + code + ".png")

    except Exception as e:
        print('error: ' + code + ", " + str(e))

print('100%')
print(message)
print(res_codes)
