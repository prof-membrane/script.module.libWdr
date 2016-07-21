# -*- coding: utf-8 -*-
import xbmc
import json
import _utils
import re
#import dateutil.parser

base = 'http://www1.wdr.de'

def parseShows(letter):
	response = _utils.getUrl('http://www1.wdr.de/mediathek/video/sendungen-a-z/sendungen-'+letter.lower()+'-102.html')
	uls = re.compile('<ul  class="list">(.+?)</ul>', re.DOTALL).findall(response)
	list = []
	for ul in uls:
		lis = re.compile('<li >(.+?)</li>', re.DOTALL).findall(ul)
		for li in lis:
			dict = {}
			strong = re.compile('<strong>(.+?)</strong>', re.DOTALL).findall(li)[0]
			if strong == 'mehr':
				dict['url'] = base + re.compile('href="(.+?)"', re.DOTALL).findall(li)[0]
				dict['name'] = re.compile('<span>(.+?)</span>', re.DOTALL).findall(li)[0]
				dict['thumb'] = base + re.compile('<img.+?src="(.+?)"', re.DOTALL).findall(li)[0]
				
				dict['type'] = 'dir'
				dict['mode'] = 'libWdrListVideos'
				
				list.append(dict)
			else:#TODO!
				pass
		
	return list
	
def parseVideos(url):#TODO remove "mehr"
	response = _utils.getUrl(url)
	#<div class="box"
	typeA = re.compile('<div class="box".+?<a(.+?)>(.+?)</a>.+?<a(.+?)>(.+?)</a>', re.DOTALL).findall(response)
	list = []
	for href,show,href2,stuff in typeA:
		#xbmc.log(href)
		#xbmc.log(href2)
		if '<div class="media mediaA video">' in stuff:
			dict = {}
			#xbmc.log(stuff)
			dict['url'] = base + re.compile('href="(.+?)"', re.DOTALL).findall(href2)[0]
			if '<h4' in stuff:
				dict['name'] = re.compile('<h4.+?>.+?<span class="hidden">Video:</span>(.+?)<', re.DOTALL).findall(stuff)[0].strip()
				#xbmc.log(dict['name'])
			else:
				dict['name'] = show.strip()
			if '<img' in stuff:
				dict['thumb'] = base + re.compile('<img.+?src="(.+?)"', re.DOTALL).findall(stuff)[0]
			dict['plot'] = re.compile('<p class="teasertext">(.+?)<', re.DOTALL).findall(stuff)[0]
			#TODO duration, ut
			dict['type'] = 'video'
			dict['mode'] = 'libWdrPlay'
			
			list.append(dict)
	return list
"""	
def parseDate(date,channel='BR'):
	j = _parseMain()
	xbmc.log(str(j))
	url = j["_links"]["epg"]["href"]
	response = _utils.getUrl(url)
	j = json.loads(response)
	url = j["epgDays"]["_links"][date]["href"]#date: 2016-12-30
	response = _utils.getUrl(url)
	j = json.loads(response)
	
	list = []
	broadcasts = j["channels"][chan[channel]]["broadcasts"]
	for b in broadcasts:
		xbmc.log(str(b))
		if "_links" in b and "video" in b["_links"]:
			dict = {}
			
			dict["name"] = b["headline"]
			dict["plot"] = b["subTitle"]
			dict["subtitle"] = b["hasSubtitle"]
			dict["url"] = b["_links"]["video"]["href"]
			dict["time"] = startTimeToInt(b["broadcastStartDate"][11:19])
			#TODO: rest of properties
			dict['type'] = 'video'
			dict['mode'] = 'libBrPlay'
			list.append(dict)
	return list
"""		
	

def parseVideo(url):
	#xbmc.log(url)
	response = _utils.getUrl(url)
	#'mediaObj': { 'url': 'http://deviceids-medp.wdr.de/ondemand/111/1114678.js'
	#xbmc.log(response)
	url2 = re.compile("'mediaObj': { 'url': '(.+?)'", re.DOTALL).findall(response)[0]
	response = _utils.getUrl(url2)
	videos = re.compile('"videoURL":"(.+?)"', re.DOTALL).findall(response)
	for video in videos:
		if 'm3u8' in video:
			vid = video
	return vid#todo subtitles
def startTimeToInt(s):
	HH,MM,SS = s.split(":")
	return int(HH) * 60 + int(MM)