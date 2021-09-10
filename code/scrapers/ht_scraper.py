import requests
from bs4 import BeautifulSoup 
import os
from time import strptime
import datetime

# compare dates in the format of dd-mm-yyyy, return 1 if d1 is bigger, d2 if d2 is bigger, 0 if d1 and d2 are equal
def compare_dates(d1, d2):
	try:
		date1 = datetime.datetime.strptime(d1.strip(), "%d-%m-%Y")
		date2 = datetime.datetime.strptime(d2.strip(), "%d-%m-%Y")
	except:
		print(d1,d2)
	if date1 < date2 :
		return 2
	if date2 < date1:
		return 1
	return 0

# string of the form "PUBLISHED ON JUN 10, 2021"
def get_date(string):
	if 'UPDATED' in string:
		string = string.replace('UPDATED', 'PUBLISHED')

	string = string.strip()[13:25]
	date = datetime.datetime.strptime(string, "%b %d, %Y")
	return datetime.datetime.strftime(date, "%d-%m-%Y")

def get_text_ht(url):
	headers = {'user-agent' : 'Mozilla/5.0',
	'accept': 'application/json, text/plain, */*'
	}
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.content, 'html5lib')
	try:
		title = soup.find('meta', property='og:title')['content'].strip() # getting article title
	except:
		return '','','',''

	try:
		coverage_div = soup.find('div', id='dataHolder')
		coverage = coverage_div['data-title'].split(',')[0].split()[0]
	except:
		coverage = 'NA'	
	date_string = soup.find("div", class_="dateTime").text.strip()

	text_div = soup.find("div", class_="storyDetails").find("div", class_="detail")
	text_paras = text_div.findAll("p")
	text = ''
	for p in text_paras:
		text += p.text

	date = get_date(date_string)
	return title, date, coverage, text


def get_filepath(dir_path, date, section):
	section = section.split('-')[0]
	month = date[3:]
	cur_dir_path = dir_path + '/' + month
	if not os.path.exists(cur_dir_path):
		os.makedirs(cur_dir_path)
	cur_dir_path = cur_dir_path + '/' + section.lower()
	if not os.path.exists(cur_dir_path):
		os.makedirs(cur_dir_path)
	return cur_dir_path + '/' + date + '.txt'

def write_page_articles(articles, dir_path, section):
	for article in articles:
		title, coverage, text, date, url = article['title'], article['coverage'], article['text'], article['date'], article['url']
		filepath = get_filepath(dir_path, date, section)
		file = open(filepath, 'a')
		to_write = date.strip() + '||' + coverage + '||' + title + '||' + text.strip() + '||' + url + '\n'
		file.write(to_write)
		file.close()

def get_page_articles(url, beg_date, end_date, dir_path, section):
	headers = {'user-agent' : 'Mozilla/5.0',
	'accept': 'application/json, text/plain, */*'
	}
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.content, 'html5lib')
	
	articles = []
	h2s = soup.findAll("h2", class_ = "hdg3")
	for index, h2 in enumerate(h2s):
		link = 'https://www.hindustantimes.com' + h2.find("a")['href']

		if '/india-news' not in url and '/india-news/' in link:
			print("india news")
			continue
		if '/opinion/' in url and '/opinion' not in link:
			print("not opinion")
			continue
		if '/editorials/' in url and '/editorials' not in link:
			print("not editorials")
			continue
		if '/analysis/' in url and '/analysis' not in link:
			print("not analysis")
			continue
		
		title, date, coverage, text = get_text_ht(link)		
		if title == '':
			continue
		articles.append({'title':title, 'coverage':coverage, 'text':text, 'date':date, 'url':link})
		print(index, date, title)
	write_page_articles(articles, dir_path, section)
		
beg = 19
end = 24
section = 'editorials'

# beg = 10
# end = 27
# section = 'analysis'

# beg = 2
# end = 61
# section = 'opinion'

# beg = 1558
# end = 1600
# section = 'india-news'

# beg = 2301
# end = 2400			# mar 07 2021
# section = 'cities'

# beg = 700
# end = 750
# section = 'world-news'

cur = beg
dir_path = '../../corpus/hindustantimes'

while cur <= end:
	url = 'https://www.hindustantimes.com/' + section + '/page-' + str(cur)
	print(url + "\n")
	get_page_articles(url, dir_path, section)
	print("\n\n")
	cur += 1

# url = 'https://www.hindustantimes.com/india-news/odisha-sounds-flood-alert-ahead-of-low-pressure-in-bay-of-bengal-101623306134630.html'
# get_text_ht(url)

# url = 'https://www.hindustantimes.com/cities/chandigarh-news/mixed-cropping-gaining-ground-in-rural-chamba-101623308717630.html'
# get_text_ht(url)


# beg = 1
# end = 35
# section = 'topic/farmers-protest'

# beg = 1
# end = 5
# section = 'topic/farm-bill'

# beg = 1
# end = 3
# section = 'topic/farm-bills'

# beg = 1
# end = 10
# section = 'topic/farm-laws'

# beg = 1
# end = 5
# section = 'topic/farmers'
