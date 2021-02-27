import os
import sys
import re

def remove_file_repetitions(path):
	file = open(path, 'r')
	content = file.read()
	file.close()

	content = re.sub('\|\|\n[\n|\s]*\|\|','||---||',content)
	content = re.sub('\n[\n|\s]*\|\|','---||',content)
	
	file = open(path, 'w')
	file.write(content)
	file.close()

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


remove_repetitions_directory('../../corpus/tribune/feature')
