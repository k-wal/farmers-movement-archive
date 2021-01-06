import os
import re
import operator
import matplotlib.pyplot as plt

# function that takes in filename and returns the number of articles(lines)
def get_day_article_total(filename):
	file = open(filename, 'r')
	n = len(file.readlines())
	file.close()
	return n

# add all articles in each file in dir_path
def get_total_articles(dir_path):
	total = 0
	files = os.listdir(dir_path)
	for file in files:
		filename = dir_path + '/' + file
		total += get_day_article_total(filename)
	return total

# number of times keyword occurs in date in filename
def get_keyword_count_day(filename, keyword):
	file = open(filename, 'r')
	lines = file.readlines()
	file.close()
	count = 0

	for line in lines:
		parts = line.split('||')
		date, location, title, text = parts[0], parts[1], parts[2], parts[3]
		if keyword in title.lower() or keyword in text.lower():
			count += 1

	return count

def get_keyword_counts_total(dir_path, keyword):
	total = 0
	files = os.listdir(dir_path)
	for file in files:
		filename = dir_path + '/' + file
		total += get_keyword_count_day(filename, keyword)
	return total


# return [count, day, month, year], where count is the number of articles with keyword in text/title
def get_keywords_count_with_date(filename, keywords):
	date = filename.split('/')[-1]
	date = date.split('.')[0]
	date = date.split('-')
	day, month, year = date[0], date[1], date[2]
	file = open(filename, 'r')
	lines = file.readlines()
	file.close()
	count = 0

	for line in lines:
		parts = line.split('||')
		date, location, title, text = parts[0], parts[1], parts[2], parts[3]

		# if any keyword is present, increase count
		for keyword in keywords:
			if keyword in title.lower() or keyword in text.lower():
				count += 1
				break

	return [count, day, month, year]


# given counts : list of [count, day, month, year], creates graph
def create_keywords_graph(counts):
	# creating lists for plotting
	count_list = [x[0] for x in counts]
	month_list = []
	tick_locs = []
	remainder = 0
	for i,count in enumerate(counts):
		# show every nth date
		if remainder == 35:
			month_list.append(count[1] + '/' + count[2] + '/' + count[3][2:4])
			tick_locs.append(i)
			remainder = 0
		else:
			remainder += 1

	plt.plot(range(len(count_list)), count_list, 'r', label='# articles with '+', '.join(keywords))
	plt.xticks(tick_locs,month_list)
	plt.title('keywords : ' + ', '.join(keywords))
	plt.ylabel('number of articles')
	plt.xlabel('date')
	plt.legend()
	plt.show()

# givend path to corpus and list of keywords, create a graph of number of occurences vs time
def get_keywords_timeline(dir_path, keywords):
	counts = []
	files = os.listdir(dir_path)
	for file in files:
		filename = dir_path + '/' + file
		counts.append(get_keywords_count_with_date(filename, keywords))
	counts = sorted(counts, key=operator.itemgetter(3,2,1)) # sorting according to date
	create_keywords_graph(counts)


corpus_path = '../corpus/hindu'

total_articles = get_total_articles(corpus_path)
print('total number of articles : ' + str(total_articles))

keyword = 'farmer'
total_keyword_articles = get_keyword_counts_total(corpus_path, keyword)
print('total articles with keyword ' + keyword + ' in them  : ' + str(total_keyword_articles))

keyword = 'msp'
total_keyword_articles = get_keyword_counts_total(corpus_path, keyword)
print('total articles with keyword ' + keyword + ' in them  : ' + str(total_keyword_articles))

keyword = 'apmc'
total_keyword_articles = get_keyword_counts_total(corpus_path, keyword)
print('total articles with keyword ' + keyword + ' in them  : ' + str(total_keyword_articles))

keyword = 'esca'
total_keyword_articles = get_keyword_counts_total(corpus_path, keyword)
print('total articles with keyword ' + keyword + ' in them  : ' + str(total_keyword_articles))


# GRAPH
keywords = ['farmer']
get_keywords_timeline(corpus_path, keywords)

