import pandas as pd
import global_value
import os

# 【code】 股票的代码，上证股票以sh开头，深证股票以sz开头
# 【date】 交易日期
# 【open】 开盘价
# 【high】 最高价
# 【low】 最低价
# 【close】 收盘价
# 【change】 涨跌幅，复权之后的真实涨跌幅，保证准确
# 【volume】 成交量
# 【money】 成交额
# 【traded_market_value】 流通市值
# 【market_value】 总市值
# 【turnover】 换手率，成交量/流通股本
# 【adjust_price】 后复权价，复权开始时间为股票上市日，精确到小数点后10位
# 【report_type】 最近一期财务报告的类型，3-31对应一季报，6-30对应半年报，9-30对应三季报，12-31对应年报
# 【report_date】 最近一期财务报告实际发布的日期
# 【PE_TTM】 最近12个月市盈率，股价 / 最近12个月归属母公司的每股收益TTM
# 【PS_TTM】 最近12个月市销率， 股价 / 最近12个月每股营业收入
# 【PC_TTM】 最近12个月市现率， 股价 / 最近12个月每股经营现金流
# 【PB】 市净率，股价 / 最近期财报每股净资产
# 【adjust_price_f】 前复权价，复权开始时间为股票最近一个交易日，精确到小数点后10位


local_position = global_value.local_position
daily_data_position = global_value.local_position + 'daily_data/'
old_data_position = global_value.old_data_position
names = ['code' ,'date', 'open', 'high', 'low',    'close', 'change', 'volume', 'money', 'traded_market_value',
         'market_value', 'turnover', 'adjust_price', 'report_type', 'report_date', 'PE_TTM', 'PS_TTM', 'PC_TTM',
         'PB', 'adjust_price_f']


# 获取该目录下文件
def get_file_names(file_dir):
    return os.listdir(file_dir)


# 获取该列表得和
def get_list_sum(stock_list):
    length = len(stock_list)
    sum_list = 0
    for i in range(0,length):
        sum_list += stock_list[i]
    return sum_list


# 大于minum_price的股票的个数
def count_over_min_price_num(stock_list, minum_price):
    length = len(stock_list)
    count = 0
    for i in range(0,length):
        if stock_list[i]>minum_price:
            count += 1
    return count


# 获取average_day均线价格
def get_average_list(stock_prices, average_day):
    length = len(stock_prices)
    i = length - 1
    previous_prices = []
    average_prices = []
    for x in range(0,average_day):
        previous_prices.append(stock_prices[i])
        i = i - 1
    average_prices.append(get_list_sum(previous_prices)/average_day)
    while i >= 0:
        current_price = stock_prices[i]
        prvious_first = previous_prices[0]
        average_first = average_prices[0]
        average_current_sum = average_first * average_day - prvious_first + current_price
        average_prices.insert(0, average_current_sum/average_day)
        del previous_prices[0]
        previous_prices.append(current_price)
        i = i - 1
    return average_prices


# stock_prices：股票价格list
# average_day_buy：买入均线
# average_day_sale：卖出均线
# max_loss：最大损失百分比0.1表示10%
# 具体策略
# 高于average_day_buy均线买入，低于average_day_sale均线卖出
def get_percent(stock_prices, average_day_buy, average_day_sale, max_loss):
    intit_price = 1000000
    all_price = intit_price

    length = len(stock_prices)
    # 如果数据量小于100，直接不判断该股票
    max_average = average_day_buy if average_day_buy>=average_day_sale else average_day_sale
    if length < max_average:
        return -1

    # 求出并存储average_day_buy天均线
    average_prices_buy = get_average_list(stock_prices, average_day_buy)
    # 求出并存储average_day_sale天均线
    average_prices_sale = get_average_list(stock_prices, average_day_sale)

    # 具体策略
    # 高于average_day_buy均线买入，低于average_day_sale均线卖出
    length = len(average_prices_sale) if len(average_prices_sale)>=len(average_prices_sale) else len(average_prices_sale)
    i = length
    # 是否拥有股票
    has_stock = False
    stock_num = 0
    last_all_price = all_price
    while i >= 0:
        if has_stock:
            temp_price = all_price + stock_prices[i] * stock_num * 100 * 0.999
            if (stock_prices[i] < average_prices_sale[i]) or (last_all_price - temp_price)/last_all_price >= max_loss:
                all_price += stock_prices[i] * stock_num * 100 * 0.999
                last_all_price = all_price
                stock_num = 0
                has_stock = False
        else:
            if stock_prices[i] > average_prices_buy[i]:
                stock_num = int(all_price/stock_prices[i]/100)
                all_price -= stock_prices[i] * stock_num * 100
                has_stock = True
        i -= 1
    if has_stock:
        all_price += stock_prices[0] * stock_num * 100
    return (all_price - intit_price)/intit_price


