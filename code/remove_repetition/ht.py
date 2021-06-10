import os
import sys
import re

def remove_file_repetitions(path):
	# file = open(path, 'r')
	# content = file.read()
	# file.close()

	# content = re.sub('\|\|\n[\n|\s]*\|\|','||---||',content)
	# content = re.sub('\n[\n|\s]*\|\|','---||',content)
	
	# file = open(path, 'w')
	# file.write(content)
	# file.close()

	file = open(path, 'r')
	lines = file.readlines()
	file.close()

	file = open(path, 'w')
	titles = []


	for line in lines:
		# print(line)
		parts = line.split('||')
		try:
		 	title = parts[2]
		except:
			continue
		if title in titles:
			continue
		titles.append(title)
		file.write(line)

	file.close() 



def remove_repetitions_directory(dir_path):
	filenames = os.listdir(dir_path)
	for filename in filenames:
		remove_file_repetitions(dir_path + '/' + filename)

# dir_path = '../../corpus/ht'
# months = os.listdir(dir_path)
# for month in months:
# 	remove_repetitions_directory(dir_path + '/' + month)


dir_path = '../../corpus/hindustantimes'
months = os.listdir(dir_path)
for month in months:
	print("-----" + month + "-----")
	path = dir_path + '/' + month
	sections = os.listdir(path)
	for section in sections:
		print(section)
		remove_repetitions_directory(path + '/' + section)
	print("\n\n")