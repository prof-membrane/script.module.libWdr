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
	ddmmyy = day.strftime('%d%m%Y')
	xbmc.log(params['datum'])
	xbmc.log(ddmmyy)
	#url = 'http://www1.wdr.de/mediathek/video/sendungverpasst/sendung-verpasst-100~_tag-19092016_format-mp111_type-rss.feed'
	url = 'http://www1.wdr.de/mediathek/video/sendungverpasst/sendung-verpasst-100~_tag-'+ddmmyy+'_format-mp111_type-rss.feed'
	xbmc.log(url)
	l = libWdrRssParser.parseFeed(url,'date')
	from operator import itemgetter
	l = sorted(l, key=itemgetter('sort')) 
	libMediathek.addEntries(l)
	
def libWdrPlay():
	url = libWdrParser.parseVideo(params['url'])
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