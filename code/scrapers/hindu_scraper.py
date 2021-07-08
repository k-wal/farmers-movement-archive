import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time

class HinduScraper:

	def __init__(self):
		self.indian_states = ["andhra pradesh","arunachal pradesh ","assam","bihar",
		"chhattisgarh","goa","gujarat","haryana","himachal pradesh","jammu and kashmir",
		"jharkhand","karnataka","kerala","madhya pradesh","maharashtra","manipur",
		"meghalaya","mizoram","nagaland","odisha","punjab","rajasthan","sikkim",
		"tamil nadu","telangana","tripura","uttar pradesh","uttarakhand","west bengal",
		"andaman and nicobar islands","chandigarh","dadra and nagar haveli","daman and diu",
		"lakshadweep","national capital territory of delhi","puducherry"]

	# return text and date of news articles of the article with url
	def get_text(self, url):
		try:
			r = requests.get(url)
		except:
			return '', '', '', '', ''
		soup = BeautifulSoup(r.content, 'html5lib')
		

		divs = soup.findAll('div')
		
		try:
			none = soup.findAll('none')[1]
			t = none.text.replace('\n','')
			parts = t.split(',') 
			date = parts[0].split()[1] + ' ' + parts[0].split()[0] + ' ' + parts[1].split()[0]
		except:
			return '', '', '', '', ''

		final = ""
		for div in divs:
			if not div.has_attr('id'):
				continue
			if 'content-body' not in div['id']:
				continue
			ps = div.findAll('p')
			for p in ps:
				final += p.text + ' '
			break
		divs = soup.findAll('div',class_ = 'also-view-text-cont')
		for div in divs:
			ps = div.findAll('p')
			for p in ps:
				text = p.text
				final = final.replace(text,'')

		final = final.replace('\n', ' ')

		article_exclusive = soup.findAll('div',class_ = 'article-exclusive')
		
		article_section = soup.find('meta',property = 'article:section')['content'].strip()

		city = soup.find('span', class_= 'blue-color ksl-time-stamp').text.strip()
		city = city.replace(',','')

		title = soup.find('div',class_='artcl-nm-stky-text').text.strip()

		if article_section.lower() in self.indian_states:
			region = article_section
		else:
			region = ''

		return title,final, date, city, region

	# write all articles of a day
	def write_day_articles(self, articles, filename, dir_path):
		if not os.path.isdir(dir_path):
			os.mkdir(dir_path)
		overall_date = ''
		for article in articles:
			title, text, date, city, region, url = article['title'], article['text'], article['date'], article['city'], article['region'], article['url']
		
			if date!='' and overall_date=='':
				overall_date = date
			elif date=='' and overall_date!='':
				date = overall_date

			file = open(dir_path+'/'+filename+'.txt', 'a')
			to_write = date.strip() + '||' + city + ',' + region + '||' + title + '||' + text.strip() + '||' + url + '\n'
			file.write(to_write)
			file.close()

	# given a url of all articles of a day, return all articles of that day
	def get_day_articles(self, url, dir_path):
		url_date = url.split('/')[5:8]
		url_date.reverse()
		filename = '-'.join(url_date)
		print('\n'+filename + '-------------------\n\n')

		total = 0
		all_articles = []
		r = requests.get(url)
		soup = BeautifulSoup(r.content,'html5lib')
		archive_lists = soup.findAll('ul','archive-list')
		# print(soup)
		for al in archive_lists:
			hrefs = al.findAll('a')
			for href in hrefs:
				total += 1
				link = href['href']
				title, text, date, city, region = self.get_text(link)
				print(total,title)
				if title=='' and date=='':
					continue
				all_articles.append({'title':title, 'text':text, 'date':date, 'city':city, 'region':region, 'url':link})
		print(total)
		self.write_day_articles(all_articles,filename, dir_path)

	# given start date and end date, write articles of the interval (both inclusive)
	def write_date_range_articles(self, start_date, end_date, dir_path):
		cur_date = start_date
		while cur_date <= end_date:
			date_string = datetime.datetime.strftime(cur_date, "%Y/%m/%d/")
			month_string = datetime.datetime.strftime(cur_date, "%m-%Y")
			url = 'https://www.thehindu.com/archive/print/' + date_string
			print(url)
			self.get_day_articles(url, dir_path + '/' + month_string)
			time.sleep(3)
			cur_date += datetime.timedelta(days=1)