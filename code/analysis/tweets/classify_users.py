import twint
import os
import datetime

# store tweets with hashtag ht in the given interval in filepath
def get_user_bio(username):
	c = twint.Config()
	c.Username = username
	c.Format = '{username}|-|{bio}'
	c.Output = 'results/bios.txt'

	twint.run.Lookup(c)

def get_usernames():
	file = open('results/usernames.txt','r')
	lines = file.readlines()
	file.close()
	return [line.strip() for line in lines]

def write_bios():
	usernames = get_usernames()
	for i,u in enumerate(usernames):
		try:
			print(i)
			get_user_bio(u)
		except:
			continue

write_bios()