# -*- coding: utf-8 -*-
import xbmc
import json
import _utils
import re
#import dateutil.parser

base = 'http://www1.wdr.de'

#channels:
#10 - wdr fernsehen
#34 - one
def getDate(d):
	l = parseEpg(d)

	return l
	
def parseEpg(url,channels=[10]):
	list = []
	#url = 'http://www.wdr.de/programmvorschau/ajax/alle/uebersicht/2016-09-18/'
	response = _utils.getUrl(url)
	j = json.loads(response)
	for sender in j['sender']:
		if sender['senderId'] in channels:
			for sendung in sender['sendungen']:
				dict = {}	
				dict['channel'] = sender['senderName']
				dict['start'] = str(sendung['start'])[:-3]
				dict['end'] = str(sendung['ende'])[:-3]
				dict['duration'] = str(sendung['ende'] - sendung['start'])[:-3]
				dict['name'] = sendung['hauptTitel']
				if sendung['mediathek']:
					dict['url'] = sendung['mediathekUrl']
					xbmc.log(str(dict))
				#dict['plot'] = #unterTitel
				#dict[''] =
				list.append(dict)
	return list