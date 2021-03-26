from upload_functions import *

def get_location(part):
	if '--' in part:
		return ''
	if ' ' in part and part!='New Delhi':
		return ''
	return part 


item_set_dict = {'nation' : 330,
'delhi' : 326,
'punjab' : 324,
'haryana' : 325,
'editorial' : 328,
'chandigarh': 333,
'bathinda': 332,
'amritsar' : 331,
'jalandhar' : 334,
'feature' : 329}

keywords = ['farmer',
'mandi',
'agrarian crisis',
'kisan sabha',
'msp',
'bku',
'tikri', 
'singhu', 
'ghazipur',
'farm bill',
'farm bills',
'the essential commodities',
'trolley times',
'Kisan Sangharsh Committee',
'Kisan Bachao Morcha',
'Kisan Mazdoor Sangharsh Committee',
'Jai Kisan Andolan',
'Punjab Kisan Union',
'Kirti Kisan Union',
'Terai Kisan Sangatha',
'All India Kisan Sabha',
'Mahila Kisan Adhikar Manch',
'Doaba Kisan Samiti',
'Rakesh Tikait',
'Bhartiya Kisan Union']


upload_section('../../corpus/tribune/bathinda', item_set_dict['bathinda'], 'The Tribune', '', keywords, get_location)
