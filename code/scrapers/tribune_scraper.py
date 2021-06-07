import requests
from bs4 import BeautifulSoup 
import os
from time import strptime
import datetime

# take date from article and format in dd-mm-yyyy format
def format_date(date):
	date = date.replace(',','')
	date = date.split(' ')
	month, day, year = str(strptime(date[0],'%b').tm_mon) , date[1], date[2]
	if len(month) == 1:
		month = '0'+month
	date = day + '-' + month + '-' + year
	return date

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


def get_text_tribune(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')
	try:
		title = soup.find('meta', property='og:title')['content'] # getting article title
	except:
		return '','','',''

	date_div = soup.find('div', class_='time-share') # getting and formatting date
	date = date_div.findAll('span')[0].text.strip()
	date = format_date(date)


	story = soup.find('div',class_='story-desc') # getting story div
	story_para = story.findAll('p') # getting all paragraphs in story div
	
	try:
		location = story_para[2].text.split(',')[0] # third paragraph contains location
	except:
		return date, '---', title, ''

	location = location.split(':')[0]
	if location.lower() == 'tribune news service':
		location = ''
	if 'tribune news service' in location.lower():
		try:
			location = location.split('Tribune News Service')[1]
		except:
			location = ''
	if location.strip() == '':
		location = '---'

	text = ''
	for p in story_para[3:]: # adding all rest paragraphs to get text
	 	text += p.text
	text = text.replace('\n',' ')
	return date, location, title.strip(), text


def store_articles(articles, dir_path):
	file_handlers = {}
	for article in articles:
		date, location, title, text, url = article[0], article[1], article[2], article[3], article[4]
		if date not in file_handlers.keys():
		
			cur_dir_path = dir_path + '/' + '-'.join(date.split('-')[1:])
			if not os.path.exists(cur_dir_path):
				os.makedirs(cur_dir_path)

			f = open(cur_dir_path+'/'+date+'.txt','a')
			file_handlers[date] = f
		f = file_handlers[date]
		to_write = date.strip() + '||' + location + '||' + title + '||' + text.strip() + '||' + url + '\n'
		f.write(to_write)

	for date in file_handlers.keys():
		file_handlers[date].close()
		

def get_page_articles(url, dir_path, start_date, end_date = "none"):
	if_end_reached = False

	main_url = 'https://www.tribuneindia.com'
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')
	card_titles = soup.findAll('h4', class_='ts-card-title')

	first_card_title = soup.find('h4', class_='card-title')
	card_titles.insert(0,first_card_title)
	articles = []


	# if date of last article in the page is after the ending date, go to the next page directly
	last_ct = card_titles[-1]
	if last_ct:
		link = main_url + last_ct.find('a')['href']
		date,b,title,d = get_text_tribune(link)
		if date and compare_dates(date, end_date) == 1:
			return False

	for i,ct in enumerate(card_titles):
		if not ct:
			continue
		link = main_url + ct.find('a')['href']
		date,b,title,d = get_text_tribune(link)
		
		if not date:
			continue
		if compare_dates(date, end_date) == 1:			# if date is after end date, continue
			continue
		if compare_dates(date, start_date) == 2:		# if date is before start date, return true so that scraping stops
			if_end_reached = True			
			break
		if title=='':
			continue
		print(i,title)		
		articles.append([date,b,title,d,link])
	# store_articles(articles, '../corpus/tribune/delhi')
	store_articles(articles, dir_path)
	return if_end_reached


# return array with section names and respective ids
def get_sections_ids():
	return [['comment','59'],
	['musing','62'],
	['business','19'],
	['punjab','45'],
	['haryana','28'],
	['amritsar','17'],
	['bathinda','18'],
	['delhi','24'],
	['chandigarh','20'],
	['jalandhar','34'],
	['nation','42'],
	['editorial','60'],
	['ludhiana','40'],
	['patiala','213'],
	['himachalpradesh','30'],
	['jammukashmir','36']
	]

# write one section, section_name:name of section, main_dir_path (not the section dir path), start_date and end_date are both
# included in the interval of scraping, format : dd-mm-yyyy
def write_one_section(section_name, main_dir_path, start_date, end_date):
	section_id_arr = get_sections_ids()
	section_id = [row[1] for row in section_id_arr if row[0]==section_name][0]

	print("\n\n SECTION BEGINNING : " + section_name + "\n--")

	dir_path = main_dir_path + '/' + section_name
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	page = 1
	to_continue = True

	while to_continue:														#scrape till end is not reached
		url = 'https://www.tribuneindia.com/Pagination/ViewAll?id='+section_id+'&page='+str(page)+'&topNews='
		print(url)
		print('-'*15)
		to_continue = not get_page_articles(url, dir_path, start_date, end_date)
		print('\n-----\n\n')
		page += 1
		print("\n\n SECTION ENDING : " + section_name + "\n-----")


# date has to be in dd-mm-yyyy format
def write_all_sections(main_dir_path, start_date, end_date):
	section_id_arr = get_sections_ids()
	for section_id in section_id_arr:
		cur_section = section_id[0]
		cur_id = section_id[1]
		print("\n\n SECTION BEGINNING : " + cur_section + "\n--")

		dir_path = main_dir_path + '/' + cur_section
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

		page = 1
		to_continue = True

		while to_continue:														#scrape till end is not reached
			url = 'https://www.tribuneindia.com/Pagination/ViewAll?id='+cur_id+'&page='+str(page)+'&topNews='
			print(url)
			print('-'*15)
			to_continue = not get_page_articles(url, dir_path, start_date, end_date)
			print('\n-----\n\n')
			page += 1
		print("\n\n SECTION ENDING : " + cur_section + "\n-----")
		
