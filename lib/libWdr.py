# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import libWdrParser
import libWdrRssParser
import libMediathek

translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString





def getDate(date):
	return libWdrJsonParser.parseDate(date)
def getVideoUrl(url):
	return libWdrJsonParser.parseVideo(url)
def play(dict):
	url = getVideoUrl(dict["url"])
	#listitem = xbmcgui.ListItem(label=video["name"],thumbnailImage=video["thumb"],path=url)
	listitem = xbmcgui.ListItem(label=dict["name"],path=url)
	xbmc.Player().play(url, listitem)	
	

def libWdrListMain():
	libMediathek.addEntry({'name':'Neue Videos', 'mode':'libWdrListFeed', 'url':'http://www1.wdr.de/mediathek/video/sendungverpasst/sendung-verpasst-100~_format-mp111_type-rss.feed'})
	libMediathek.addEntry({'name':translation(31032), 'mode':'libWdrListLetters'})
	libMediathek.addEntry({'name':translation(31033), 'mode':'libWdrListDate'})
	#libMediathek.addEntry({'name':'Videos in Gebärdensprache', 'mode':'libWdrListFeed', 'url':'http://www1.wdr.de/mediathek/video/sendungen/videos-dgs-100~_format-mp111_type-rss.feed'})
	#libMediathek.addEntry({'name':'Videos mit Untertiteln', 'mode':'libWdrListFeed', 'url':'http://www1.wdr.de/mediathek/video/sendungen/videos-untertitel-100~_format-mp111_type-rss.feed'})
	libMediathek.addEntry({'name':translation(31039), 'mode':'libWdrSearch'})
	
	
	
	
	
def libWdrListLetters():
	libMediathek.populateDirAZ('libWdrListShows',ignore=['#'])
	
def libWdrListShows():
	xbmc.log('listshows')
	libMediathek.addEntries(libWdrParser.parseShows(params['name']))
	
def libWdrListVideos():
	libMediathek.addEntries(libWdrRssParser.parseVideos(params['url']))
	
def libWdrListFeed():
	libMediathek.addEntries(libWdrRssParser.parseFeed(params['url']))

def libWdrListDate():
	libMediathek.populateDirDate('libWdrListDateVideos')
	
def libWdrListDateVideos():
	from datetime import date, timedelta
	day = date.today() - timedelta(int(params['datum']))
	ddmmyyyy = day.strftime('%d%m%Y')
	yyyymmdd = day.strftime('%Y-%m-%d')
	url = 'http://www1.wdr.de/mediathek/video/sendungverpasst/sendung-verpasst-100~_tag-'+ddmmyyyy+'_format-mp111_type-rss.feed'
	urlEpg = 'http://www.wdr.de/programmvorschau/ajax/alle/uebersicht/'+yyyymmdd+'/'
	xbmc.log(url)
	xbmc.log(urlEpg)
	import libWdrJsonParser
	import time
	#listEpg = libWdrJsonParser.parseEpg(urlEpg)
	listVideos = libWdrRssParser.parseFeed(url,'date')
	libMediathek.addEntries(listVideos)
	"""
	listFinal = []
	epochmax = int(time.mktime(time.strptime(ddmmyyyy, "%d%m%Y"))) + 86400
	xbmc.log(str(epochmax))
	for item in listEpg:
		if 'url' in item and int(item['start']) <= epochmax:
		
			xbmc.log('###########')
			xbmc.log(item['url'])
			xbmc.log(str(item['start']))
			xbmc.log(str(epochmax))
			xbmc.log('###')
			
			for vid in listVideos:
				xbmc.log(vid['url'])
				if item['url'] == vid['url']:
					dict = vid
					dict['duration'] = item['duration']
					listFinal.append(dict)
					break
			else:
				dict = {}
				xbmc.log(time.strftime('%H:%M', time.localtime(int(item['start']))))
				dict['name'] = item['name']
				dict['url'] = item['url']
				dict['duration'] = item['duration']
				dict['aired'] = yyyymmdd
				dict['airedtime'] = time.strftime('%H:%M', time.localtime(int(item['start'])))
				dict['type'] = 'date'
				dict['mode'] = 'libWdrPlay'
				listFinal.append(dict)
				
	#from operator import itemgetter
	#l = sorted(l, key=itemgetter('sort')) 
	libMediathek.addEntries(listFinal)
	"""
def libWdrSearch():
	import libWdrHtmlParser
	keyboard = xbmc.Keyboard('', translation(31039))
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText():
		search_string =  urllib.quote_plus(keyboard.getText())
		libMediathek.addEntries(libWdrHtmlParser.parse("http://www1.wdr.de/mediathek/video/suche/avsuche100~suche_parentId-videosuche100.html?pageNumber=1&sort=date&q="+search_string))
def libWdrListSearch():
	import libWdrHtmlParser
	libMediathek.addEntries(libWdrHtmlParser.parse(params['url']))
def libWdrPlay():
	url,subUrl = libWdrParser.parseVideo(params['url'])
	xbmc.log(url)
	listitem = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	
	
def list():	
	modes = {
	'libWdrListLetters': libWdrListLetters,
	'libWdrListShows': libWdrListShows,
	'libWdrListVideos': libWdrListVideos,
	'libWdrListFeed': libWdrListFeed,
	'libWdrListDate': libWdrListDate,
	'libWdrListDateVideos': libWdrListDateVideos,
	'libWdrSearch': libWdrSearch,
	'libWdrListSearch': libWdrListSearch,
	'libWdrPlay': libWdrPlay
	}
	global params
	params = libMediathek.get_params()
	global pluginhandle
	pluginhandle = int(sys.argv[1])
	xbmc.log('mode')
	xbmc.log(params.get('mode',''))
	if not params.has_key('mode'):
		libWdrListMain()
	else:
		modes.get(params['mode'],libWdrListMain)()
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	