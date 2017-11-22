import tushare as ts
import time
import json

file_location = 'G:/python/stock/data/'
init_time = '2017-01-01'
current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))

##保存数据
##code: 股票代码
##start_time: 保存开始时间
##end_time: 保存结束时间
def save_data(code, start_time, end_time):
	filename = file_location + code + '.json'
	data = ts.get_h_data(code, start=start_time, end=end_time)
	data.to_json(filename, orient='records')
	with open(filename, 'a') as f_new:
		f_new.write('\n' + start_time + ' ' + end_time)

##更新数据
##code: 股票代码
##end_time: 更新结束时间, 默认当前时间
def update_data(code, end_time=current_time):
	filename = file_location + code + '.json'
	temp_filename = file_location + 'temp.json'
	try:
		with open(filename) as file_old:
			count = 0
			date = ''
			data_old = ''
			for line in file_old:
				if count == 0:
					data_old = json.loads(line)
				elif count == 1:
					date = line
				count = count + 1
			if date:
				time_old = date.split()
				start_time_old = time_old[0]
				end_time_old = time_old[1]
				data = ts.get_h_data(code, start=end_time_old, end=end_time)
				data.to_json(temp_filename, orient='records')
				with open(temp_filename) as f_temp:
					data_temp = json.load(f_temp)
				if data_temp:
					data_temp.pop()
					data_new = data_temp + data_old
					with open(filename, 'w') as f_new:
						json.dump(data_new, f_new)
					with open(filename, 'a') as f_object:
						f_object.write('\n' + start_time_old + ' ' + end_time)
			else:
				#重新获取
				pass
			#file_object.write("I love creating apps that can run in a browser.\n")
	except FileNotFoundError:
		data = ts.get_h_data(code, start=init_time, end=end_time)
		data.to_json(filename, orient='records')
		with open(filename, 'a') as f_new:
			f_new.write('\n' + init_time + ' ' + '2017-02-01')


#save_data('002337', '2017-10-23', '2017-10-25')
update_data('002337')

