import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time

def get_formed_articles(all_text, date):
	articles = []
	cur_article = {'date' : date}
	for elem in all_text:
		if elem['type'] == 'title' and 'title' in cur_article.keys():
			articles.append(cur_article)
			cur_article = {'date' : date}

		if elem['type'] == 'title':
			cur_article['title'] = elem['text']

		if elem['type'] == 'author':
			cur_article['author'] = elem['text']

		if elem['type'] == 'location':
			cur_article['location'] = elem['text']

		if elem['type'] == 'content':
			if 'content' not in cur_article.keys():
				cur_article['content'] = ''
			cur_article['content'] += elem['text'] + '\n'
	articles.append(cur_article)
	return articles

def get_articles_trolley(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')

	divs = soup.findAll("div", class_="sqs-block-content")

	meta = soup.find("meta", itemprop="datePublished")
	date = meta['content'].split('T')[0]

	all_text = []
	for div in divs:

		# if title
		title = div.find("h2")
		if not title:
			title = div.find("b")
		if title:
			title = title.text.strip()
			if title != 'Subscribe':
				all_text.append({'type':'title','text':title})
			else:
				break
		
		# if author, location
		strong = div.find("strong")
		if strong:
			strong = strong.text.strip()
			if strong == 'अगले प्रकाशनों के लिए अधिसूचित होने के लिए, कृपया हमारे न्यूज़लेटर की सदस्यता लें':
				break
			parts = strong.split(',')
			author = parts[0]
			if len(parts) == 2:
				location = parts[1]
			else:
				location = '---'

			all_text.append({'type':'author', 'text':author.strip()})
			all_text.append({'type':'location', 'text':location.strip()})

		p_tag = div.findAll("p")
		for p in p_tag:
			text = p.text.strip()
			if 'Newsletter dedicated to farmers protest. Reporting from the protest and for the protest.' in text:
				break
			all_text.append({'type':'content', 'text':text})

	return get_formed_articles(all_text, date)			


def write_articles(articles, dir_path, url):
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)
	for index, article in enumerate(articles):
		file = open(dir_path + '/' + str(index+1) +'.txt', 'w')
		print(article['title'])
		if 'location' not in article.keys():
			article['location'] = '---'
		if 'author' not in article.keys():
			article['author'] = '---'
		try:
			to_write = '||'.join([article['date'],article['location'],article['title'],article['content'],url,article['author']])
		except:
			print(article)
		file.write(to_write)
		file.close()


dir_path = '../../corpus/trolleytimes/hindi/5'
url = 'https://www.trolleytimes.online/edition/hindi/5'
articles = get_articles_trolley(url)
write_articles(articles, dir_path, url)
