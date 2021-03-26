from upload_functions import *

def get_location(part):
	if '--' in part:
		return ''
	if part[-1] == ',':
		return part[:-1]
	return part 


item_set_dict = {'hindu' : 330}

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


upload_section('../../corpus/hindu', item_set_dict['hindu'], 'The Hindu', '', keywords, get_location)
