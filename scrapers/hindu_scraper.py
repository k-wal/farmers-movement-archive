import requests
from bs4 import BeautifulSoup 
import os


indian_states = ["andhra pradesh","arunachal pradesh ","assam","bihar",
"chhattisgarh","goa","gujarat","haryana","himachal pradesh","jammu and kashmir",
"jharkhand","karnataka","kerala","madhya pradesh","maharashtra","manipur",
"meghalaya","mizoram","nagaland","odisha","punjab","rajasthan","sikkim",
"tamil nadu","telangana","tripura","uttar pradesh","uttarakhand","west bengal",
"andaman and nicobar islands","chandigarh","dadra and nagar haveli","daman and diu",
"lakshadweep","national capital territory of delhi","puducherry"]


# return text and date of news articles of the article with url
def get_text_hindu(url):
	try:
		r = requests.get(url)
	except:
		return '',''
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

	if article_section.lower() in indian_states:
		region = article_section
	else:
		region = ''

	return title,final, date, city, region


# write all articles of a day
def write_day_articles(articles,filename):
	overall_date = ''
	for article in articles:
		title, text, date, city, region, url = article['title'], article['text'], article['date'], article['city'], article['region'], article['url']
	
		if date!='' and overall_date=='':
			overall_date = date
		elif date=='' and overall_date!='':
			date = overall_date

		file = open('../corpus/hindu_with_urls/'+filename+'.txt', 'a')
		to_write = date.strip() + '||' + city + ',' + region + '||' + title + '||' + text.strip() + '||' + url + '\n'
		file.write(to_write)
		file.close()


# given a url of all articles of a day, return all articles of that day
def get_day_articles(url):
	url_date = url.split('/')[5:8]
	url_date.reverse()
	filename = '-'.join(url_date)
	print('\n'+filename + '-------------------\n\n')

	total = 0
	all_articles = []
	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html5lib')
	archive_lists = soup.findAll('ul','archive-list')
	for al in archive_lists:
		hrefs = al.findAll('a')
		for href in hrefs:
			total += 1
			link = href['href']
			title, text, date, city, region = get_text_hindu(link)
			print(total,title)
			if title=='' and date=='':
				continue
			all_articles.append({'title':title, 'text':text, 'date':date, 'city':city, 'region':region, 'url':link})
	print(total)
	write_day_articles(all_articles,filename)



def get_month_articles(start, end, url)
	date = start
	while date <= end:
		d = str(date)
		if len(d) == 1:
			d = '0' + d
		print(url + d)
		get_day_articles(url + d)
		date += 1


date_arr = [['1','30','04'],
['1','31','05'],
['1','30','06'],
['1','31','07'],
['1','31','08'],
['1','30','09'],
['1','31','10'],
['1','30','11'],
['1','31','12']]

for date_element in date_arr:
	star, end, month = date_element[0], date_element[1], date_element[2]
	url = 'https://www.thehindu.com/archive/print/2020/' + month + '/'
	get_month_articles(start, end, url)