# 具体策略函数
# 高于average_day_buy均线买入，低于average_day_sale均线卖出
def stragy_one():
    stock_percent = []
    for filename in get_file_names(old_data_position):
        filename = old_data_position + '/' + filename
        stock_prices = []
        df_old = pd.read_csv(filename)
        # rows = df_old.head(1)
        length = len(df_old)
        # print(df_old.iat[0,12])
        # #后复权价为第12位
        all_times = 400
        if length >= all_times:
            for x in range(0, all_times):
                stock_prices.append(df_old.iat[x,12])
        else:
            for x in range(0, length):
                stock_prices.append(df_old.iat[x,12])
        current_percent = get_percent(stock_prices, 5, 20, 0.001)
        if current_percent!=-1:
            stock_percent.append(current_percent)
        print(current_percent)
    print('----------end--------')
    print(get_list_sum(stock_percent)/len(stock_percent))
    print('总共的个数')
    print(len(stock_percent))
    print('大于0的个数')
    print(count_over_min_price_num(stock_percent, 0))
    print('大于100%的个数')
    print(count_over_min_price_num(stock_percent, 1))
    print('大于1000%的个数')
    print(count_over_min_price_num(stock_percent, 10))


# 判断该股票是否该买
# stock_prices：股票价格
# below_day：总共天数中小于average_day均线的天数
# all_day：总共天数
# average_day：average_day天均线
def can_buy_below_average(stock_prices, below_day, all_day, average_day):
    length = len(stock_prices)
    #如果数据量小于100，直接不判断该股票
    if length<below_day or length<average_day:
        return False
    average_prices = get_average_list(stock_prices, average_day)
    if len(average_prices)<all_day:
        return False
    count = 0
    for x in range(0, all_day):
        if stock_prices[x]<average_prices[x]:
            count += 1
    if count >= below_day:
        return True
    else :
        return False


# 判断该股票是否可买
def can_buy_by_drop(stock_prices, drop_day, all_day):
    length = len(stock_prices)
    if length<(all_day+5):
        return False
    count = 0
    i = 0
    if stock_prices[0] < stock_prices[1]:
        i = 1
        if stock_prices[1] < stock_prices[2]:
            return False
        else :
            i = 2
    for x in range(i, i+all_day):
        if stock_prices[x] < stock_prices[x+1]:
            count += 1
    if count >= drop_day:
        return True
    else :
        return False


def get_stock_num():
    stock_num = []
    for filename in get_file_names(old_data_position):
        filename = old_data_position + '/' + filename
        stock_prices = []
        df_old = pd.read_csv(filename)
        # rows = df_old.head(1)
        length = len(df_old)
        #print(df_old.iat[0,12])
        #后复权价为第12位
        all_times = 2000
        if length >= all_times:
            for x in range(0, all_times):
                stock_prices.append(df_old.iat[x,12])
        else:
            for x in range(0, length):
                stock_prices.append(df_old.iat[x,12])
        # if can_buy_below_average(stock_prices, 7, 10, 10):
        if can_buy_by_drop(stock_prices, 8, 10):
            stock_num.append(df_old.iat[0,0])
            print(df_old.iat[0,0])
    print('----------end--------')
    print(stock_num)
    print('总共的个数')
    print(len(stock_num))


get_stock_num()
# stragy_one()

# ['sh600071', 'sh600072', 'sh600094', 'sh600181', 'sh600185',
#  'sh600213', 'sh600262', 'sh600398', 'sh600418', 'sh600420', 
#  'sh600511', 'sh600556', 'sh600565', 'sh600603', 'sh600609', 
#  'sh600617', 'sh600666', 'sh600672', 'sh600683', 'sh600753', 
#  'sh600766', 'sh600780', 'sh600785', 'sh600857', 'sh601908', 
#  'sh601965', 'sh603306', 'sh603535', 'sh603600', 'sh603601', 
#  'sh603611', 'sz000023', 'sz000026', 'sz000422', 'sz000535', 
#  'sz000550', 'sz000620', 'sz000752', 'sz000769', 'sz000820', 
#  'sz000851', 'sz000931', 'sz002045', 'sz002053', 'sz002071', 
#  'sz002108', 'sz002183', 'sz002205', 'sz002275', 'sz002407', 
#  'sz002425', 'sz002426', 'sz002588', 'sz002633', 'sz002647', 
#  'sz002697', 'sz002758']