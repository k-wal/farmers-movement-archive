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

# compare dates in the format of dd-mm-yyyy, return 1 if d1 is bigger, else return 2
def compare_dates(d1, d2):
	date1 = datetime.datetime.strptime(d1, "%d-%m-%Y")
	date2 = datetime.datetime.strptime(d2, "%d-%m-%Y")
	if date1 < date2 :
		return 2
	else:
		return 1


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
	if location == '':
		location = '---'

	text = ''
	for p in story_para[3:]: # adding all rest paragraphs to get text
	 	text += p.text
	text = text.replace('\n',' ')
	return date, location, title, text


def store_articles(articles, dir_path):
	file_handlers = {}
	for article in articles:
		date, location, title, text, url = article[0], article[1], article[2], article[3], article[4]
		if date not in file_handlers.keys():
			f = open(dir_path+'/'+date+'.txt','a')
			file_handlers[date] = f
		f = file_handlers[date]
		to_write = date.strip() + '||' + location + '||' + title + '||' + text.strip() + '||' + url + '\n'
		f.write(to_write)

	for date in file_handlers.keys():
		file_handlers[date].close()
		

def get_page_articles(url, dir_path, till_date = "none"):
	if_end_reached = False

	main_url = 'https://www.tribuneindia.com'
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')
	card_titles = soup.findAll('h4', class_='ts-card-title')

	first_card_title = soup.find('h4', class_='card-title')
	card_titles.insert(0,first_card_title)
	articles = []
	for i,ct in enumerate(card_titles):
		if not ct:
			continue
		link = main_url + ct.find('a')['href']
		date,b,title,d = get_text_tribune(link)
		if compare_dates(date, till_date) == 2:					# if end date is reached in the page, return true so that scraping stops
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

# date has to be in dd-mm-yyyy format
def write_all_sections(main_dir_path, till_date = "none"):
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
			to_continue = not get_page_articles(url, dir_path, till_date)
			print('\n-----\n\n')
			page += 1
		print("\n\n SECTION ENDING : " + cur_section + "\n-----")
		




# cur = 13
# end = 50

# dir_path = '../../corpus/tribune/feature'

# while cur<=end:
# 	url = 'https://www.tribuneindia.com/Pagination/ViewAll?id='+feature_id+'&page='+str(cur)+'&topNews='

# 	print(url)
# 	print('-'*15)
# 	get_page_articles(url, dir_path)
# 	print('\n-----\n\n')
# 	cur += 1