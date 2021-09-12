import requests
from bs4 import BeautifulSoup 
import os
from time import strptime
import datetime


class HTScraper:

	# string of the form "PUBLISHED ON JUN 10, 2021"
	def get_date(self, string):
		if 'UPDATED' in string:
			string = string.replace('UPDATED', 'PUBLISHED')

		string = string.strip()[13:25]
		date = datetime.datetime.strptime(string, "%b %d, %Y")
		return datetime.datetime.strftime(date, "%d-%m-%Y")

	def get_text_ht(self, url):
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

		date = self.get_date(date_string)
		return title, date, coverage, text


	def get_filepath(self, dir_path, date, section):
		section = section.split('-')[0]
		month = date[3:]
		cur_dir_path = dir_path + '/' + month
		if not os.path.exists(cur_dir_path):
			os.makedirs(cur_dir_path)
		cur_dir_path = cur_dir_path + '/' + section.lower()
		if not os.path.exists(cur_dir_path):
			os.makedirs(cur_dir_path)
		return cur_dir_path + '/' + date + '.txt'

	def write_page_articles(self, articles, dir_path, section):
		for article in articles:
			title, coverage, text, date, url = article['title'], article['coverage'], article['text'], article['date'], article['url']
			filepath = self.get_filepath(dir_path, date, section)
			file = open(filepath, 'a')
			to_write = date.strip() + '||' + coverage + '||' + title + '||' + text.strip() + '||' + url + '\n'
			file.write(to_write)
			file.close()

	def get_page_date_range(self, h2s):
		# getting date of latest article on page
		latest_h2 = h2s[0]
		latest_link = 'https://www.hindustantimes.com' + latest_h2.find("a")['href']
		_, latest_date, _, _ = self.get_text_ht(latest_link)
		latest_date = datetime.datetime.strptime(latest_date, "%d-%m-%Y")

		# getting date of earliest article on page
		earliest_h2 = h2s[-1]
		earliest_link = 'https://www.hindustantimes.com' + earliest_h2.find("a")['href']
		_, earliest_date, _, _ = self.get_text_ht(earliest_link)
		earliest_date = datetime.datetime.strptime(earliest_date, "%d-%m-%Y")	

		return earliest_date, latest_date

	# beg_date and end_date are in datetime type
	# return False if not to continue, True if to continue
	def get_page_articles(self, url, from_date, til_date, dir_path, section):
		headers = {'user-agent' : 'Mozilla/5.0',
		'accept': 'application/json, text/plain, */*'
		}
		r = requests.get(url, headers=headers)
		soup = BeautifulSoup(r.content, 'html5lib')
		
		articles = []
		h2s = soup.findAll("h2", class_ = "hdg3")
		
		earliest_date, latest_date = self.get_page_date_range(h2s)

		if latest_date < from_date:
			return False
		if earliest_date > til_date:
			return True

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
			
			title, date, coverage, text = self.get_text_ht(link)

			# check if the current article should be included
			formatted_date = datetime.datetime.strptime(date, "%d-%m-%Y")
			if formatted_date < from_date:
				return False
			if formatted_date > til_date:
				continue

			if title == '':
				continue
			articles.append({'title':title, 'coverage':coverage, 'text':text, 'date':date, 'url':link})
			print(index, date, title)
		self.write_page_articles(articles, dir_path, section)
		return True
		
	def write_date_range_articles(self, beg_string, end_string, section, dir_path):
		sections = ['editorials',
					'analysis',
					'opinion',
					'india-news',
					'cities',
					'world-news'
					]	

		cur = 1
		from_date = datetime.datetime.strptime(beg_string, "%d-%m-%Y")
		til_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
		to_continue = True
		while to_continue:
			url = 'https://www.hindustantimes.com/' + section + '/page-' + str(cur)
			print(url + "\n")
			to_continue = self.get_page_articles(url, from_date, til_date, dir_path, section)
			print("\n\n")
			cur += 1

beg = '08-09-2021'
end = '09-09-2021'
section = 'world-news'
dir_path = '../../corpus/hindustantimes'
scraper = HTScraper()
scraper.write_date_range_articles(beg, end, section, dir_path)