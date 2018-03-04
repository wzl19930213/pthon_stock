import tkinter as tk
import tushare as ts
import matplotlib.pyplot as plt

""" 获取一天内1min线的曲线图
    可以连续获取多天 """

code = '600000'
date = '2018-01-14'
# 获取连接备用
conn = ts.get_apis()
# 分钟数据, 设置freq参数，分别为1min/5min/15min/30min/60min，D(日)/W(周)/M(月)/Q(季)/Y(年)
df = ts.bar(code, conn=conn, freq='1min', start_date=date, end_date='')
ts.close_apis(conn)
start_end = [0, len(df)/240]
print(start_end[1])


# 建立tkinter窗口，设置窗口标题
window = tk.Tk()
window.title("股票当日分钟线")
#窗口大小
width, height = 800, 420
#窗口居中显示
window.geometry('%dx%d+%d+%d' % (width, height, (window.winfo_screenwidth() - width) / 2
                                 , (window.winfo_screenheight() - height) / 2))
#窗口最大值
window.maxsize(800, 420)
#窗口最小值
window.minsize(800, 420)

def put_pic():
    canvas = tk.Canvas(window, height=200, width=500)
    image_file = tk.PhotoImage(file='cache\pic.gif')
    image = canvas.create_image(0, 0, anchor='nw', image=image_file)
    canvas.pack(side='top')


def change_pic(src):
    image_load_change = tk.PhotoImage(file=src)
    label.bm = image_load_change
    label.configure(image=image_load_change)


def pre_pic():
    if start_end[0] >= (start_end[1] - 1):
        return
    else:
        start_end[0] += 1
    x = []
    y = []
    for i in range(start_end[0]*240, start_end[0]*240+240):
        x.append(240-i)
        y.append(df.iat[i, 2])
    plt.plot(x, y)
    fig = plt.gcf()
    fig.set_size_inches(8, 3.5)
    fig.savefig('cache/next.png', dpi=100)
    # plt.savefig('cache/next.png')
    plt.close()
    change_pic('cache/next.png')


def next_pic():
    if start_end[0] <= 0:
        return
    else:
        start_end[0] -= 1
    x = []
    y = []
    for i in range(start_end[0]*240, start_end[0]*240+240):
        x.append(240-i)
        y.append(df.iat[i, 2])
    plt.plot(x, y)
    fig = plt.gcf()
    fig.set_size_inches(8, 3.5)
    fig.savefig('cache/next.png', dpi=100)
    # plt.savefig('cache/next.png')
    plt.close()
    change_pic('cache/next.png')


# login and sign up button
btn_pre = tk.Button(window, text='前\n一\n天', command=pre_pic, width=2, height=3)
btn_pre.place(x=10, y=height/2-20)
btn_next = tk.Button(window, text='下\n一\n天', command=next_pic, width=2, height=3)
btn_next.place(x=width-40, y=height/2-20)

image_load = tk.PhotoImage(file='cache/next.png')
label = tk.Label(window, image=image_load)
label.bm = image_load
label.place(x=46, y=10, width=700, height=400)

start_end[0] += 1
next_pic()


# 运行并显示窗口
window.mainloop()


