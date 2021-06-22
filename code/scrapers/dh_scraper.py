import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time

def get_section_from_article_url(url):
	match_dict = {
	'/karnataka-districts/' : 'karnataka-districts',
	'/karnataka-politics/' : 'karnataka-politics',
	'/mangaluru' : '---',
	'/state/' : 'state',
	'/national-politics/' : 'national-politics',
	'/north-and-central/' : 'north-and-central',
	'/south/' : 'south',
	'/west/' : 'west',
	'/east-and-northeast/' : '---',
	'/national/' : 'national',
	'/opinion/' : 'opinion'
	}

	for key in match_dict.keys():
		if key in url:
			return match_dict[key]
	return '---'

def get_date_from_url(url):
	date = url.split('/')[-1]
	date = datetime.datetime.strptime(date, "%Y-%m-%d")
	return datetime.datetime.strftime(date, "%d-%m-%Y"), datetime.datetime.strftime(date, "%m-%Y")


# return text and date of news articles of the article with url
def get_text_dh(url):
	try:
		r = requests.get(url)
	except:
		return '', '', ''
	soup = BeautifulSoup(r.content, 'html5lib')

	title = soup.find('meta', property="og:title")['content']

	link_list = soup.find('div', class_="item-list")
	lis = link_list.findAll('li')
	section = lis[-2].text

	article_id = url.split('-')[-1].split('.')[0]
	div = soup.find('div', id = 'node-'+article_id)
	if not div:
		return '', '', ''

	text = ''
	for p in div.findAll('p'):
		if p.find('a'):
			continue
		text += ' ' + p.text

	return title, text, section

# write all articles of a day
def write_day_articles(articles, date, dir_path):
	if not os.path.isdir(dir_path):
		os.mkdir(dir_path)

	file = open(dir_path+'/'+date+'.txt', 'a')
	to_write = ''
	for article in articles:
		title, text, date, section, url = article['title'], article['text'], article['date'], article['section'], article['url']
		to_write = date.strip() + '||' + section + '||' + title + '||' + text.strip() + '||' + url + '\n'
		file.write(to_write)
	
	file.close()

# given a url of a day's archive, write all of its articles of certain sections
# dir path is the main deccan herald path, not the month dir_path
def get_day_articles(url, dir_path):
	date, month = get_date_from_url(url)
	print('\n' + date + '-------------------\n\n')
	dir_path = dir_path + '/' + month

	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html5lib')

	articles = []
	elements = soup.findAll('li', class_='group sanspro-reg archives-note')
	for index, element in enumerate(elements):
		link_element = element.find('a')
		url = 'https://www.deccanherald.com' + link_element['href']
		if get_section_from_article_url(url) == '---':
			continue
		title, text, section = get_text_dh(url)
		if title == '':
			continue
		articles.append({'date':date, 'title':title, 'text':text, 'section':section, 'url':url})
		print(index, section, title)
	write_day_articles(articles, date, dir_path)

# given start date and end date, write articles of the interval (both inclusive)
def write_date_range_articles(start_date, end_date, dir_path):
	cur_date = start_date
	while cur_date <= end_date:
		date_string = datetime.datetime.strftime(cur_date, "%Y-%m-%d")
		url = 'https://www.deccanherald.com/sitemap/detail/days/' + date_string
		print(url)
		get_day_articles(url, dir_path)
		time.sleep(3)
		cur_date += datetime.timedelta(days=1)


start_string = "01-05-2021"
end_string = "31-05-2021"
dir_path = '../../corpus/deccanherald'

start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
write_date_range_articles(start_date, end_date, dir_path)