# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import libWdrParser
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
	libMediathek.addEntry({'name':translation(31032), 'mode':'libWdrListLetters'})
	#libMediathek.addEntry({'name':translation(31033), 'mode':'libWdrListDate'})
	#libMediathek.addEntry({'name':translation(31034), 'mode':'libArdListVideos', 'url':'http://www.ardmediathek.de/appdata/servlet/tv/Rubriken/mehr?documentId=21282550&json'})
	
	
	
def libWdrListLetters():
	libMediathek.populateDirAZ('libWdrListShows',ignore=['#'])
	
def libWdrListShows():
	xbmc.log('listshows')
	libMediathek.addEntries(libWdrParser.parseShows(params['name']))
	
def libWdrListVideos():
	libMediathek.addEntries(libWdrParser.parseVideos(params['url']))

def libWdrListDate():
	libMediathek.populateDirDate('libWdrListDateChannels')
	
def libWdrListDateChannels():
	libMediathek.addEntry({'name':'ARD-Alpha', 'mode':'libWdrListLetters', 'date': params['date']})
	libMediathek.addEntry({'name':'BR', 'mode':'libWdrListLetters', 'date': params['date']})

def libWdrListDateVideos():
	libMediathek.addEntries(libWdrJsonParser.parseDate(params['date'],params['name']))#params['date'] =yyyy-mm-dd
	
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
	#'libWdrListDate': libWdrListDate,
	#'libWdrListDateChannels': libWdrListDateChannels,
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