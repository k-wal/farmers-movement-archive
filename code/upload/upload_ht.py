from upload_functions import *
import shutil
import os

def get_location(part):
	if '--' in part:
		return ''
	if ' ' in part and part!='New Delhi':
		return ''
	return part 

keywords = [
'kisan sabha',
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

ht_item_set_dict = {
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
'05-2021' : 1886257
}
ht_item_set_id = 1886095

def upload_date(date, dir_path):
	month = datetime.datetime.strftime(date, "%m-%Y")
	date_string = datetime.datetime.strftime(date, "%d-%m-%Y")
	filepath = dir_path + '/' + month + '/combined/' + date_string + ".txt"
	upload_file(filepath, date_string, ht_item_set_dict[month], ht_item_set_id,'Hindustan Times', '', keywords, get_location)

def upload_interval(start_string, end_string, dir_path):
	start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
	end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
	date = start_date
	while date <= end_date:
		print(date)
		upload_date(date, dir_path)
		date += datetime.timedelta(days=1)

start_string = "01-10-2020"
end_string = "31-12-2020"
dir_path = '../../corpus/hindustantimes'
upload_interval(start_string, end_string, dir_path)