from .upload_functions import *

def get_location(part):
	if '--' in part:
		return ''
	if part[-1] == ',':
		return part[:-1]
	return part 


toi_item_set_dict = {'12-2020' : 1631996,
'11-2020' : 1631979,
'10-2020' : 1631960,
'09-2020' : 1631948,
'08-2020' : 1631907,
'07-2020' : 1631888,
'06-2020' : 1631848,
'05-2020' : 1631815,
'04-2020' : 1631794,
'01-2021' : 1740012,
'02-2021' : 1740108,
'03-2021' : 1740147,
'04-2021' : 1740178,
'05-2021' : 1740224
}

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

toi_item_set_id = 1631756
def upload_date(date_string, filepath, month):
	upload_file(filepath, date_string, toi_item_set_dict[month], toi_item_set_id,'The Times of India', '', keywords, get_location)
