# -*- coding: utf-8 -*-
import xbmc
import json
import _utils
import re
#import dateutil.parser

base = 'http://www1.wdr.de'


def parse(url):
	response = _utils.getUrl(url)
	s = response.split('<h2 class="headline">Suchergebnis</h2>')[-1]
	#xbmc.log(response)
	videos = s.split('<div class="media mediaA">')[1:]
	list = []
	for video in videos:
		dict = {}
		#xbmc.log(video)
		dict['name'] = re.compile('<h3 class="headline">.+?>(.+?)<', re.DOTALL).findall(video)[0]
		dict['plot'] = re.compile('<p class="teasertext">.+?>(.+?)<', re.DOTALL).findall(video)[0]
		#dict['date'] = re.compile('<p class="dachzeile">.+?>(.+?)<', re.DOTALL).findall(video)[0].replace('<strong>Video</strong>','')
		dict['thumb'] = re.compile('<img.+?src="(.+?)"', re.DOTALL).findall(video)[0]
		dict['url'] = re.compile('<a href="(.+?)"', re.DOTALL).findall(video)[0]
		
		dict['type'] = 'video'
		dict['mode'] = 'libWdrPlay'
		#xbmc.log(str(dict))
		list.append(dict)
		
	pages = re.compile('<div class="entry" data-ctrl-load_avsuche100-source=".+?<a href="(.+?)">(.+?)</a>', re.DOTALL).findall(response)
	xbmc.log(str(pages))
	nextPage = str(int(url.split('pageNumber=')[-1].split('&')[0]) + 1)
	for url,page in pages:
		if page == nextPage:
			list.append({'type':'nextPage','url':base+url,'mode':'libWdrListSearch'})
		
	return list