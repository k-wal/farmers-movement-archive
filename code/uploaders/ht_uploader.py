import shutil
import os
import datetime
from .upload_functions import UploadFunctions


class HTUploader(UploadFunctions):

	def __init__(self):
		super(HTUploader, self).__init__()
		self.keywords = ['kisan sabha',
		'bku',
		'tikri',
		'singhu', 
		'anti-farmer',
		'agri-reform',
		'agriculture bills',
		'farm bill',
		'farm bills',
		'farmers bills',
		'farmers\' bills',
		'farmers\' protest',
		'farm policy',
		'farm policies',
		'farm laws',
		'pro-farmer',
		'Essential Commodities (Amendment) Bill, 2020',
		'Essential Commodities Bill, 2020',
		'Essential Commodities Act, 2020',
		'SpeakUpForFarmers',
		'agri bill',
		'agri ordinance',
		'farm ordinance',
		'trolley times',
		'Kisan Sangharsh Committee',
		'Kisan Bachao Morcha',
		'Kisan Mazdoor Sangharsh Committee',
		'Jai Kisan Andolan',
		'Punjab Kisan Union',
		'Kirti Kisan Union',
		'Terai Kisan Sangathan',
		'All India Kisan Sabha',
		'Mahila Kisan Adhikar Manch',
		'Doaba Kisan Samiti',
		'Rakesh Tikait',
		'Bhartiya Kisan Union']
			
		self.ht_item_set_dict = {
		'04-2020' : 1889150,
		'05-2020' : 1889207,
		'06-2020' : 1889271,
		'07-2020' : 1889314,
		'08-2020' : 1889425,
		'09-2020' : 1889550,
		'10-2020' : 1889567,
		'11-2020' : 1889594,
		'12-2020' : 1889611,
		'01-2021' : 1886138,
		'02-2021' : 1886176,
		'03-2021' : 1886219,
		'04-2021' : 1886239,
		'05-2021' : 1886257,
		'06-2021' : 3440789,
		'07-2021' : 3440790,
		'08-2021' : 3440791,
		'09-2021' : 3441384,
		'10-2021' : 3442230
		}
		self.ht_item_set_id = 1886095

	def get_location(self,part):
		if '--' in part:
			return ''
		if ' ' in part and part!='New Delhi':
			return ''
		return part 

	def upload_date(self, date, dir_path):
		month = datetime.datetime.strftime(date, "%m-%Y")
		date_string = datetime.datetime.strftime(date, "%d-%m-%Y")
		filepath = dir_path + '/' + month + '/combined/' + date_string + ".txt"
		self.upload_file(filepath, date_string, self.ht_item_set_dict[month], self.ht_item_set_id,'Hindustan Times', '', self.keywords, self.get_location)

	def upload_interval(self, start_string, end_string, dir_path):
		start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
		end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
		date = start_date
		while date <= end_date:
			print(date)
			self.upload_date(date, dir_path)
			date += datetime.timedelta(days=1)

# start_string = "01-10-2020"
# end_string = "31-12-2020"
# dir_path = '../../corpus/hindustantimes'
# upload_interval(start_string, end_string, dir_path)