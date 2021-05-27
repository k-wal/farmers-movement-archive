from upload_functions import *

def get_location(part):
	if '--' in part:
		return ''
	if part[-1] == ',':
		return part[:-1]
	return part 


item_set_dict = {'12-2020' : 327,
'11-2020' : 7348,
'10-2020' : 7454,
'09-2020' : 7972,
'08-2020' : 8335,
'07-2020' : 8495,
'06-2020' : 9297,
'05-2020' : 9298,
'04-2020' : 9299,
'01-2021' : 1319417}

keywords = [
# 'farmer',
# 'mandi',
# 'agrarian crisis',
'kisan sabha',
#'msp',
'bku',
'tikri', 
'singhu', 
# 'ghazipur',
'anti-farmer',
'agri-reform',
'farm bill',
'farm bills',
'farmers bills',
'farmers\' bills',
'farm policy',
'farm policies',
'pro-farmer',
'Essential Commodities (Amendment) Bill, 2020',
'Essential Commodities Bill, 2020',
'Essential Commodities Act, 2020',
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

month = '01-2021'

upload_section('../../corpus/hindu/' + month, item_set_dict[month], 'The Hindu', '', keywords, get_location)