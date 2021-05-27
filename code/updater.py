#from scrapers.hindu_scraper import get_day_articles as get_hindu_day_articles
from scrapers.tribune_scraper import write_all_sections as scraper_tribune
from scrapers.hindu_scraper import write_date_range_articles as scraper_hindu
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


filename = 'update_stats'
# update_tribune(filename)
# update_hindu(filename)

start_string = "31-01-2021"
end_string = "31-01-2021"
start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
dir_path = '../corpus/hindu'
scraper_hindu(start_date, end_date, dir_path)