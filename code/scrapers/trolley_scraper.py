import requests
from bs4 import BeautifulSoup 
import os
import datetime
import time

def get_text_trolley(url):
	r = requests.get(url)

	soup = BeautifulSoup(r.content, 'html5lib')

	h1 = soup.find("h1", class_= "entry-title entry-title--large p-name")
	title = h1.text

	h4 = soup.find("h4", style = "text-align:center;white-space:pre-wrap;")
	try:
		author = h4.text
	except:
		print(url)
		author = '---'

	meta = soup.find("meta", itemprop="datePublished")
	print(meta)
	date = meta['content'].split('T')[0]

	divs = soup.findAll('div', class_="sqs-block html-block sqs-block-html")
	divs = divs[:-1]

	content = ''
	for div in divs:
		blocks = div.findAll('p', style="white-space:pre-wrap;")
		for block in blocks:
			content += block.text
			content += '\n'
	content = content.strip()
	return title, date, author, content


def write_article(dir_path, edition_number, filename, title, date, author, content, url):
	to_write = '||'.join([date, title, content, url, author])
	file = open(dir_path + '/' + filename + '.txt', 'w')
	file.write(to_write)
	file.close()


def get_edition_trolley(url, edition_number, dir_path):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html5lib')

	divs = soup.findAll("div", class_="summary-title")

	for div in divs:
		a_tag = div.find("a")
		link = a_tag['href']
		filename = link.split('/')[-1]
		full_link = 'https://www.trolleytimes.online' + link
		title, date, author, content = get_text_trolley(full_link)
		write_article(dir_path, edition_number, filename, title, date, author, content, full_link)



edition_number = 14
dir_path = '../../corpus/trolleytimes/' + str(edition_number)
url = 'https://www.trolleytimes.online/edition/punjabi/edition-' + str(edition_number)

get_edition_trolley(url, edition_number, dir_path)

