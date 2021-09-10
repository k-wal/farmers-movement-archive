#from scrapers.hindu_scraper import get_day_articles as get_hindu_day_articles
from scrapers.tribune_scraper import write_all_sections as scraper_tribune
from scrapers.tribune_scraper import write_one_section as scraper_tribune_section
# from scrapers.toi_scraper import write_date_range_articles as scraper_toi
# from uploaders.upload_toi import upload_date as upload_date_toi
from uploaders.upload_tribune import upload_move_section as upload_section_tribune

from scrapers.hindu_scraper import HinduScraper
from uploaders.hindu_uploader import HinduUploader

from scrapers.toi_scraper import TOIScraper
from uploaders.toi_uploader import TOIUploader

import pickle
import datetime

def read_update_date(filename):
	infile = open(filename, 'rb')
	date = pickle.load(infile)
	infile.close()
	print(date.strftime("%d-%m-%Y"))
	return date

def write_update_date(date, filename):
	outfile = open(filename, 'wb')
	pickle.dump(date, outfile)
	outfile.close()

def update_tribune(update_filename):
	last_update_date = read_update_date(update_filename)
	date_string = last_update_date.strftime("%d-%m-%Y")
	dir_path = '../corpus/temp/tribune'
	scraper_tribune(dir_path, date_string)

def update_hindu(update_filename):
	last_update_date = read_update_date(update_filename)
	start_date = last_update_date + datetime.timedelta(days=1)
	current_date = datetime.datetime.today()
	dir_path = '../corpus/temp/hindu'
	scraper_hindu(start_date, current_date, dir_path)


def update_hindu_interval(start_string, end_string):
	start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
	end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
	date = start_date
	dir_path = '../corpus/hindu'
	scraper = HinduScraper()
	uploader = HinduUploader()

	# iterate through dates and scrape+upload one by one
	while date <= end_date:
		month_string = date.strftime("%m-%Y")
		date_string =  date.strftime("%Y-%m-%d")
		filepath = dir_path + '/' + month_string + '/' + date.strftime("%d-%m-%Y") + '.txt'
		scraper.write_date_range_articles(date, date, dir_path)
		uploader.upload_date(date_string, filepath, month_string)

		date += datetime.timedelta(days=1)

def update_tribune_interval(start_string, end_string, sections):
	for section in sections:
		dir_path = '../corpus/tribune/to_upload'
		scraper_tribune_section(section, dir_path, start_string, end_string)
		upload_section_tribune(section, '../corpus/tribune/to_upload')

def update_toi_interval(start_string, end_string):
	start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
	end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
	date = start_date
	dir_path = '../corpus/timesofindia'
	scraper = TOIScraper()
	uploader = TOIUploader()

	# iterate through dates to scrape, upload one by one
	while date <= end_date:
		month_string = date.strftime("%m-%Y")
		date_string =  date.strftime("%Y-%m-%d")
		filepath = dir_path + '/' + month_string + '/' + date.strftime("%d-%m-%Y") + '.txt'
		# scraper_toi(date, date, dir_path)
		# upload_date_toi(date_string, filepath, month_string)
		scraper.write_date_range_articles(date, date, dir_path)
		uploader.upload_date(date_string, filepath, month_string)

		date += datetime.timedelta(days=1)

filename = 'update_stats'

# FOR Times of India
# start_string = "26-07-2021"
# end_string = "31-07-2021"
# update_toi_interval(start_string, end_string)


# FOR HINDU
# start_string = "23-08-2021"
# end_string = "31-08-2021"
# update_hindu_interval(start_string, end_string)


# FOR TRIBUNE
# sections = ['comment',
# 			'musing',
# 			'business',
# 			'haryana',
# 			'punjab',
# 			'amritsar',
# 			'bathinda',
# 			'delhi',
# 			'chandigarh',
# 			'jalandhar',
# 			'nation',
# 			'editorial',
# 			'ludhiana',
# 			'patiala',
# 			'himachalpradesh',
# 			'jammukashmir']

# start_string = "01-08-2021"
# end_string = "31-08-2021"

# temp_sections = ['musing']
# update_tribune_interval(start_string, end_string, temp_sections)
