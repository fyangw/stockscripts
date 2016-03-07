#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
calculate delta volume of SHT (Shanghai Hongkong Tong)
'''

import urllib2
import demjson
import sys
from datetime import *

def getPage(url):
	socket = urllib2.urlopen(url)
	text = socket.read()
	socket.close()
	return text
	
def main():

	# need a YYYY-mm-dd style date
	if len(sys.argv) <= 1 or len(sys.argv[1]) != 10:
		print 'Please give me a date'
	else:
		fromDateStr = sys.argv[1]
		fromDate = datetime.strptime(fromDateStr, '%Y-%m-%d')
		day = (datetime.now() - fromDate).days
		if day <= 0:
			print 'I need a past date for from-date, not future'
		else:
			(data, shtDeltaId, shtDeltaSum) = calcShtDelta(fromDateStr, day)
			
			for x in data:
				print '{0}: {1}'.format(x[0], x[shtDeltaId])
			print 'The summary of SHT from {0} is {1}'.format(fromDateStr, shtDeltaSum);
			
def calcShtDelta(fromDateStr, day):
	url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHT&sty=SHTHPS&st=2&sr=-1&p=1&ps=" + str(day) + "&js={pages:(pc),data:[(x)]}&mkt=1&rt=48577769"
	#print url
	text = getPage(url)

	js = demjson.decode(text)

	#prepare
	data = filter(lambda x: x[0] >= fromDateStr, 
		map(lambda x: x.split(','), js['data']))
	
	#calc the deltas of sht
	date = map (lambda x: x.append(130 - float(x[5])/100), data)
	shtDeltaId = len(data[0]) - 1
	
	#calc the sum of sht
	shtDeltaSum = reduce(lambda x, y : x + y, map (lambda x: x[shtDeltaId], data))
	
	return (data, shtDeltaId, shtDeltaSum)

if __name__ == '__main__':
	main()
