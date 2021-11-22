import os
import re
import datetime

def combine_date(date, dir_path):
	titles = []
	articles = []

	month = datetime.datetime.strftime(date, "%m-%Y")
	filename = datetime.datetime.strftime(date, "%d-%m-%Y.txt")

	out_dir_path = dir_path + '/combined/' + month
	if not os.path.exists(out_dir_path):
		os.makedirs(out_dir_path)
	outfile = open(out_dir_path + '/' + filename, 'w')

	for section in os.listdir(dir_path):
		if section == 'combined':
			continue
		filepath = dir_path + '/' + section + '/' + month + '/' + filename
		if filename not in os.listdir(dir_path + '/' + section + '/' + month):
			continue

		file = open(filepath, 'r')
		lines = file.readlines()
		file.close()

		for line in lines:
			title = line.split('||')[2]
			# except:
			# 	print(line)
			# 	continue
			if title in titles:
				continue
			outfile.write(line)
			titles.append(title)
	outfile.close()


def combine_interval(start_string, end_string, dir_path):
	start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
	end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
	date = start_date
	while date <= end_date:
		print(date)
		combine_date(date, dir_path)
		date += datetime.timedelta(days=1)


start_string = "01-07-2021"
end_string = "31-10-2021"
dir_path = '../../corpus/telegraph'
combine_interval(start_string, end_string, dir_path)