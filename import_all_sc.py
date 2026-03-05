import json
import csv
import requests
import os

# Currency converter
class RealTimeCurrencyConverter():
	def __init__(self,url):
		self.data= requests.get(url).json()
		self.currencies = self.data['rates']
	def convert(self, from_currency, to_currency, amount):
		initial_amount = amount 
		if from_currency != 'USD' : 
			amount = amount / self.currencies[from_currency] 
		amount = round(amount * self.currencies[to_currency], 4) 
		return amount

url = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(url)

"""
# Initial output files
with open('sc_total.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['Total','0','','0.0'])
with open('sc_daily.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
with open('sc_user.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
"""

# Input
"""
print('Input stream date: ')
date = input()
"""
"""
f = open('download.txt', 'r')
for date_nl in f.readlines():
	date = date_nl.rstrip('\n')
"""
list_file = os.listdir('.')
for file in list_file:
	filename = file.rstrip('\n').split('.')
	if(len(filename) < 2 or filename[1] != 'json'):
		continue
	date = filename[0].split('[')[0].split('_')[0]
	print(file.rstrip('\n'))

	# Read past total sc
	dict_total = {}		#{currency : [number, amount, converted_amount]}
	with open('sc_total.csv', newline='') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
			if(row[0] == 'Total'):
				dict_total[row[0]] = [int(row[1]), '', float(row[3])]
			elif(row[0] != ''):
				dict_total[row[0]] = [int(row[1]), float(row[2]), float(row[3])]

	dict_user = {}		#{user_channel_id: [user_id, converted_amount, number]}
	with open('sc_user.csv', newline='', encoding='utf-8') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
			dict_user[row[0]] = [row[1],float(row[2]),int(row[3])];

	# Read today sc
	with open(file.rstrip('\n'), encoding='utf-8') as f:
    		data = json.load(f)
	float_today = 0
	int_today = 0

	for items in data:
		if(items['message_type'] != 'membership_item'):
			#print(items['money'])
			int_today += 1
			converted_amount = converter.convert(items['money']['currency'], 'TWD', items['money']['amount'])
			float_today += converted_amount
			list_onesc = [1, items['money']['amount'], converted_amount]
			#print(list_onesc)
			if(items['money']['currency'] in dict_total):
				#print('key exist')
				dict_total[items['money']['currency']][0] += 1
				dict_total[items['money']['currency']][1] += items['money']['amount']
				dict_total[items['money']['currency']][2] += converted_amount
			else:
				#print('key not exist')
				dict_total[items['money']['currency']] = list_onesc	
			#print(items['author'])
			if(items['author']['id'] in dict_user):
				if('name' in items['author']):
					dict_user[items['author']['id']][0] = items['author']['name']
				else:
					dict_user[items['author']['id']][0] = ''
				dict_user[items['author']['id']][1] += converted_amount
				dict_user[items['author']['id']][2] += 1
			else:
				if('name' in items['author']):
					dict_user[items['author']['id']] = [items['author']['name'], converted_amount, 1]
				else:
					dict_user[items['author']['id']] = ['', converted_amount, 1]

	# Write output files
	with open('sc_total.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		for key in dict_total:
			if(key != 'Total'):
				writer.writerow([key, dict_total[key][0], dict_total[key][1], dict_total[key][2]])
		writer.writerow(['','','',''])
		writer.writerow(['Total',dict_total['Total'][0]+int_today,'',dict_total['Total'][2]+float_today])

	with open('sc_daily.csv', 'a', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([date, float_today])

	with open('sc_user.csv', 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile)
		for key in dict_user:
			#print(key
			writer.writerow([key, dict_user[key][0], dict_user[key][1], dict_user[key][2]])












































