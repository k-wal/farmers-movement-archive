from upload_functions import *

def get_location(part):
	if '--' in part:
		return ''
	if part[-1] == ',':
		return part[:-1]
	return part 


item_set_dict = {12 : 327,
11 : 7348,
10 : 7454,
9 : 7972,
8 : 8335,
7 : 8495,
6 : 9297,
5 : 9298,
4 : 9299}

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

month = 5

upload_section('../../corpus/hindu/' + str(month), item_set_dict[month], 'The Hindu', '', keywords, get_location)
