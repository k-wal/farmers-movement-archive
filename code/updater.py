#from scrapers.hindu_scraper import get_day_articles as get_hindu_day_articles
from scrapers.tribune_scraper import write_all_sections as scraper_tribune
from scrapers.tribune_scraper import write_one_section as scraper_tribune_section
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


# FOR HINDU
# start_string = "21-04-2021"
# end_string = "30-04-2021"
# start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
# end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
# dir_path = '../corpus/hindu'
# scraper_hindu(start_date, end_date, dir_path)

# FOR TRIBUNE
sections = [['comment','59'],
	['musing','62'],
	['business','19'],
	['punjab','45'],
	['haryana','28'],
	['amritsar','17'],
	['bathinda','18'],
	['delhi','24'],
	['chandigarh','20'],
	['jalandhar','34'],
	['nation','42'],
	['editorial','60'],
	['ludhiana','40'],
	['patiala','213'],
	['himachalpradesh','30'],
	['jammukashmir','36']
	]

section = 'chandigarh'
start_string = "01-01-2021"
end_string = "21-01-2021"
dir_path = '../corpus/tribune/to_upload'
scraper_tribune_section(section, dir_path, start_string, end_string)

# scraper_tribune(dir_path, start_string, end_string)
