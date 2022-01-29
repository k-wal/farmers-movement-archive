import os
import sys
import datetime
import matplotlib.pyplot as plt


# return true if article is relevant, false otherwise
def check_article_relevance(title, desc):
	keywords = [
	'kisan sabha',
	'bku',
	'tikri', 
	'singhu', 
	'anti-farmer',
	'agri-reform',
	'farm bill',
	'farm bills',
	'farmers bills',
	'farmers\' bills',
	'farm policy',
	'farm policies',
	'pro-farmer',
	'Essential Commodities (Amendment) Bill, 2020',
	'Essential Commodities Bill, 2020',
	'Essential Commodities Act, 2020',
	'agri bill',
	'agri ordinance',
	'farm ordinance',
	'trolley times',
	'Kisan Sangharsh Committee',
	'Kisan Bachao Morcha',
	'Kisan Mazdoor Sangharsh Committee',
	'Jai Kisan Andolan',
	'Punjab Kisan Union',
	'Kirti Kisan Union',
	'Terai Kisan Sangathan',
	'All India Kisan Sabha',
	'Mahila Kisan Adhikar Manch',
	'Doaba Kisan Samiti',
	'Rakesh Tikait',
	'Bhartiya Kisan Union']

	title = title.lower()
	desc = desc.lower()
	for keyword in keywords:
		keyword = keyword.lower()
		if keyword in title or keyword in desc:
			return True
	return False

# get list of text from all relevant articles from one file
def get_file_relevant_text(filepath):
	file = open(filepath, 'r')
	lines = file.readlines()
	file.close()
	all_articles = []
	for line in lines:
		try:
			parts = line.strip().split('||')
			title, desc = parts[2], parts[3]
		except:
			continue
		if check_article_relevance(title, desc):
			all_articles.append(desc)
	return all_articles

# number of articles that have the _keyword_ in the file at _filepath_
def get_file_keyword_count(keywords, filepath):
	articles = get_file_relevant_text(filepath)
	count = 0
	keywords = [keyword.lower() for keyword in keywords]
	for article in articles:
		for kw in keywords:
			if kw in article.lower():
				count += 1
				break

	return count

# return total number of articles, array of articles per day
# that contain the keyword (s)
def get_month_keyword_count(keyword, dir_path):
	filenames = os.listdir(dir_path)
	filenames.sort()
	total = 0
	counts = []
	for filename in filenames:
		filepath = dir_path + '/' + filename
		month_count = get_file_keyword_count(keyword, filepath)
		total += month_count
		counts.append(month_count)
	return total, counts


def get_interval_keyword_count(keyword, start_string, end_string, dir_path):
	start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
	end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
	date = start_date
	counts = []
	while date <= end_date:
		month_path = dir_path + '/' + date.strftime("%m-%Y")
		filename = date.strftime("%d-%m-%Y") + '.txt'
		if len(counts) % 50 == 0:
			print(keyword[0], filename)	
	
		if filename not in os.listdir(month_path):
			counts.append(0)
			date += datetime.timedelta(days=1)
			continue

		filepath =  month_path + '/' + filename
		counts.append(get_file_keyword_count(keyword, filepath))

		date += datetime.timedelta(days=1)

	return counts

def get_span_counts(start_string, end_string, counts, day_span):
	counts = [sum(counts[i:i+day_span]) for i in range(0, len(counts), day_span)]
	start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
	end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
	dates = [(start_date + datetime.timedelta(days=x)).strftime("%d-%m-%y") for x in range(0, (end_date-start_date).days, day_span)]
	return counts, dates

def plot_interval_keywors_sets(keyword_sets, start_string, end_string, dir_path, day_span=20):
	plt.rc('xtick', labelsize=8)
	colors = ['blue', 'orange', 'green', 'cyan', 'deeppink', 'red', 'purple', 'saddlebrown']

	for i,keywords in enumerate(keyword_sets):
		counts = get_interval_keyword_count(keywords, start_string, end_string, dir_path)
		counts, dates = get_span_counts(start_string, end_string, counts, day_span)
		plt.plot(dates, counts, colors[i], label=' / '.join(keywords), linewidth=2.0)
		# plt.plot(list(range(int(years[0]), int(years[-1])+1)), title_counts, 'b', label='# title')
	
	plt.ylabel('number of articles')
	plt.xlabel('date')
	plt.legend()

	plt.show()


start_string = '01-10-2020'
end_string = '31-12-2021'
dir_path = '../../../../corpus/hindu'

keyword_sets = [
			['maharashtra'],
			['punjab'],
			['haryana'],
			['u.p', 'uttar pradesh'],
			['delhi'],
			['uttarakhand'],
			['bengal']
			]

plot_interval_keywors_sets(keyword_sets, start_string, end_string, dir_path)