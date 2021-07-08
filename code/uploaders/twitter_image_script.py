import twint
import re
import datetime
import requests
import shutil

def get_next_date(date):
	date = datetime.datetime.strptime(date, "%Y-%m-%d")
	date = date + datetime.timedelta(days=1)
	return date.strftime("%Y-%m-%d")

def get_previous_date(date):
	date = datetime.datetime.strptime(date, "%Y-%m-%d")
	date = date - datetime.timedelta(days=1)
	return date.strftime("%Y-%m-%d")

def get_image_url(url, date, username):
	c = twint.Config()
	c.Search = url
	c.Username = username
	c.Since = date
	c.Until = get_next_date(date)
	c.Store_object = True
	c.Format = "{photos} || {video}"
	c.Limit = 1
	try:
		twint.run.Search(c)
	except:
		return []
	tweets_as_objects = twint.output.tweets_list
	twint.output.tweets_list = [] 
	if len(tweets_as_objects) == 0:
#		print(url, date, username)
		return []
	return tweets_as_objects[0].photos

# return a photo path if successfully downloaded, else return empty string
def store_image(url):
	print(url)
	extension = url.split('.')[-1]
	r = requests.get(url, stream=True)
	if r.status_code != 200:
		print("xxxxxxxxxxx")
		return ''
	r.raw.decode_content = True
	with open('twitter_image.' + extension, 'wb') as f:
		shutil.copyfileobj(r.raw,f)
		print('===== IMAGE DOWNLOAD SUCCESSFUL =======')
		return 'twitter_image.' + extension



# return photo path if there is an image in the tweet, else return empty string
def if_image(text, date, username):
	if 'https://' in text:
		# find the url in text : can be photo/video/another tweet
		urls = re.findall('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', text)
		for url in urls:													# for each url, check if the image exists
			url = url[0]+'://'+url[1]+url[2]								# create the url string
			image_urls = get_image_url(url, date, username)
			if len(image_urls) > 0:
				for image_url in image_urls:
					photo_path = store_image(image_url)
					if photo_path != '':
						return photo_path
	return ''



# text = ' प्रधान मंत्री नरेंद्र मोदी ने आज केंद्र के नए कृषि कानूनों और उनके द्वारा लाए गए फायदों की बात की, क्योंकि देश में पिछले चार दिनों से किसानों द्वारा अभूतपूर्व विरोध प्रदर्शन हो रहे थे।   #preminister #modi #farmer #farmersprotest #farmbill #opportunity  https://t.co/hUTCGs6nRM'
# date = '2020-11-29'
# username = 'VidharbhS'
# print(if_image(text, date, username))
