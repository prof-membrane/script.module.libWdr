# -*- coding: utf-8 -*-
import xbmc
import json
import _utils
import re
#import dateutil.parser

base = 'http://www1.wdr.de'

def parseVideos(url):#TODO remove "mehr"
	if not url.endswith('index.html'):
		l = len(url.split('/')[-1])
		url = url[:-l] + 'index.html'
	xbmc.log(url)
	response = _utils.getUrl(url)
	feed = re.compile('<link rel="alternate".+?href="(.+?)"').findall(response)[0]
	feed = base + feed.replace('.feed','~_format-mp111_type-rss.feed')
	return parseFeed(feed)
	
def parseFeed(feed,type=False):
	xbmc.log(feed)
	response = _utils.getUrl(feed)
	items = re.compile('<item>(.+?)</item>', re.DOTALL).findall(response)
	list = []
	for item in items:
		#xbmc.log(item)
		dict = {}
		dctype = re.compile('<dc:type>(.+?)</dc:type>', re.DOTALL).findall(item)[0]
		if 'Video' in dctype:
			dict['name'] = re.compile('<title>(.+?)</title>', re.DOTALL).findall(item)[0]
			dict['url'] = re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)[0]
			if '<content:encoded>' in item:
				dict['plot'] = re.compile('<content:encoded>(.+?)</content:encoded>', re.DOTALL).findall(item)[0].replace('\n ','\n')
			dict['channel'] = re.compile('<dc:creator>(.+?)</dc:creator>', re.DOTALL).findall(item)[0]
			dict['tvshowtitle'] = re.compile('<mp:topline>(.+?)</mp:topline>', re.DOTALL).findall(item)[0]
			dict['thumb'] = _chooseThumb(re.compile('<mp:image>(.+?)</mp:image>', re.DOTALL).findall(item))
			
			d = re.compile('<dc:date>(.+?)</dc:date>', re.DOTALL).findall(item)[0]#TODO
			s = d.split('T')
			dict['aired'] = s[0]
			t = s[1].replace('Z','').split(':')
			dict['airedtime'] = str(int(t[0])+1) + ':' + t[1]
			dict['sort'] = s[1].replace('Z','').replace(':','')
			if len(dict['airedtime']) == 4:
				dict['airedtime'] = '0' + dict['airedtime']
			if type:
				dict['type'] = type
			else:
				dict['type'] = 'video'
			dict['mode'] = 'libWdrPlay'
			xbmc.log(str(dict))
			list.append(dict)
	return list
	#<div class="box"

def _chooseThumb(thumbs):
	for thumb in thumbs:
		w = re.compile('<mp:width>(.+?)</mp:width>', re.DOTALL).findall(thumb)[0]
		h = re.compile('<mp:height>(.+?)</mp:height>', re.DOTALL).findall(thumb)[0]
		if w == '310' and h == '174':
			return re.compile('<mp:data>(.+?)</mp:data>', re.DOTALL).findall(thumb)[0]