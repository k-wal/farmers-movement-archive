import requests
from bs4 import BeautifulSoup 
import os
from time import strptime

# take date from article and format in dd-mm-yyyy format
def format_date(date):
	date = date.replace(',','')
	date = date.split(' ')
	month, day, year = str(strptime(date[0],'%b').tm_mon) , date[1], date[2]
	if len(month) == 1:
		month = '0'+month
	date = day + '-' + month + '-' + year
	return date

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
		

def get_page_articles(url):
	main_url = 'https://www.tribuneindia.com'
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')
	card_titles = soup.findAll('h4', class_='ts-card-title')

	first_card_title = soup.find('h4', class_='card-title')
	card_titles.insert(0,first_card_title)
	articles = []
	for i,ct in enumerate(card_titles):
		link = main_url + ct.find('a')['href']
		a,b,title,d = get_text_tribune(link)
		if title=='':
			continue
		print(i,title)		
		articles.append([a,b,title,d,link])
	# store_articles(articles, '../corpus/tribune/amritsar')
	# store_articles(articles, '../corpus/tribune/punjab')
	store_articles(articles, '../corpus/tribune/haryana')



cur = 145
end = 150

punjab_id = '45'
haryana_id = '28'
delhi_id = '24'
amritsar_id = '17'

while cur<=end:
	# url = 'https://www.tribuneindia.com/Pagination/ViewAll?id='+amritsar_id+'&page='+str(cur)+'&topNews='
	# url = 'https://www.tribuneindia.com/Pagination/ViewAll?id='+punjab_id+'&page='+str(cur)+'&topNews='
	url = 'https://www.tribuneindia.com/Pagination/ViewAll?id='+haryana_id+'&page='+str(cur)+'&topNews='

	print(url)
	print('-'*15)
	get_page_articles(url)
	print('\n-----\n\n')
	cur += 1