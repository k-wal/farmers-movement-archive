import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time

class TOIScraper:

	# get coverage/section from article URl
	def get_article_coverage(self, url):
		if '/india/' in url:
			return 'India'
		if '/city/' in url:
			city = url.split('/city/')[1]
			city = city.split('/')[0]
			city = city.capitalize()
			return city
		if '/world/' in url:
			return 'World'
		if '/business/' in url:
			return 'Business'
		if '/sports/' in url:
			return 'Sports'
		if '/home/' in url:
			return 'Home'
		return '---'

	# get text, title etc from article url
	def get_text(self, url):
		try:
			r = requests.get(url)
		except:
			return '', '', '', '', ''
		soup = BeautifulSoup(r.content, 'html5lib')

		divs = soup.findAll('div')

		try:
			title = soup.find('div', class_='_1Vd7A').text.strip()
		except:
			return '', '', '', '', ''

		try:
			author_div = soup.find('div', class_='yYIu- byline')
			author = author_div.find('a').text.strip()
		except:
			author = '---'

		try:
			date_div = soup.find('div', class_='j9QAQ')
			date = date_div.text.strip().split('from ')[1]
		except:
			date = '---'

		coverage = self.get_article_coverage(url)

		text = soup.find('div', class_='_3YYSt clearfix').text.strip()
		
		return title, text, date, coverage, author

	# write articles of one day
	def write_day_articles(self, articles, filename, dir_path):
		if not os.path.isdir(dir_path):
			os.mkdir(dir_path)
		overall_date = ''
		for article in articles:
			title, text, date, coverage, url, author = article['title'], article['text'], article['date'], article['coverage'], article['url'], article['author']

			file = open(dir_path+'/'+filename+'.txt', 'a')
			to_write = date.strip() + '||' + coverage + '||' + title + '||' + text.strip() + '||' + url + '||' + author + '\n'
			file.write(to_write)
			file.close()

	# get all articles of a day and send them to be printed
	def get_day_articles(self, url, date, dir_path):
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html5lib')
		dir_path +=  '/' + datetime.datetime.strftime(date, "%m-%Y")
		filename = datetime.datetime.strftime(date, "%d-%m-%Y")

		articles = []
		spans = soup.findAll('span', style="font-family:arial ;font-size:12;color: #006699")
		hrefs = spans[0].findAll("a")
		hrefs.extend(spans[1].findAll("a"))
		print(len(hrefs))

		for index, href in enumerate(hrefs):
			link = href['href']
			if 'http' not in link:
				link = 'https://timesofindia.indiatimes.com' + link
			if 'sports' not in link and '/entertainment/' not in link and '/astrology/' not in link and '/life-style/' not in link and '/tv/' not in link and '/web-series/' not in link:
				title, text, date, coverage, author = self.get_text(link)
				if title == '':
					continue
				print(index, title)
				articles.append({'title':title, 'text':text, 'date':date,'coverage' : coverage, 'url':link, 'author':author})
		self.write_day_articles(articles, filename, dir_path)

	# write articles from start_date to end_date; start_date and end_date are datetime.datetime types
	def write_date_range_articles(self, start_date, end_date, dir_path):
		# id for 2020 jan 1
		initial_id = 43831
		cur_id = initial_id + (start_date - datetime.datetime.strptime("01-01-2020", "%d-%m-%Y")).days

		cur_date = start_date
		while cur_date <= end_date:
			date_string = datetime.datetime.strftime(cur_date, "%d-%m-%Y")
			d = str(int(datetime.datetime.strftime(cur_date, "%d")))
			m = str(int(datetime.datetime.strftime(cur_date, "%m")))
			y = str(int(datetime.datetime.strftime(cur_date, "%Y")))
			url = 'https://timesofindia.indiatimes.com/'+y+'/'+m+'/'+d+'/archivelist/year-'+y+','+'month-'+m+',starttime-'+str(cur_id)+'.cms'
			print(url)
			self.get_day_articles(url, cur_date, dir_path)
			time.sleep(3)
			cur_date += datetime.timedelta(days=1)
			cur_id += 1