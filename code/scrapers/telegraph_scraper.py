import requests
from bs4 import BeautifulSoup 
import os
from time import strptime
import datetime

def get_section(url):
	section_dict = {
	'/opinion/' : 'Opinion',
	'/india/' : 'India',
	'/west-bengal/calcutta/' : 'Calcutta',
	'/business/' : 'Business',
	'/west-bengal/' : 'West Bengal',
	'/north-east/' : 'North East',
	'/jharkhand' : 'Jharkhand'
	}

	for key in section_dict.keys():
		if key in url:
			return section_dict[key]
	print("ERROR : ", url)

# compare dates in the format of dd-mm-yyyy, return 1 if d1 is bigger, d2 if d2 is bigger, 0 if d1 and d2 are equal
def compare_dates(d1, d2):
	if date1 < date2 :
		return 2
	if date2 < date1:
		return 1
	return 0

def get_date(text):
	date = text.split(' ')[1]
	return datetime.datetime.strptime(date, '%d.%m.%y')

def get_text_telegraph(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')
	try:
		title = soup.find('meta', property='og:title')['content'] # getting article title
	except:
		return '', '', ''

	divs = soup.findAll('div', class_='fs-17 pt-2 noto-regular')
	text = ''
	for div in divs:
		paras = div.findAll('p')
		for p in paras:
			text += p.text.strip() + ' '
	section = get_section(url)
	# print(title)
	# print(section)
	# print(text)
	return title, text, section


def is_article_after_interval(div, end_date):
	date = get_date(div.find('span').text)
	if end_date < date:
		return True
	return False


def store_articles(articles, dir_path):
	file_handlers = {}
	for article in articles:
		date, section, title, text, url = article['date'], article['section'], article['title'], article['text'], article['url']
		month = datetime.datetime.strftime(date, "%m-%Y") 
		date = datetime.datetime.strftime(date, "%d-%m-%Y")

		if date not in file_handlers.keys():
			cur_dir_path = dir_path + '/' + month
			if not os.path.exists(cur_dir_path):
				os.makedirs(cur_dir_path)

			f = open(cur_dir_path+'/'+date+'.txt','a')
			file_handlers[date] = f
		f = file_handlers[date]
		try:
			to_write = date + '||' + section + '||' + title + '||' + text.strip() + '||' + url + '\n'
		except:
			print("ERROR 3 : ", url)
			continue
		f.write(to_write)

	for date in file_handlers.keys():
		file_handlers[date].close()


def get_page_articles(url, start_date, end_date, dir_path):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')
	divs = soup.findAll('div', class_='row pb-3 pt-3')[1:]

	if is_article_after_interval(divs[-1], end_date):
		print('* * SKIP * *')
		return False
	if_end_reached = False

	articles = []
	for i, div in enumerate(divs):
		link = 'https://www.telegraphindia.com' + div.find('a')['href']
		
		date = get_date(div.find('span').text)

		if date > end_date:			# if date is after end date, continue
			continue
		if date < start_date:		# if date is before start date, return true so that scraping stops
			if_end_reached = True			
			break

		title, text, section = get_text_telegraph(link)
		if title == '':
			print("ERROR 2 : ", link)
			continue
		print(i, title)
		articles.append({'title':title, 'text':text, 'section':section, 'date':date, 'url':url})

	store_articles(articles, dir_path)
	return if_end_reached


# write one section, section_name:name of section, main_dir_path (not the section dir path), start_date and end_date are both
# included in the interval of scraping, format : dd-mm-yyyy
def write_one_section(section_name, main_dir_path, start_date, end_date):
	print("\n\n SECTION BEGINNING : " + section_name + "\n--")

	dir_path = main_dir_path + '/' + section_name
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	if section_name == 'calcutta':
		section_name = 'west-bengal/calcutta'

	page = 1
	to_continue = True

	while to_continue:														#scrape till end is not reached
		url = 'https://www.telegraphindia.com/'+ section_name +'/page-'+str(page)
		print(url)
		print('-'*15)
		to_continue = not get_page_articles(url, start_date, end_date, dir_path)
		print('\n-----\n\n')
		page += 1
		print("\n\n SECTION ENDING : " + section_name + "\n-----")


section_name = 'north-east'
start_date = "01-08-2020"
end_date = "31-12-2020"
dir_path = '../../corpus/telegraph'

start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y")
write_one_section(section_name, dir_path, start_date, end_date)


# url = 'https://www.telegraphindia.com/west-bengal/page-100'
# get_page_articles(url, '', '')

# url = 'https://www.telegraphindia.com/west-bengal/west-bengal-assembly-elections-2021-posters-mimic-pm-taunt/cid/1812647'
# get_text_telegraph(url)