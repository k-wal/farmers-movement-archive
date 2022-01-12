from .upload_functions import UploadFunctions


class TOIUploader(UploadFunctions):

	def __init__(self):
		super(TOIUploader, self).__init__()
		self.toi_item_set_id = 1631756
		self.toi_item_set_dict = {'12-2020' : 1631996,
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
		'05-2021' : 1740224,
		'06-2021' : 3439883,
		'07-2021' : 3440033,
		'08-2021' : 3440034,
		'09-2021' : 3441772,
		'10-2021' : 3442651,
		'11-2021' : 3443157
		}
		self.keywords = [
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

	def get_location(self, part):
		if '--' in part:
			return ''
		if part[-1] == ',':
			return part[:-1]
		return part 


	def upload_date(self, date_string, filepath, month):
		self.upload_file(filepath, date_string, self.toi_item_set_dict[month], self.toi_item_set_id,
			'The Times of India', '', self.keywords, self.get_location)
