import urllib
import urllib2
import datetime
import shutil
import re
import os
import base64
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import cookielib
import plugintools
import urlparse
import httplib
import time
from addon.common.net import Net
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
try:
    import json
except:
    import simplejson as json
import SimpleDownloader as downloader
import time
import requests
from lib.utils import *
import xml.etree.ElementTree as ET
import random



net = Net(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
headers = {
    'Accept'    :   'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
	
resolve_url=['180upload.com', 'allmyvideos.net', 'bestreams.net', 'clicknupload.com', 'cloudzilla.to', 'movshare.net', 'novamov.com', 'nowvideo.sx', 'videoweed.es', 'daclips.in', 'datemule.com', 'fastvideo.in', 'faststream.in', 'filehoot.com', 'filenuke.com', 'sharesix.com', 'docs.google.com', 'plus.google.com', 'picasaweb.google.com', 'gorillavid.com', 'gorillavid.in', 'grifthost.com', 'hugefiles.net', 'ipithos.to', 'ishared.eu', 'kingfiles.net', 'mail.ru', 'my.mail.ru', 'videoapi.my.mail.ru', 'mightyupload.com', 'mooshare.biz', 'movdivx.com', 'movpod.net', 'movpod.in', 'movreel.com', 'mrfile.me', 'nosvideo.com', 'openload.io', 'played.to', 'bitshare.com', 'filefactory.com', 'k2s.cc', 'oboom.com', 'rapidgator.net', 'uploaded.net', 'primeshare.tv', 'bitshare.com', 'filefactory.com', 'k2s.cc', 'oboom.com', 'rapidgator.net', 'uploaded.net', 'sharerepo.com', 'stagevu.com', 'streamcloud.eu', 'streamin.to', 'thefile.me', 'thevideo.me', 'tusfiles.net', 'uploadc.com', 'zalaa.com', 'uploadrocket.net', 'uptobox.com', 'v-vids.com', 'veehd.com', 'vidbull.com', 'videomega.tv', 'vidplay.net', 'vidspot.net', 'vidto.me', 'vidzi.tv', 'vimeo.com', 'vk.com', 'vodlocker.com', 'xfileload.com', 'xvidstage.com', 'zettahost.tv']
g_ignoreSetResolved=['plugin.video.dramasonline','plugin.video.f4mTester','plugin.video.shahidmbcnet','plugin.video.SportsDevil','plugin.stream.vaughnlive.tv','plugin.video.ZemTV-shani']

class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response


sourceSitebvls = 'http://www.bvls2016.sc/'      
DCTVBase = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2R1dGNoc3BvcnRzdHJlYW1zL0RTUy9tYXN0ZXIveG1sL0luZGV4LnhtbA=='
addon = xbmcaddon.Addon('plugin.video.cloudtv')
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
favorites = os.path.join(profile, 'favorites')
history = os.path.join(profile, 'history')



fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
iconpath = xbmc.translatePath(os.path.join(home, 'resources/icons/'))
#icon = xbmc.translatePath(os.path.join(home, 'resources/icons/icon.png'))


REV = os.path.join(profile, 'list_revision')
Mode = addon.getAddonInfo('version')
icon = os.path.join(home, 'icon.png')
FANART = os.path.join(home, 'fanart.jpg')
source_file = os.path.join(profile, 'source_file')
functions_dir = profile

if not os.path.exists(profile):
    os.makedirs(profile)

S365COOKIEFILE='s365CookieFile.lwp'
S365COOKIEFILE=os.path.join(profile, S365COOKIEFILE)



class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response

def ShowSettings(Fromurl):
	selfAddon.openSettings()


def get365CookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(S365COOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar






downloader = downloader.SimpleDownloader()
debug = addon.getSetting('debug')
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else: FAV = []
if os.path.exists(source_file)==True:
    SOURCES = open(source_file).read()
else: SOURCES = []



    
    

###
API_URL = 'http://ida.omroep.nl/aapi/?stream='
BASE_URL = 'http://livestreams.omroep.nl/'
#USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25'
REF_URL = 'http://www.npo.nl'
TOKEN_URL = 'http://ida.omroep.nl/npoplayer/i.js'

def collect_token():
    req = urllib2.Request(TOKEN_URL)
    req.add_header('User-Agent', USER_AGENT)
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    token = re.search(r'npoplayer.token = "(.*?)"',page).group(1)
    #xbmc.log("plugin.video.nederland24:: oldtoken: %s" % token)
    # site change, token invalid, needs to be reordered. Thanks to rieter for figuring this out very quickly.
    first = -1
    last = -1
    for i in range(5, len(token) - 5, 1):
	#xbmc.log("plugin.video.nederland24:: %s" % token[i])
        if token[i].isdigit():
            if first < 0:
                first = i
                #xbmc.log("plugin.video.nederland24:: %s" % token[i])
            elif last < 0:
                last = i
                #xbmc.log("plugin.video.nederland24:: %s" % token[i])
                break

    newtoken = list(token)
    if first < 0 or last < 0:
        first = 12
        last = 13
    newtoken[first] = token[last]
    newtoken[last] = token[first]
    newtoken = ''.join(newtoken)
    #xbmc.log("plugin.video.nederland24:: newtoken: %s" % newtoken)
    return newtoken

def resolve_http_redirect(url, depth=0):
    if depth > 10:
        raise Exception("Redirected "+depth+" times, giving up.")
    o = urlparse.urlparse(url,allow_fragments=True)
    conn = httplib.HTTPConnection(o.netloc)
    path = o.path
    if o.query:
        path +='?'+o.query
    conn.request("HEAD", path)
    res = conn.getresponse()
    headers = dict(res.getheaders())
    if headers.has_key('location') and headers['location'] != url:
        return resolve_http_redirect(headers['location'], depth+1)
    else:
        return url
    
def streamNpo(source):
    URL=API_URL+BASE_URL+source+"&token=%s" % collect_token()
    req = urllib2.Request(URL)
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Referer', REF_URL)
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    videopre=re.search(r'http:(.*?)url',page).group()
    prostream= (videopre.replace('\/', '/'))
    finalUrl = resolve_http_redirect(prostream)
    return finalUrl

def findStream(page) :
    frameHtml = bitly.OPEN_URL2(page, sourceSitebvls, bitly.getUserAgent())
    b64coded = bitly.getBaseEncodedString(frameHtml)
    streamUrl = bitly.getStreamUrl(b64coded)
    return streamUrl

def addon_log(string):
    if debug == 'true':
        xbmc.log("[addon.live.cloudtvr3-%s]: %s" %(string))


def Play():
    paradise = 'http://shoutcast.paradiseradio.org:8390/'
    pl = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    pl.clear()    
    pl.add(paradise)

    xbmc.Player().play(pl)


def makeRequest(url, headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            addon_log('URL: '+url)
            if hasattr(e, 'code'):
                addon_log('We failed with error code - %s.' % e.code)
                xbmc.executebuiltin("XBMC.Notification(CloudTV,We failed with error code - "+str(e.code)+",10000,"+icon+")")
            elif hasattr(e, 'reason'):
                addon_log('We failed to reach a server.')
                addon_log('Reason: %s' %e.reason)
                xbmc.executebuiltin("XBMC.Notification(CloudTV,We failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")

				
def DCTVIndex():
    addon_log("DCTVIndex")
    addDir('[B][COLOR orange]Privacy Policy[/COLOR][/B]','Privacy Policy',45,'%s/p-p.png'% iconpath ,  FANART,'','','','')
    addDir('[B][COLOR yellow]NL Tv[/COLOR][/B]','aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2R1dGNoc3BvcnRzdHJlYW1zL0RTUy9tYXN0ZXIveG1sL0luZGV4TmxUdi54bWw=',10,iconpath+'nltv.png' ,  FANART,'','','','')
    addDir('[B][COLOR blue]NL Radio[/COLOR][/B]','aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2R1dGNoc3BvcnRzdHJlYW1zL0RTUy9tYXN0ZXIveG1sL0luZGV4UmFkaW8ueG1s',10,iconpath+'radio.png' ,  FANART,'','','','')
    addDir('[B][COLOR yellow]Int Tv[/COLOR][/B]','aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2R1dGNoc3BvcnRzdHJlYW1zL0RTUy9tYXN0ZXIveG1sL0luZGV4SW50VFYueG1s',10,iconpath+'tvint.png' ,  FANART,'','','','')
    addDir('[B][COLOR blue]Sport Tv[/COLOR][/B]','Sport',100,iconpath+'sporttv.png' ,  FANART,'','','','')
    addDir('[B][COLOR yellow]Music Tv[/COLOR][/B]','aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2R1dGNoc3BvcnRzdHJlYW1zL0RTUy9tYXN0ZXIveG1sL0luZGV4TXVzaWMueG1s',10,iconpath+'musictv.png' ,  FANART,'','','','')
    addDir('[B][COLOR blue]NL Youtube[/COLOR][/B]','aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2R1dGNoc3BvcnRzdHJlYW1zL0RTUy9tYXN0ZXIveG1sL0luZGV4WXR1YmUueG1s',10,iconpath+'youtube.png' ,  FANART,'','','','')
    addDir('My Own List','My Own List',48,icon ,  FANART,'','','','')
    addDir('Test Url','Test Url',47,icon,  FANART,'','','','')
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))





def CatIndex(url):
    try :
        getData(base64.b64decode(url),'')
    except:
        pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    

def IndexSport():
    addDir('[B][COLOR orange]DutchSportstreams[/COLOR][/B]','Sport',101,iconpath+'sporttv.png' ,  FANART,'','','','')
    try :
        getData(base64.b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2R1dGNoc3BvcnRzdHJlYW1zL0RTUy9tYXN0ZXIveG1sL0luZGV4U3BvcnQueG1s'),'')
    except:
        pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def IndexDSS():
    import geo
    if geo.returnCountyCode() == "NL":
        addDir('[B][COLOR yellow]bvls2016[/COLOR][/B]','Sport',102,iconpath+'sporttv.png' ,  FANART,'','','','')
    addDir('[B][COLOR blue]feed2all[/COLOR][/B]','Sport',104,iconpath+'sporttv.png' ,  FANART,'','','','')
    addDir('[B][COLOR yellow]wiz1.net[/COLOR][/B]','Sport',106,iconpath+'sporttv.png' ,  FANART,'','','','')
    addDir('[B][COLOR blue]goatd.net[/COLOR][/B]','Sport',107,iconpath+'sporttv.png' ,  FANART,'','','','')
    if geo.returnCountyCode() == "NL":
        addDir('[B][COLOR yellow]sport365[/COLOR][/B]','Sport',108,iconpath+'sporttv.png' ,  FANART,'','','','')
    addDir('[B][COLOR blue]wizhdsports[/COLOR][/B]','Sport',109,iconpath+'sporttv.png' ,  FANART,'','','','')
    try :
        getData(base64.b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2R1dGNoc3BvcnRzdHJlYW1zL0RTUy9tYXN0ZXIveG1sL0luZGV4ZHNzLnhtbA=='),'')
    except:
        pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


    


def MyIndex():
    if addon.getSetting('Pastebin_On1') == 'true':
        MyBase1 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl1')
    else:
        MyBase1 = addon.getSetting('MyOwnListUrl1')
    if addon.getSetting('Pastebin_On2') == 'true':
        MyBase2 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl2')
    else:
        MyBase2 = addon.getSetting('MyOwnListUrl2')
    if addon.getSetting('Pastebin_On3') == 'true':
        MyBase3 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl3')
    else:
        MyBase3 = addon.getSetting('MyOwnListUrl3')
    if addon.getSetting('Pastebin_On4') == 'true':
        MyBase4 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl4')
    else:
        MyBase4 = addon.getSetting('MyOwnListUrl4')
    if addon.getSetting('Pastebin_On5') == 'true':
        MyBase5 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl5')
    else:
        MyBase5 = addon.getSetting('MyOwnListUrl5')
    if addon.getSetting('Pastebin_On6') == 'true':
        MyBase6 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl6')
    else:
        MyBase6 = addon.getSetting('MyOwnListUrl6')
    if addon.getSetting('Pastebin_On7') == 'true':
        MyBase7 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl7')
    else:
        MyBase7 = addon.getSetting('MyOwnListUrl7')
    if addon.getSetting('Pastebin_On8') == 'true':
        MyBase8 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl8')
    else:
        MyBase8 = addon.getSetting('MyOwnListUrl8')
    if addon.getSetting('Pastebin_On9') == 'true':
        MyBase9 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl9')
    else:
        MyBase9 = addon.getSetting('MyOwnListUrl9')
    if addon.getSetting('Pastebin_On10') == 'true':
        MyBase10 = 'http://pastebin.com/raw/' + addon.getSetting('MyOwnListUrl10')
    else:
        MyBase10 = addon.getSetting('MyOwnListUrl10')
    addon_log("DCTVIndex")
    addDir(addon.getSetting('MyOwnListTitle1'),MyBase1,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle2'),MyBase2,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle3'),MyBase3,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle4'),MyBase4,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle5'),MyBase5,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle6'),MyBase6,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle7'),MyBase7,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle8'),MyBase8,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle9'),MyBase9,6,icon ,  FANART,'','','','')
    addDir(addon.getSetting('MyOwnListTitle10'),MyBase10,6,icon ,  FANART,'','','','')
    
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
       

def Nieuws():
	text = ''
	twit = 'http://dctv.comlu.com/xml/news.xml'
	req = urllib2.Request(twit)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile("<title>(.+?)</title><pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)
	for status, dte in match:
	    try:
			    status = status.decode('ascii', 'ignore')
	    except:
			    status = status.decode('utf-8','ignore')
	    dte = dte[:-15]
	    status = status.replace('&amp;','')
	    dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
	    text = text+dte+'\n'+status+'\n'+'\n'
	showText('[COLOR blue][B]Dutch Cloud Tv Laaste Nieuws[/B][/COLOR]', text)



def Privacy_Policy():
	dialog = xbmcgui.Dialog()
        dialog.ok("Privacy Policy", "No video or videos are hosted by dutch cloud tv.", "Any of the video you can find here may be gotten for free on sites like Justin.tv, Ustream.tv, Selfcast, bvls2016, and many others.Note we do not promise or guarantee our service and are not responsible for any action of our user's.We have no partnership and don't request to have partnership with any owner of video's or stream's given on our website.","All content is copyright of their respective owners.")
        
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
	try:
	    xbmc.sleep(10)
	    retry -= 1
	    win.getControl(1).setLabel(heading)
	    win.getControl(5).setText(text)
	    return
	except:
	    pass
		
	
def getSources():
        if os.path.exists(favorites) == True:
            addDir('Favorites','url',4,os.path.join(home, 'resources', 'favorite.png'),FANART,'','','','')
        if addon.getSetting("browse_xml_database") == "true":
            addDir('XML Database','http://xbmcplus.xb.funpic.de/www-data/filesystem/',15,icon,FANART,'','','','')
        if addon.getSetting("browse_community") == "true":
            addDir('Community Files','community_files',16,icon,FANART,'','','','')
        if os.path.exists(history) == True:
            addDir('Search History','history',25,os.path.join(home, 'resources', 'favorite.png'),FANART,'','','','')
        if addon.getSetting("searchyt") == "true":
            addDir('Search:Youtube','youtube',25,icon,FANART,'','','','')
        if addon.getSetting("searchDM") == "true":
            addDir('Search:dailymotion','dmotion',25,icon,FANART,'','','','')
        if addon.getSetting("PulsarM") == "true":
            addDir('Pulsar:IMDB','IMDBidplay',27,icon,FANART,'','','','')            
        if os.path.exists(source_file)==True:
            sources = json.loads(open(source_file,"r").read())
            #print 'sources',sources
            if len(sources) > 1:
                for i in sources:
                    ## for pre 1.0.8 sources
                    if isinstance(i, list):
                        addDir(i[0].encode('utf-8'),i[1].encode('utf-8'),1,icon,FANART,'','','','','source')
                    else:
                        thumb = icon
                        fanart = FANART
                        desc = ''
                        date = ''
                        credits = ''
                        genre = ''
                        if i.has_key('thumbnail'):
                            thumb = i['thumbnail']
                        if i.has_key('fanart'):
                            fanart = i['fanart']
                        if i.has_key('description'):
                            desc = i['description']
                        if i.has_key('date'):
                            date = i['date']
                        if i.has_key('genre'):
                            genre = i['genre']
                        if i.has_key('credits'):
                            credits = i['credits']
                        addDir(i['title'].encode('utf-8'),i['url'].encode('utf-8'),1,thumb,fanart,desc,genre,date,credits,'source')

            else:
                if len(sources) == 1:
                    if isinstance(sources[0], list):
                        getData(sources[0][1].encode('utf-8'),FANART)
                    else:
                        getData(sources[0]['url'], sources[0]['fanart'])



def addSource(url=None):
        if url is None:
            if not addon.getSetting("new_file_source") == "":
               source_url = addon.getSetting('new_file_source').decode('utf-8')
            elif not addon.getSetting("new_url_source") == "":
               source_url = addon.getSetting('new_url_source').decode('utf-8')
        else:
            source_url = url
        if source_url == '' or source_url is None:
            return
        addon_log('Adding New Source: '+source_url.encode('utf-8'))

        media_info = None
        #print 'source_url',source_url
        data = getSoup(source_url)
        #print 'source_url',source_url
        if isinstance(data,BeautifulSOAP):
            if data.find('channels_info'):
                media_info = data.channels_info
            elif data.find('items_info'):
                media_info = data.items_info
        if media_info:
            source_media = {}
            source_media['url'] = source_url
            try: source_media['title'] = media_info.title.string
            except: pass
            try: source_media['thumbnail'] = media_info.thumbnail.string
            except: pass
            try: source_media['fanart'] = media_info.fanart.string
            except: pass
            try: source_media['genre'] = media_info.genre.string
            except: pass
            try: source_media['description'] = media_info.description.string
            except: pass
            try: source_media['date'] = media_info.date.string
            except: pass
            try: source_media['credits'] = media_info.credits.string
            except: pass
        else:
            if '/' in source_url:
                nameStr = source_url.split('/')[-1].split('.')[0]
            if '\\' in source_url:
                nameStr = source_url.split('\\')[-1].split('.')[0]
            if '%' in nameStr:
                nameStr = urllib.unquote_plus(nameStr)
            keyboard = xbmc.Keyboard(nameStr,'Displayed Name, Rename?')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            newStr = keyboard.getText()
            if len(newStr) == 0:
                return
            source_media = {}
            source_media['title'] = newStr
            source_media['url'] = source_url
            source_media['fanart'] = fanart

        if os.path.exists(source_file)==False:
            source_list = []
            source_list.append(source_media)
            b = open(source_file,"w")
            b.write(json.dumps(source_list))
            b.close()
        else:
            sources = json.loads(open(source_file,"r").read())
            sources.append(source_media)
            b = open(source_file,"w")
            b.write(json.dumps(sources))
            b.close()
        addon.setSetting('new_url_source', "")
        addon.setSetting('new_file_source', "")
        xbmc.executebuiltin("XBMC.Notification(CloudTV,New source added.,5000,"+icon+")")
        addon.openSettings()


def rmSource(name):
        sources = json.loads(open(source_file,"r").read())
        for index in range(len(sources)):
            if isinstance(sources[index], list):
                if sources[index][0] == name:
                    del sources[index]
                    b = open(source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    break
            else:
                if sources[index]['title'] == name:
                    del sources[index]
                    b = open(source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    break
        xbmc.executebuiltin("XBMC.Container.Refresh")



def get_xml_database(url, browse=False):
        soup = BeautifulSoup(makeRequest(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        for i in soup('a'):
            href = i['href']
            if not href.startswith('?'):
                name = i.string
                if name not in ['Parent Directory', 'recycle_bin/']:
                    if href.endswith('/'):
                        if browse:
                            addDir(name,url+href,15,icon,fanart,'','','')
                        else:
                            addDir(name,url+href,14,icon,fanart,'','','')
                    elif href.endswith('.xml'):
                        if browse:
                            addDir(name,url+href,1,icon,fanart,'','','','','download')
                        else:
                            if os.path.exists(source_file)==True:
                                if name in SOURCES:
                                    addDir(name+' (in use)',url+href,11,icon,fanart,'','','','','download')
                                else:
                                    addDir(name,url+href,11,icon,fanart,'','','','','download')
                            else:
                                addDir(name,url+href,11,icon,fanart,'','','','','download')





def getSoup(url,data=None):
        #print 'getsoup',url,data
        if url.startswith('http://') or url.startswith('https://'):
            data = makeRequest(url)
            if re.search("#EXTM3U",data) or 'm3u' in url: 
                #print 'found m3u data',data
                return data
                
        elif data == None:
            if xbmcvfs.exists(url):
                if url.startswith("smb://") or url.startswith("nfs://"):
                    copy = xbmcvfs.copy(url, os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    if copy:
                        data = open(os.path.join(profile, 'temp', 'sorce_temp.txt'), "r").read()
                        xbmcvfs.delete(os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    else:
                        addon_log("failed to copy from smb:")
                else:
                    data = open(url, 'r').read()
                    if re.match("#EXTM3U",data)or 'm3u' in url: 
                        #print 'found m3u data',data
                        return data
            else:
                addon_log("Soup Data not found!")
                return
        return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)


def getData(url,fanart):
    if addon.getSetting('Thumbnail_On') =="true":
        SetViewLayout = "Thumbnail"
    else:
        SetViewLayout = "List"
     
    soup = getSoup(url)
    #print type(soup)
    if isinstance(soup,BeautifulSOAP):
        if len(soup('layoutype')) < 1:
            SetViewLayout = "List"	    

        if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:
#                print channel

                linkedUrl=''
                lcount=0
                try:
                    linkedUrl =  channel('externallink')[0].string
                    lcount=len(channel('externallink'))
                except: pass
                #print 'linkedUrl',linkedUrl,lcount
                if lcount>1: linkedUrl=''

                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = icon

                try:
                    if not channel('fanart'):
                        if addon.getSetting('use_thumb') == "true":
                            fanArt = thumbnail
                        else:
                            fanArt = fanart
                    else:
                        fanArt = channel('fanart')[0].string
                    if fanArt == None:
                        raise
                except:
                    fanArt = fanart

                try:
                    desc = channel('info')[0].string
                    if desc == None:
                        raise
                except:
                    desc = ''

                try:
                    genre = channel('genre')[0].string
                    if genre == None:
                        raise
                except:
                    genre = ''

                try:
                    date = channel('date')[0].string
                    if date == None:
                        raise
                except:
                    date = ''

                try:
                    credits = channel('credits')[0].string
                    if credits == None:
                        raise
                except:
                    credits = ''

                try:
                    if linkedUrl=='':
                        addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                    else:
                        #print linkedUrl
                        addDir(name.encode('utf-8'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                except:
                    addon_log('There was a problem adding directory from getData(): '+name.encode('utf-8', 'ignore'))
        else:
            addon_log('No Channels: getItems')
            getItems(soup('item'),fanart)
    else:
        try:
            parse_m3u(soup)
        except:
            pass
            

    if SetViewLayout == "Thumbnail":
       SetViewThumbnail()
    if SetViewLayout == "List":
       SetViewList()

	
	
# borrow from https://github.com/enen92/P2P-Streams-XBMC/blob/master/plugin.video.p2p-streams/resources/core/livestreams.py
# This will not go through the getItems functions ( means you must have ready to play url, no regex)
def parse_m3u(data):
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
    total = len(match)
    print 'total m3u links',total
    for other,channel_name,stream_url in match:
        if 'tvg-logo' in other:
            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
            if thumbnail:
                if thumbnail.startswith('http'):
                    thumbnail = thumbnail

                elif not addon.getSetting('logo-folderPath') == "":
                    logo_url = addon.getSetting('logo-folderPath')
                    thumbnail = logo_url + thumbnail

                else:
                    thumbnail = thumbnail
            #else:

        else:
            thumbnail = icon
        if 'type' in other:
            mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
            if mode_type == 'yt-dl':
                stream_url = stream_url +"&mode=18"
            elif mode_type == 'regex':
                url = stream_url.split('&regexs=')
                #print url[0] getSoup(url,data=None)
                regexs = parse_regex(getSoup('',data=url[1]))

                addLink(url[0], channel_name,thumbnail,'','','','','',None,regexs,total)
                continue
            elif mode_type == 'ftv':
                stream_url = 'plugin://plugin.video.F.T.V/?name='+urllib.quote(channel_name) +'&url=' +stream_url +'&mode=125&ch_fanart=na'
        addLink(stream_url, channel_name,thumbnail,'','','','','',None,'',total)
	
def getChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('channel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('item')
        try:
            fanArt = channel_list('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = icon
            try:
                if not channel('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                pass
            try:
                desc = channel('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = channel('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = channel('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            try:
                credits = channel('credits')[0].string
                if credits == None:
                    raise
            except:
                credits = ''

            try:
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc,genre,credits,date)
            except:
                addon_log('There was a problem adding directory - '+name.encode('utf-8', 'ignore'))
        getItems(items,fanArt)


def getSubChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('subchannel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('subitem')
        getItems(items,fanart)

#hakamac
def GetSublinks(name,url,iconimage,fanart):
    List=[]; ListU=[]; c=0
    all_videos = regex_get_all(url, 'sublink:', '--#')
    for a in all_videos:
        if 'LISTSOURCE:' in a:
            vurl = regex_from_to(a, 'LISTSOURCE:', '::')
            linename = regex_from_to(a, 'LISTNAME:', '::')
        else:
            vurl = a.replace('sublink:','').replace('--#','')
            linename = name
        if len(vurl) > 10:
            c=c+1; List.append(linename); ListU.append(vurl)
 
    if c==1:
        try:
            liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=ListU[0],listitem=liz)
            xbmc.Player().play(urlsolver(ListU[0]), liz)
        except:
            pass
    else:
         dialog=xbmcgui.Dialog()
         rNo=dialog.select('CloudTV Select A Source', List)
         if rNo>=0:
             rName=str(List[rNo])
             rURL=str(ListU[rNo])
             #print 'Sublinks   Name:' + name + '   url:' + rURL
             try:
                 liz=xbmcgui.ListItem(rName, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": rName } )
                 ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=rURL,listitem=liz)
                 xbmc.Player().play(urlsolver(rURL), liz)
             except:
                 pass

				
def SearchChannels():
#hakamac code
    KeyboardMessage = 'Name of channel show or movie'
    Searchkey = ''
    keyboard = xbmc.Keyboard(Searchkey, KeyboardMessage)
    keyboard.doModal()
    if keyboard.isConfirmed():
       Searchkey = keyboard.getText().replace('\n','').strip()
       if len(Searchkey) == 0: 
          xbmcgui.Dialog().ok('CloudTV', 'Nothing Entered')
          return	   
    
    Searchkey = Searchkey.lower()
    List=[]
    List.append(DCTVBase)
    PassedUrls = 0
    FoundChannel = 1 
    ReadChannel = 0
    FoundMatch = 0
    progress = xbmcgui.DialogProgress()
    progress.create('CloudTV Searching Please wait',' ')
	
    while FoundChannel <> ReadChannel:
        BaseSearch = List[ReadChannel].strip()
        #print 'read this one from file list (' + str(ReadChannel) + ')'  
        ReadChannel = ReadChannel + 1

        PageSource = ''
        try:
            PageSource = net.http_GET(BaseSearch).content
            PageSource = PageSource.encode('ascii', 'ignore').decode('ascii')
            #time.sleep(1)
        except: 
            pass
		
        if len(PageSource) < 10:
            PageSource = ''
            PassedUrls = PassedUrls + 1
            #print '*** PASSED ****' + BaseSearch + '  ************* Total Passed Urls: ' + str(PassedUrls)
            time.sleep(.5)
 
        percent = int( ( ReadChannel / 300) * 100) 
        message = '     Pages Read: '+str(ReadChannel)+'        Matches Found: ' + str(FoundMatch)
        progress.update(percent,"", message, "" )

        if progress.iscanceled():
           return
 		
        if len(PageSource) > 10:
            all_links = regex_get_all(PageSource, '<channel>', '</channel>')
            for a in all_links:
                vurl = regex_from_to(a, '<externallink>', '</externallink>')
                #name = regex_from_to(a, '<name>', '</name>')
                #print name + '    ' + vurl
                if len(vurl) > 5:
                   FoundChannel = FoundChannel + 1
                   List.append(vurl)
                   #print 'Found Channel: '+ str(FoundChannel) +' : '+ vurl 

            all_items = regex_get_all(PageSource, '<item>', '</item>')
            for a in all_items:
                vurl = regex_from_to(a, '<link>', '</link>')
                name = regex_from_to(a, '<title>', '</title>')
                TestName = '  ' + name.lower() + '  '
                #print 'Testing:' + TestName + '  ' + Searchkey
                if len(vurl) > 5 and TestName.find(Searchkey) > 0:
                    FoundMatch = FoundMatch + 1
                    fanart = ''
                    thumbnail = regex_from_to(a, '<thumbnail>', '</thumbnail>')
                    fanart = regex_from_to(a, '<fanart>', '</fanart>')
                    if len(fanart) < 5:
                       fanart = icon
                    if vurl.find('sublink') > 0:
                        addDir(name,vurl,30,thumbnail,fanart,'','','','')
                    else: 
                        addLink(str(vurl),name,thumbnail,fanart,'','','',True,None,'',1)
						
    
    progress.close()
    xbmc.executebuiltin("Container.SetViewMode(50)")
	
def Search_m3u(data,Searchkey):
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(content)
    total = len(match)
    #print 'total m3u links',total
    for other,channel_name,stream_url in match:
        if 'tvg-logo' in other:
            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
            if thumbnail:
                if thumbnail.startswith('http'):
                    thumbnail = thumbnail
                
                elif not addon.getSetting('logo-folderPath') == "":
                    logo_url = addon.getSetting('logo-folderPath')
                    thumbnail = logo_url + thumbnail

                else:
                    thumbnail = thumbnail
            #else:
            
        else:
            thumbnail = ''
        if 'type' in other:
            mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
            if mode_type == 'regex':
                url = stream_url.split('&regexs=')
                #print url[0] getSoup(url,data=None)
                regexs = parse_regex(getSoup('',data=url[1]))
                
                addLink(url[0], channel_name,thumbnail,'','','','','',None,regexs,total)
                continue
        addLink(stream_url, channel_name,thumbnail,'','','','','',None,'',total)

def FindFirstPattern(text,pattern):
    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result
	
def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r				

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
	   try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
	   except: r = ''
    else:
       try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
       except: r = ''
    return r

def getItems(items,fanart):
        total = len(items)
        #print 'START GET ITEMS *****'
        addon_log('Total Items: %s' %total)
        for item in items:
            isXMLSource=False
            isJsonrpc = False
            try:
                name = item('title')[0].string
                if name is None:
                    name = 'unknown?'
            except:
                addon_log('Name Error')
                name = ''


            try:
                url = []
                if len(item('link')) >0:
#                    print 'item link', item('link')
                    for i in item('link'):
                        if not i.string == None:
                            url.append(i.string)
                    
                elif len(item('sportsdevil')) >0:
                    for i in item('sportsdevil'):
                        if not i.string == None:
                            sportsdevil = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +i.string
                            referer = item('referer')[0].string
                            if referer:
                                #print 'referer found'
                                sportsdevil = sportsdevil + '%26referer=' +referer
                            url.append(sportsdevil)
                elif len(item('p2p')) >0:
                    for i in item('p2p'):
                        if not i.string == None:
                            if addon.getSetting('default_player') == 'p2p-streams':
                                if 'sop://' in i:
                                    sop = 'plugin://plugin.video.p2p-streams/?url='+i.string +'&amp;mode=2&amp;' + 'name='+name 
                                    url.append(sop) 
                                else:
                                    p2p='plugin://plugin.video.p2p-streams/?url='+i.string +'&mode=1&name=' +name 
                                url.append(p2p)
                            else:
                                if 'sop://' in i:
                                    sop = 'plugin://program.plexus/?url='+i.string +'&amp;mode=2&amp;' + 'name='+name 
                                    url.append(sop) 
                                else:
                                    p2p='plugin://program.plexus/?url='+i.string +'&mode=1&name=' +name 
                                url.append(p2p)
                elif len(item('torrent')) >0:
                    for i in item('torrent'):
                        if not i.string == None:
                            title = item('title')[0].string
                            name = base64.b64decode(title)
                            if addon.getSetting('torrent_player') == 'Pulsar':
                                torrent = 'plugin://plugin.video.pulsar/play?uri='+base64.b64decode(i.string)
                            else: #addon.getSetting('torrent_player') == 'KmediaTorrent':
                                torrent = 'plugin://plugin.video.kmediatorrent/play/'+base64.b64decode(i.string)
                            #elif addon.getSetting('torrent_player') == 'Torrenter':
                                #torrent = 'plugin://plugin.video.torrenter/?action=playSTRM&url='+i.string+'&not_download_only=True'
                            #elif addon.getSetting('torrent_player') == 'YATP':
                                #torrent = 'plugin://plugin.video.yatp/?action=play&torrent='+i.string
                            #else :
                                #torrent = 'plugin.video.xbmctorrent/play/'+i.string
                            url.append(torrent)
                elif len(item('vaughn')) >0:
                    for i in item('vaughn'):
                        if not i.string == None:
                            vaughn = 'plugin://plugin.stream.vaughnlive.tv/?mode=PlayLiveStream&amp;channel='+i.string
                            url.append(vaughn)
                elif len(item('veetle')) >0:
                    for i in item('veetle'):
                        if not i.string == None:
                            veetle = 'plugin://plugin.video.veetle/?channel='+i.string
                        url.append(veetle)
                elif len(item('npo')) >0:
                    for i in item('npo'):
                        if not i.string == None:
                            npo = streamNpo(i.string)
                    url.append(npo)
                elif len(item('bvls')) >0:
                    for i in item('bvls'):
                        if not i.string == None:
                            title = item('title')[0].string 
                            streamUrl = findStream(i.string)
                            if (bitly.getResponse(streamUrl)) :
                                color = 'green'
                                if streamUrl[-4:] == '.flv' :
                                    streamUrl = bitly.VeetleId(streamUrl)
                            else :
                                color = 'red'
                            name='[COLOR '+color+']' + title + '[/COLOR]' 
                            bvls = streamUrl
                            url.append(bvls)
                elif len(item('ilive')) >0:
                    for i in item('ilive'):
                        if not i.string == None:
                            if not 'http' in i.string:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url=http://www.streamlive.to/view/'+i.string+'&amp;link=99&amp;mode=iLivePlay'
                            else:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url='+i.string+'&amp;link=99&amp;mode=iLivePlay'
                        url.append(ilive)
                elif len(item('ytlist')) >0:
                    for i in item('ytlist'):
                        thumbnail = item('thumbnail')[0].string
                        title = item('title')[0].string
                        plugintools.add_item( 
                        #action="", 
                        title=title,
                        url="plugin://plugin.video.youtube/user/"+i.string+"/",
                        thumbnail= thumbnail,
                        folder=True )
                elif len(item('utube')) >0:
                    for i in item('utube'):
                        if not i.string == None:
                            if len(i.string) == 11:
                                utube = 'plugin://plugin.video.youtube/play/?video_id='+ i.string 
                            elif i.string.startswith('PL') and not '&order=' in i.string :
                                utube = 'plugin://plugin.video.youtube/play/?&order=default&playlist_id=' + i.string
                            else:
                                utube = 'plugin://plugin.video.youtube/play/?playlist_id=' + i.string 
                    url.append(utube)
                elif len(item('imdb')) >0:
                    for i in item('imdb'):
                        if not i.string == None:
                            if addon.getSetting('genesisorpulsar') == '0':
                                imdb = 'plugin://plugin.video.genesis/?action=play&imdb='+i.string
                            else:
                                imdb = 'plugin://plugin.video.pulsar/movie/tt'+i.string+'/play'
                            url.append(imdb)                      
                elif len(item('f4m')) >0:
                        for i in item('f4m'):
                            if not i.string == None:
                                if '.f4m' in i.string:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)
                                elif '.m3u8' in i.string:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)+'&amp;streamtype=HLS'
                                    
                                else:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(i.string)+'&amp;streamtype=SIMPLE'
                        url.append(f4m)
                elif len(item('ftv')) >0:
                    for i in item('ftv'):
                        if not i.string == None:
                            ftv = 'plugin://plugin.video.F.T.V/?name='+urllib.quote(name) +'&url=' +i.string +'&mode=125&ch_fanart=na'
                        url.append(ftv)                        
                if len(url) < 1:
                    raise
            except:
                addon_log('Error <link> element, Passing:'+name.encode('utf-8', 'ignore'))
                continue
                
            isXMLSource=False

            try:
                isXMLSource = item('externallink')[0].string
            except: pass
            
            if isXMLSource:
                ext_url=[isXMLSource]
                isXMLSource=True
            else:
                isXMLSource=False
            try:
                isJsonrpc = item('jsonrpc')[0].string
            except: pass
            if isJsonrpc:
                ext_url=[isJsonrpc]
                isJsonrpc=True
            else:
                isJsonrpc=False            
            try:
                thumbnail = item('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not item('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                    else:
                        fanArt = fanart
                else:
                    fanArt = item('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                fanArt = fanart
            try:
                desc = item('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = item('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = item('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            regexs = None
            if item('regex'):
                try:
                    reg_item = item('regex')
                    regexs = parse_regex(reg_item)
                except:
                    pass            
           
            try:
                if len(url) > 1:
                    
                    alt = 0
                    playlist = []
                    for i in url:
                    	if addon.getSetting('ask_playlist_items') == 'true':
	                        if regexs:
	                            playlist.append(i+'&regexs='+regexs)
	                        elif  any(x in i for x in resolve_url) and  i.startswith('http'):
	                            playlist.append(i+'&mode=19')                            
                        else:
                            playlist.append(i)
                    if addon.getSetting('add_playlist') == "false":                    
                            for i in url:
                                alt += 1
                                #print 'ADDLINK 1'
                                addLink(i,'%s) %s' %(alt, name.encode('utf-8', 'ignore')),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)                            
                    else:
                        addLink('', name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)
                else:
                    if isXMLSource:
                    	addDir(name.encode('utf-8'),ext_url[0].encode('utf-8'),1,thumbnail,fanart,desc,genre,date,None,'source')
                    elif isJsonrpc:
                        addDir(name.encode('utf-8'),ext_url[0],53,thumbnail,fanart,desc,genre,date,None,'source')
                    elif url[0].find('sublink') > 0:
                        addDir(name.encode('utf-8'),url[0],30,thumbnail,fanArt,desc,regexs,'','','')
                        #addDir(name.encode('utf-8'),url[0],30,thumbnail,fanart,desc,genre,date,'sublink')				
                    else: 
                        addLink(url[0],name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)

                    #print 'success'
            except:
                addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))
        #print 'FINISH GET ITEMS *****'      

def parse_regex(reg_item):
                try:
                    regexs = {}
                    for i in reg_item:
                        regexs[i('name')[0].string] = {}
                        #regexs[i('name')[0].string]['expre'] = i('expres')[0].string
                        try:
                            regexs[i('name')[0].string]['expre'] = i('expres')[0].string
                            if not regexs[i('name')[0].string]['expre']:
                                regexs[i('name')[0].string]['expre']=''
                        except:
                            addon_log("Regex: -- No Referer --")
                        regexs[i('name')[0].string]['page'] = i('page')[0].string
                        try:
                            regexs[i('name')[0].string]['refer'] = i('referer')[0].string
                        except:
                            addon_log("Regex: -- No Referer --")
                        try:
                            regexs[i('name')[0].string]['connection'] = i('connection')[0].string
                        except:
                            addon_log("Regex: -- No connection --")

                        try:
                            regexs[i('name')[0].string]['notplayable'] = i('notplayable')[0].string
                        except:
                            addon_log("Regex: -- No notplayable --")
                            
                        try:
                            regexs[i('name')[0].string]['noredirect'] = i('noredirect')[0].string
                        except:
                            addon_log("Regex: -- No noredirect --")
                        try:
                            regexs[i('name')[0].string]['origin'] = i('origin')[0].string
                        except:
                            addon_log("Regex: -- No origin --")
                        try:
                            regexs[i('name')[0].string]['includeheaders'] = i('includeheaders')[0].string
                        except:
                            addon_log("Regex: -- No includeheaders --")                            
                            
                        try:
                            regexs[i('name')[0].string]['x-req'] = i('x-req')[0].string
                        except:
                            addon_log("Regex: -- No x-req --")
                        try:
                            regexs[i('name')[0].string]['x-forward'] = i('x-forward')[0].string
                        except:
                            addon_log("Regex: -- No x-forward --")

                        try:
                            regexs[i('name')[0].string]['agent'] = i('agent')[0].string
                        except:
                            addon_log("Regex: -- No User Agent --")
                        try:
                            regexs[i('name')[0].string]['post'] = i('post')[0].string
                        except:
                            addon_log("Regex: -- Not a post")
                        try:
                            regexs[i('name')[0].string]['rawpost'] = i('rawpost')[0].string
                        except:
                            addon_log("Regex: -- Not a rawpost")
                        try:
                            regexs[i('name')[0].string]['htmlunescape'] = i('htmlunescape')[0].string
                        except:
                            addon_log("Regex: -- Not a htmlunescape")


                        try:
                            regexs[i('name')[0].string]['readcookieonly'] = i('readcookieonly')[0].string
                        except:
                            addon_log("Regex: -- Not a readCookieOnly")
                        #print i
                        try:
                            regexs[i('name')[0].string]['cookiejar'] = i('cookiejar')[0].string
                            if not regexs[i('name')[0].string]['cookiejar']:
                                regexs[i('name')[0].string]['cookiejar']=''
                        except:
                            addon_log("Regex: -- Not a cookieJar")							
                        try:
                            regexs[i('name')[0].string]['setcookie'] = i('setcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a setcookie")
                        try:
                            regexs[i('name')[0].string]['appendcookie'] = i('appendcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a appendcookie")
                                                    
                        try:
                            regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        except:
                            addon_log("Regex: -- no ignorecache")
                        #try:
                        #    regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        #except:
                        #    addon_log("Regex: -- no ignorecache")			

                    regexs = urllib.quote(repr(regexs))
                    return regexs
                    #print regexs
                except:
                    regexs = None
                    addon_log('regex Error: '+name.encode('utf-8', 'ignore'))
#copies from lamda's implementation
def get_ustream(url):
    try:
        for i in range(1, 51):
            result = getUrl(url)
            if "EXT-X-STREAM-INF" in result: return url
            if not "EXTM3U" in result: return
            xbmc.sleep(2000)
        return
    except:
        return


 
def getRegexParsed(regexs, url,cookieJar=None,forCookieJarOnly=False,recursiveCall=False,cachedPages={}, rawPost=False, cookie_jar_file=None):#0,1,2 = URL, regexOnly, CookieJarOnly
        if not recursiveCall:
            regexs = eval(urllib.unquote(regexs))
        #cachedPages = {}
        #print 'url',url
        doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
        #print 'doRegexs',doRegexs,regexs
        setresolved=True
              
 


        for k in doRegexs:
            if k in regexs:
                #print 'processing ' ,k
                m = regexs[k]
                #print m
                cookieJarParam=False


                if  'cookiejar' in m: # so either create or reuse existing jar
                    #print 'cookiejar exists',m['cookiejar']
                    cookieJarParam=m['cookiejar']
                    if  '$doregex' in cookieJarParam:
                        cookieJar=getRegexParsed(regexs, m['cookiejar'],cookieJar,True, True,cachedPages)
                        cookieJarParam=True
                    else:
                        cookieJarParam=True
                #print 'm[cookiejar]',m['cookiejar'],cookieJar
                if cookieJarParam:
                    if cookieJar==None:
                        #print 'create cookie jar'
                        cookie_jar_file=None
                        if 'open[' in m['cookiejar']:
                            cookie_jar_file=m['cookiejar'].split('open[')[1].split(']')[0]
                            
                        cookieJar=getCookieJar(cookie_jar_file)
                        if cookie_jar_file:
                            saveCookieJar(cookieJar,cookie_jar_file)
                        #import cookielib
                        #cookieJar = cookielib.LWPCookieJar()
                        #print 'cookieJar new',cookieJar
                    elif 'save[' in m['cookiejar']:
                        cookie_jar_file=m['cookiejar'].split('save[')[1].split(']')[0]
                        complete_path=os.path.join(profile,cookie_jar_file)
                        print 'complete_path',complete_path
                        saveCookieJar(cookieJar,cookie_jar_file)
                        
 
                if  m['page'] and '$doregex' in m['page']:
                    m['page']=getRegexParsed(regexs, m['page'],cookieJar,recursiveCall=True,cachedPages=cachedPages)

                if 'setcookie' in m and m['setcookie'] and '$doregex' in m['setcookie']:
                    m['setcookie']=getRegexParsed(regexs, m['setcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                if 'appendcookie' in m and m['appendcookie'] and '$doregex' in m['appendcookie']:
                    m['appendcookie']=getRegexParsed(regexs, m['appendcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)

                 
                if  'post' in m and '$doregex' in m['post']:
                    m['post']=getRegexParsed(regexs, m['post'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                    #print 'post is now',m['post']

                if  'rawpost' in m and '$doregex' in m['rawpost']:
                    m['rawpost']=getRegexParsed(regexs, m['rawpost'],cookieJar,recursiveCall=True,cachedPages=cachedPages,rawPost=True)
                    #print 'rawpost is now',m['rawpost']
  
                if 'rawpost' in m and '$epoctime$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime$',getEpocTime())
  
                if 'rawpost' in m and '$epoctime2$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime2$',getEpocTime2())

  
                link=''
                if m['page'] and m['page'] in cachedPages and not 'ignorecache' in m and forCookieJarOnly==False :
                    link = cachedPages[m['page']]
                else:
                    if m['page'] and  not m['page']=='' and  m['page'].startswith('http'):
                        if '$epoctime$' in m['page']:
                            m['page']=m['page'].replace('$epoctime$',getEpocTime())
                        if '$epoctime2$' in m['page']:
                            m['page']=m['page'].replace('$epoctime2$',getEpocTime2())

                        #print 'Ingoring Cache',m['page']
                        page_split=m['page'].split('|')
                        pageUrl=page_split[0]
                        header_in_page=None
                        if len(page_split)>1:
                            header_in_page=page_split[1]
                        req = urllib2.Request(pageUrl)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                        if 'refer' in m:
                            req.add_header('Referer', m['refer'])
                        if 'agent' in m:
                            req.add_header('User-agent', m['agent'])
                        if 'x-req' in m:
                            req.add_header('X-Requested-With', m['x-req'])
                        if 'x-forward' in m:
                            req.add_header('X-Forwarded-For', m['x-forward'])
                        if 'setcookie' in m:
                            print 'adding cookie',m['setcookie']
                            req.add_header('Cookie', m['setcookie'])
                        if 'appendcookie' in m:
                            print 'appending cookie to cookiejar',m['appendcookie']
                            cookiestoApend=m['appendcookie']
                            cookiestoApend=cookiestoApend.split(';')
                            for h in cookiestoApend:
                                n,v=h.split('=')
                                w,n= n.split(':')
                                ck = cookielib.Cookie(version=0, name=n, value=v, port=None, port_specified=False, domain=w, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                                cookieJar.set_cookie(ck)

                                

                            
                        if 'origin' in m:
                            req.add_header('Origin', m['origin'])
                        if header_in_page:
                            header_in_page=header_in_page.split('&')
                            for h in header_in_page:
                                n,v=h.split('=')
                                req.add_header(n,v)


                        if not cookieJar==None:
                            #print 'cookieJarVal',cookieJar
                            cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
                            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                            opener = urllib2.install_opener(opener)
                            if 'noredirect' in m:
                                opener2 = urllib2.build_opener(NoRedirection)
                                opener = urllib2.install_opener(opener2)
                                
                        if 'connection' in m:
                            print '..........................connection//////.',m['connection']
                            from keepalive import HTTPHandler
                            keepalive_handler = HTTPHandler()
                            opener = urllib2.build_opener(keepalive_handler)
                            urllib2.install_opener(opener)
                            
                        #print 'after cookie jar'
                        post=None

                        if 'post' in m:
                            postData=m['post']
                            if '$LiveStreamRecaptcha' in postData:
                                (captcha_challenge,catpcha_word)=processRecaptcha(m['page'])
                                if captcha_challenge:
                                    postData+='recaptcha_challenge_field:'+captcha_challenge+',recaptcha_response_field:'+catpcha_word
                            splitpost=postData.split(',');
                            post={}
                            for p in splitpost:
                                n=p.split(':')[0];
                                v=p.split(':')[1];
                                post[n]=v
                            post = urllib.urlencode(post)

                        if 'rawpost' in m:
                            post=m['rawpost']
                            if '$LiveStreamRecaptcha' in post:
                                (captcha_challenge,catpcha_word)=processRecaptcha(m['page'])
                                if captcha_challenge:
                                   post+='&recaptcha_challenge_field='+captcha_challenge+'&recaptcha_response_field='+catpcha_word


                            

                        if post:
                            response = urllib2.urlopen(req,post)
                        else:
                            response = urllib2.urlopen(req)

                        link = response.read()
                        link=javascriptUnEscape(link)
                        #print link This just print whole webpage in LOG
                        if 'includeheaders' in m:
                            link+=str(response.headers.get('Set-Cookie'))

                        response.close()
                        cachedPages[m['page']] = link
                        #print link
                        #print 'store link for',m['page'],forCookieJarOnly
                        
                        if forCookieJarOnly:
                            return cookieJar# do nothing
                    elif m['page'] and  not m['page'].startswith('http'):
                        if m['page'].startswith('$pyFunction:'):
                            val=doEval(m['page'].split('$pyFunction:')[1],'',cookieJar )
                            if forCookieJarOnly:
                                return cookieJar# do nothing
                            link=val
                        else:
                            link=m['page']
                if '$pyFunction:playmedia(' in m['expre'] or 'ActivateWindow'  in m['expre']   or  any(x in url for x in g_ignoreSetResolved):
                    setresolved=False
                if  '$doregex' in m['expre']:
                    m['expre']=getRegexParsed(regexs, m['expre'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                    
                
                if not m['expre']=='':
                    print 'doing it ',m['expre']
                    if '$LiveStreamCaptcha' in m['expre']:
                        val=askCaptcha(m,link,cookieJar)
                        #print 'url and val',url,val
                        url = url.replace("$doregex[" + k + "]", val)
                    elif m['expre'].startswith('$pyFunction:'):
                        #print 'expeeeeeeeeeeeeeeeeeee',m['expre']
                        val=doEval(m['expre'].split('$pyFunction:')[1],link,cookieJar )
                        if 'ActivateWindow' in m['expre']: return 
                        print 'still hre'
                        print 'url k val',url,k,val

                        url = url.replace("$doregex[" + k + "]", val)
                    else:
                        if not link=='':
                            reg = re.compile(m['expre']).search(link)
                            val=''
                            try:
                                val=reg.group(1).strip()
                            except: traceback.print_exc()
                        else:
                            val=m['expre']
                        if rawPost:
                            print 'rawpost'
                            val=urllib.quote_plus(val)
                        if 'htmlunescape' in m:
                            #val=urllib.unquote_plus(val)
                            import HTMLParser
                            val=HTMLParser.HTMLParser().unescape(val)                     
                        url = url.replace("$doregex[" + k + "]", val)
                        #return val
                else:           
                    url = url.replace("$doregex[" + k + "]",'')
        if '$epoctime$' in url:
            url=url.replace('$epoctime$',getEpocTime())
        if '$epoctime2$' in url:
            url=url.replace('$epoctime2$',getEpocTime2())

        if '$GUID$' in url:
            import uuid
            url=url.replace('$GUID$',str(uuid.uuid1()).upper())
        if '$get_cookies$' in url:
            url=url.replace('$get_cookies$',getCookiesString(cookieJar))   

        if recursiveCall: return url
        print 'final url',url
        if url=="": 
        	return
        else:
        	return url,setresolved

            
        
def getmd5(t):
    import hashlib
    h=hashlib.md5()
    h.update(t)
    return h.hexdigest()

def decrypt_vaughnlive(encrypted):
    retVal=""
    for val in encrypted.split(':'):
        retVal+=chr(int(val.replace("0m0",""))/84/5)
    return retVal

def playmedia(media_url):
    try:
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=media_url )
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    return ''
    
        
def get_saw_rtmp(page_value, referer=None):
    if referer:
        referer=[('Referer',referer)]
    if page_value.startswith("http"):
        page_url=page_value
        page_value= getUrl(page_value,headers=referer)

    str_pattern="(eval\(function\(p,a,c,k,e,(?:r|d).*)"

    reg_res=re.compile(str_pattern).findall(page_value)
    r=""
    if reg_res and len(reg_res)>0:
        for v in reg_res:
            r1=get_unpacked(v)
            r2=re_me(r1,'\'(.*?)\'')
            if 'unescape' in r1:
                r1=urllib.unquote(r2)
            r+=r1+'\n'
        print 'final value is ',r
        
        page_url=re_me(r,'src="(.*?)"')
        
        page_value= getUrl(page_url,headers=referer)

    #print page_value

    rtmp=re_me(page_value,'streamer\'.*?\'(.*?)\'\)')
    playpath=re_me(page_value,'file\',\s\'(.*?)\'')

    
    return rtmp+' playpath='+playpath +' pageUrl='+page_url
    
def get_leton_rtmp(page_value, referer=None):
    if referer:
        referer=[('Referer',referer)]
    if page_value.startswith("http"):
        page_value= getUrl(page_value,headers=referer)
    str_pattern="var a = (.*?);\s*var b = (.*?);\s*var c = (.*?);\s*var d = (.*?);\s*var f = (.*?);\s*var v_part = '(.*?)';"
    reg_res=re.compile(str_pattern).findall(page_value)[0] 

    a,b,c,d,f,v=(reg_res)
    f=int(f)
    a=int(a)/f
    b=int(b)/f
    c=int(c)/f
    d=int(d)/f

    ret= 'rtmp://' + str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d) + v;
    return ret

def createM3uForDash(url,useragent=None):
    str='#EXTM3U'
    str+='\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=361816'
    str+='\n'+url+'&bytes=0-200000'#+'|User-Agent='+useragent
    source_file = os.path.join(profile, 'testfile.m3u')
    str+='\n'
    SaveToFile(source_file,str)
    #return 'C:/Users/shani/Downloads/test.m3u8'
    return source_file

def SaveToFile(file_name,page_data,append=False):
    if append:
        f = open(file_name, 'a')
        f.write(page_data)
        f.close()        
    else:
        f=open(file_name,'wb')
        f.write(page_data)
        f.close()
        return ''
    
def LoadFile(file_name):
	f=open(file_name,'rb')
	d=f.read()
	f.close()
	return d
    
def get_packed_iphonetv_url(page_data):
	import re,base64,urllib; 
	s=page_data
	while 'geh(' in s:
		if s.startswith('lol('): s=s[5:-1]    
#		print 's is ',s
		s=re.compile('"(.*?)"').findall(s)[0]; 
		s=  base64.b64decode(s); 
		s=urllib.unquote(s); 
	print s
	return s



    


def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match





    
def get_unpacked( page_value, regex_for_text='', iterations=1, total_iteration=1):
    try:        
        reg_data=None
        if page_value.startswith("http"):
            page_value= getUrl(page_value)
        print 'page_value',page_value
        if regex_for_text and len(regex_for_text)>0:
            page_value=re.compile(regex_for_text).findall(page_value)[0] #get the js variable
        
        page_value=unpack(page_value,iterations,total_iteration)
    except: traceback.print_exc(file=sys.stdout)
    print 'unpacked',page_value
    if 'sav1live.tv' in page_value:
        page_value=page_value.replace('sav1live.tv','sawlive.tv') #quick fix some bug somewhere
        print 'sav1 unpacked',page_value
    return page_value

def unpack(sJavascript,iteration=1, totaliterations=2  ):
    print 'iteration',iteration
    if sJavascript.startswith('var _0xcb8a='):
        aSplit=sJavascript.split('var _0xcb8a=')
        ss="myarray="+aSplit[1].split("eval(")[0]
        exec(ss)
        a1=62
        c1=int(aSplit[1].split(",62,")[1].split(',')[0])
        p1=myarray[0]
        k1=myarray[3]
        with open('temp file'+str(iteration)+'.js', "wb") as filewriter:
            filewriter.write(str(k1))
        #aa=1/0
    else:

        aSplit = sJavascript.split("rn p}('")
        print aSplit
        
        p1,a1,c1,k1=('','0','0','')
     
        ss="p1,a1,c1,k1=('"+aSplit[1].split(".spli")[0]+')' 
        exec(ss)
    k1=k1.split('|')
    aSplit = aSplit[1].split("))'")
#    print ' p array is ',len(aSplit)
#   print len(aSplit )

    #p=str(aSplit[0]+'))')#.replace("\\","")#.replace('\\\\','\\')

    #print aSplit[1]
    #aSplit = aSplit[1].split(",")
    #print aSplit[0] 
    #a = int(aSplit[1])
    #c = int(aSplit[2])
    #k = aSplit[3].split(".")[0].replace("'", '').split('|')
    #a=int(a)
    #c=int(c)
    
    #p=p.replace('\\', '')
#    print 'p val is ',p[0:100],'............',p[-100:],len(p)
#    print 'p1 val is ',p1[0:100],'............',p1[-100:],len(p1)
    
    #print a,a1
    #print c,a1
    #print 'k val is ',k[-10:],len(k)
#    print 'k1 val is ',k1[-10:],len(k1)
    e = ''
    d = ''#32823

    #sUnpacked = str(__unpack(p, a, c, k, e, d))
    sUnpacked1 = str(__unpack(p1, a1, c1, k1, e, d,iteration))
    
    #print sUnpacked[:200]+'....'+sUnpacked[-100:], len(sUnpacked)
#    print sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
    
    #exec('sUnpacked1="'+sUnpacked1+'"')
    if iteration>=totaliterations:
#        print 'final res',sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
        return sUnpacked1#.replace('\\\\', '\\')
    else:
#        print 'final res for this iteration is',iteration
        return unpack(sUnpacked1,iteration+1)#.replace('\\', ''),iteration)#.replace('\\', '');#unpack(sUnpacked.replace('\\', ''))

def __unpack(p, a, c, k, e, d, iteration,v=1):

    #with open('before file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    while (c >= 1):
        c = c -1
        if (k[c]):
            aa=str(__itoaNew(c, a))
            if v==1:
                p=re.sub('\\b' + aa +'\\b', k[c], p)# THIS IS Bloody slow!
            else:
                p=findAndReplaceWord(p,aa,k[c])

            #p=findAndReplaceWord(p,aa,k[c])

            
    #with open('after file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    return p

#
#function equalavent to re.sub('\\b' + aa +'\\b', k[c], p)
def findAndReplaceWord(source_str, word_to_find,replace_with):
    splits=None
    splits=source_str.split(word_to_find)
    if len(splits)>1:
        new_string=[]
        current_index=0
        for current_split in splits:
            #print 'here',i
            new_string.append(current_split)
            val=word_to_find#by default assume it was wrong to split

            #if its first one and item is blank then check next item is valid or not
            if current_index==len(splits)-1:
                val='' # last one nothing to append normally
            else:
                if len(current_split)==0: #if blank check next one with current split value
                    if ( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_'):# first just just check next
                        val=replace_with
                #not blank, then check current endvalue and next first value
                else:
                    if (splits[current_index][-1].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') and (( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_')):# first just just check next
                        val=replace_with
                        
            new_string.append(val)
            current_index+=1
        #aaaa=1/0
        source_str=''.join(new_string)
    return source_str        

def __itoa(num, radix):
#    print 'num red',num, radix
    result = ""
    if num==0: return '0'
    while num > 0:
        result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
        num /= radix
    return result
	
def __itoaNew(cc, a):
    aa="" if cc < a else __itoaNew(int(cc / a),a) 
    cc = (cc % a)
    bb=chr(cc + 29) if cc> 35 else str(__itoa(cc,36))
    return aa+bb


def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    #print 'cookieString',cookieString
    return cookieString


def saveCookieJar(cookieJar,COOKIEFILE):
	try:
		complete_path=os.path.join(profile,COOKIEFILE)
		cookieJar.save(complete_path,ignore_discard=True)
	except: pass

def getCookieJar(COOKIEFILE):

	cookieJar=None
	if COOKIEFILE:
		try:
			complete_path=os.path.join(profile,COOKIEFILE)
			cookieJar = cookielib.LWPCookieJar()
			cookieJar.load(complete_path,ignore_discard=True)
		except: 
			cookieJar=None
	
	if not cookieJar:
		cookieJar = cookielib.LWPCookieJar()
	
	return cookieJar
    
def doEval(fun_call,page_data,Cookie_Jar):
    ret_val=''
    if functions_dir not in sys.path:
        sys.path.append(functions_dir)
    
    print fun_call
    try:
        py_file='import '+fun_call.split('.')[0]
        print py_file,sys.path
        exec( py_file)
        print 'done'
    except:
        print 'error in import'
        traceback.print_exc(file=sys.stdout)
    print 'ret_val='+fun_call
    exec ('ret_val='+fun_call)
    print ret_val
    #exec('ret_val=1+1')
    return str(ret_val)
    
def processRecaptcha(url):
	html_text=getUrl(url)
	recapChallenge=""
	solution=""
	cap_reg="<script.*?src=\"(.*?recap.*?)\""
	match =re.findall(cap_reg, html_text)
	captcha=False
	captcha_reload_response_chall=None
	solution=None
	
	if match and len(match)>0: #new shiny captcha!
		captcha_url=match[0]
		captcha=True
		
		cap_chall_reg='challenge.*?\'(.*?)\''
		cap_image_reg='\'(.*?)\''
		captcha_script=getUrl(captcha_url)
		recapChallenge=re.findall(cap_chall_reg, captcha_script)[0]
		captcha_reload='http://www.google.com/recaptcha/api/reload?c=';
		captcha_k=captcha_url.split('k=')[1]
		captcha_reload+=recapChallenge+'&k='+captcha_k+'&captcha_k=1&type=image&lang=en-GB'
		captcha_reload_js=getUrl(captcha_reload)
		captcha_reload_response_chall=re.findall(cap_image_reg, captcha_reload_js)[0]
		captcha_image_url='http://www.google.com/recaptcha/api/image?c='+captcha_reload_response_chall
		if not captcha_image_url.startswith("http"):
			captcha_image_url='http://www.google.com/recaptcha/api/'+captcha_image_url
		import random
		n=random.randrange(100,1000,5)
		local_captcha = os.path.join(profile,str(n) +"captcha.img" )
		localFile = open(local_captcha, "wb")
		localFile.write(getUrl(captcha_image_url))
		localFile.close()
		solver = InputWindow(captcha=local_captcha)
		solution = solver.get()
		os.remove(local_captcha)
	return captcha_reload_response_chall ,solution

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):


	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	#opener = urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	if headers:
		for h,hv in headers:
			req.add_header(h,hv)

	response = opener.open(req,post,timeout=timeout)
	link=response.read()
	response.close()
	return link;

def get_decode(str,reg=None):
	if reg:
		str=re.findall(reg, str)[0]
	s1 = urllib.unquote(str[0: len(str)-1]);
	t = '';
	for i in range( len(s1)):
		t += chr(ord(s1[i]) - s1[len(s1)-1]);
	t=urllib.unquote(t)
	print t
	return t

def javascriptUnEscape(str):
	js=re.findall('unescape\(\'(.*?)\'',str)
	print 'js',js
	if (not js==None) and len(js)>0:
		for j in js:
			#print urllib.unquote(j)
			str=str.replace(j ,urllib.unquote(j))
	return str

iid=0
def askCaptcha(m,html_page, cookieJar):
    global iid
    iid+=1
    expre= m['expre']
    page_url = m['page']
    captcha_regex=re.compile('\$LiveStreamCaptcha\[([^\]]*)\]').findall(expre)[0]

    captcha_url=re.compile(captcha_regex).findall(html_page)[0]
    print expre,captcha_regex,captcha_url
    if not captcha_url.startswith("http"):
        page_='http://'+"".join(page_url.split('/')[2:3])
        if captcha_url.startswith("/"):
            captcha_url=page_+captcha_url
        else:
            captcha_url=page_+'/'+captcha_url
    
    local_captcha = os.path.join(profile, str(iid)+"captcha.jpg" )
    localFile = open(local_captcha, "wb")
    print ' c capurl',captcha_url
    req = urllib2.Request(captcha_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    if 'refer' in m:
        req.add_header('Referer', m['refer'])
    if 'agent' in m:
        req.add_header('User-agent', m['agent'])
    if 'setcookie' in m:
        print 'adding cookie',m['setcookie']
        req.add_header('Cookie', m['setcookie'])
        
    #cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    #opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    urllib2.urlopen(req)
    response = urllib2.urlopen(req)

    localFile.write(response.read())
    response.close()
    localFile.close()
    solver = InputWindow(captcha=local_captcha)
    solution = solver.get()
    return solution
    
class InputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,30,624,60,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        time.sleep(2)        
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        self.close()
        return False
    
def getEpocTime():
    import time
    return str(int(time.time()*1000))

def getEpocTime2():
    import time
    return str(int(time.time()))

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param







def urlsolver(url):
    if addon.getSetting('Updatecommonresolvers') == 'true':
        l = os.path.join(home,'genesisresolvers.py')
        if xbmcvfs.exists(l):
            os.remove(l)

        genesis_url = 'http://pastebin.com/raw.php?i=b9wwkSxe'
        th= urllib.urlretrieve(genesis_url,l)
        addon.setSetting('Updatecommonresolvers', 'false')
    try:
        import genesisresolvers
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(CloudTV,Please enable Update Commonresolvers to Play in Settings. - ,10000)")

    resolved=genesisresolvers.get(url).result
    if url == resolved or resolved is None:
        #import
        import urlresolver
        host = urlresolver.HostedMediaFile(url)
        if host:
            resolver = urlresolver.resolve(url)
            resolved = resolver
    if resolved :
        if isinstance(resolved,list):
            for k in resolved:
                quality = addon.getSetting('quality')
                if k['quality'] == 'HD'  :
                    resolver = k['url']
                    break
                elif k['quality'] == 'SD' :
                    resolver = k['url']
                elif k['quality'] == '1080p' and addon.getSetting('1080pquality') == 'true' :
                    resolver = k['url']
                    break
        else:
            resolver = resolved
    return resolver

def play_playlist(name, mu_playlist):
        import urlparse
        if addon.getSetting('ask_playlist_items') == 'true':
            names = []
            for i in mu_playlist:
                d_name=urlparse.urlparse(i).netloc
                if d_name == '':
                    names.append(name)
                else:
                    names.append(d_name)
            dialog = xbmcgui.Dialog()
            index = dialog.select('Choose a video source', names)
            if index >= 0:
                if "&mode=19" in mu_playlist[index]:
                    xbmc.Player().play(urlsolver(mu_playlist[index].replace('&mode=19','')))
                elif "$doregex" in mu_playlist[index] :

                    sepate = mu_playlist[index].split('&regexs=')

                    url,setresolved = getRegexParsed(sepate[1], sepate[0])
                    xbmc.Player().play(url)
                else:
                    url = mu_playlist[index]
                    xbmc.Player().play(url)
        else:
            playlist = xbmc.PlayList(1) # 1 means video
            playlist.clear()
            item = 0
            for i in mu_playlist:
                item += 1
                info = xbmcgui.ListItem('%s) %s' %(str(item),name))
                playlist.add(i, info)
                xbmc.executebuiltin('playlist.playoffset(video,0)')


def download_file(name, url):
        if addon.getSetting('save_location') == "":
            xbmc.executebuiltin("XBMC.Notification('CloudTV','Choose a location to save files.',15000,"+icon+")")
            addon.openSettings()
        params = {'url': url, 'download_path': addon.getSetting('save_location')}
        downloader.download(name, params)
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('CloudTV', 'Do you want to add this file as a source?')
        if ret:
            addSource(os.path.join(addon.getSetting('save_location'), name))


def addDir(name,url,mode,iconimage,fanart,description,genre,date,credits,showcontext=False):
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date, "credits": credits })
        liz.setProperty("Fanart_Image", fanart)

        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

        return ok

 
def search(site_name,search_term=None):
    thumbnail=''
    if os.path.exists(history) == False or addon.getSetting('clearseachhistory')=='true':
        SaveToFile(history,'')
        addon.setSetting("clearseachhistory","false")
    if site_name == 'history' :
        content = LoadFile(history)
        match = re.compile('(.+?):(.*?)(?:\r|\n)').findall(content)

        for name,search_term in match:
            if 'plugin://' in search_term:
                addLink(search_term, name,thumbnail,'','','','','',None,'',total=int(len(match)))
            else:
                addDir(name+':'+search_term,name,26,icon,FANART,'','','','')
    if not search_term:    
        keyboard = xbmc.Keyboard('','Enter Search Term')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        search_term = keyboard.getText()
        if len(search_term) == 0:
            return        
    search_term = search_term.replace(' ','+')
    search_term = search_term.encode('utf-8')
    if 'youtube' in site_name:
        #youtube = youtube#Lana Del Rey
        import _ytplist

        search_res = {}
        search_res = _ytplist.YoUTube('searchYT',youtube=search_term,max_page=4,nosave='nosave')
        total = len(search_res)
        for item in search_res:
            try:
                name = search_res[item]['title']
                date= search_res[item]['date']
                try:
                    description = search_res[item]['desc']
                except Exception:
                    description = 'UNAVAIABLE'

                url = 'plugin://plugin.video.youtube/play/?video_id=' + search_res[item]['url']
                thumbnail ='http://img.youtube.com/vi/'+search_res[item]['url']+'/0.jpg'
                addLink(url, name,thumbnail,'','','','','',None,'',total)
            except Exception:
            	addon_log( 'This item is ignored::')
        page_data = site_name +':'+ search_term + '\n'
        SaveToFile(os.path.join(profile,'history'),page_data,append=True)
    elif 'dmotion' in site_name:
        urlMain = "https://api.dailymotion.com" 
        #youtube = youtube#Lana Del Rey
        import _DMsearch
        familyFilter = str(addon.getSetting('familyFilter'))
        _DMsearch.listVideos(urlMain+"/videos?fields=description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search="+search_term+"&sort=relevance&limit=100&family_filter="+familyFilter+"&localization=en_EN&page=1")
    
        page_data = site_name +':'+ search_term+ '\n'
        SaveToFile(os.path.join(profile,'history'),page_data,append=True)        
    elif 'IMDBidplay' in site_name:
        urlMain = "http://www.omdbapi.com/?t=" 
        url= urlMain+search_term

        headers = dict({'User-Agent':'Mozilla/5.0 (Windows NT 6.3; rv:33.0) Gecko/20100101 Firefox/33.0','Referer': 'http://joker.org/','Accept-Encoding':'gzip, deflate','Content-Type': 'application/json;charset=utf-8','Accept': 'application/json, text/plain, */*'})
    
        r=requests.get(url,headers=headers)
        data = r.json()
        res = data['Response']
        if res == 'True':
            imdbID = data['imdbID']
            name= data['Title'] + data['Released']
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno('Check Movie Title', 'PLAY :: %s ?'%name)
            if ret:
                url = 'plugin://plugin.video.pulsar/movie/'+imdbID+'/play'
                page_data = name +':'+ url+ '\n'
                SaveToFile(history,page_data,append=True)
                return url
        else:
            xbmc.executebuiltin("XBMC.Notification(CloudTV,No IMDB match found ,7000,"+icon+")")
## Lunatixz PseudoTV feature
def ascii(string):
    if isinstance(string, basestring):
        if isinstance(string, unicode):
           string = string.encode('ascii', 'ignore')
    return string
def uni(string, encoding = 'utf-8'):
    if isinstance(string, basestring):
        if not isinstance(string, unicode):
            string = unicode(string, encoding, 'ignore')
    return string
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def sendJSON( command):
    data = ''
    try:
        data = xbmc.executeJSONRPC(uni(command))
    except UnicodeEncodeError:
        data = xbmc.executeJSONRPC(ascii(command))

    return uni(data)


def SetViewThumbnail():
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')
    elif skin_used == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(511)') 
    else:
        xbmc.executebuiltin('Container.SetViewMode(500)')

def SetViewList():
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(511)')
    elif skin_used == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(511)') 
    else:
        xbmc.executebuiltin('Container.SetViewMode(511)')
	
	
def pluginquerybyJSON(url):
    json_query = uni('{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":["thumbnail","title","year","dateadded","fanart","rating","season","episode","studio"]},"id":1}') %url

    json_folder_detail = json.loads(sendJSON(json_query))
    for i in json_folder_detail['result']['files'] :
        url = i['file']
        name = removeNonAscii(i['label'])
        thumbnail = removeNonAscii(i['thumbnail'])
        try:
            fanart = removeNonAscii(i['fanart'])
        except Exception:
            fanart = ''
        try:
            date = i['year']
        except Exception:
            date = ''
        try:
            episode = i['episode']
            season = i['season']
            if episode == -1 or season == -1:
                description = ''
            else:
                description = '[COLOR yellow] S' + str(season)+'[/COLOR][COLOR hotpink] E' + str(episode) +'[/COLOR]'
        except Exception:
            description = ''
        try:
            studio = i['studio']
            if studio:
                description += '\n Studio:[COLOR steelblue] ' + studio[0] + '[/COLOR]'
        except Exception:
            studio = ''

        if i['filetype'] == 'file':
            addLink(url,name,thumbnail,fanart,description,'',date,'',None,'',total=len(json_folder_detail['result']['files']))
            #xbmc.executebuiltin("Container.SetViewMode(500)")

        else:
            addDir(name,url,53,thumbnail,fanart,description,'',date,'')
            #xbmc.executebuiltin("Container.SetViewMode(500)")

def addLink(url,name,iconimage,fanart,description,genre,date,showcontext,playlist,regexs,total,setCookie=""):
        #print 'url,name',url,name
        contextMenu =[]
        try:
            name = name.encode('utf-8')
        except: pass
        ok = True
       
        if regexs: 
            mode = '17'
           
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
        elif  any(x in url for x in resolve_url) and  url.startswith('http'):
            mode = '19'
          
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
        elif url.startswith('magnet:?xt=') or '.torrent' in url:
          
            if '&' in url and not '&amp;' in url :
                url = url.replace('&','&amp;')
            url = 'plugin://plugin.video.pulsar/play?uri=' + url
            mode = '12'
                     
        else: 
            mode = '12'
      
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
        u=sys.argv[0]+"?"
        play_list = False
      
        if playlist:
            if addon.getSetting('add_playlist') == "false":
                u += "url="+urllib.quote_plus(url)+"&mode="+mode
            else:
                u += "mode=13&name=%s&playlist=%s" %(urllib.quote_plus(name), urllib.quote_plus(str(playlist).replace(',','||')))
                name = name + '[COLOR magenta] (' + str(len(playlist)) + ' items )[/COLOR]'
                play_list = True
        else:
            u += "url="+urllib.quote_plus(url)+"&mode="+mode
        if regexs:
            u += "&regexs="+regexs
        if not setCookie == '':
            u += "&setCookie="+urllib.quote_plus(setCookie)
  
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date })
        liz.setProperty("Fanart_Image", fanart)
        
        if (not play_list) and not any(x in url for x in g_ignoreSetResolved):#  (not url.startswith('plugin://plugin.video.f4mTester')):
            if regexs:
                if '$pyFunction:playmedia(' not in urllib.unquote_plus(regexs) and 'notplayable' not in urllib.unquote_plus(regexs)  :
                    #print 'setting isplayable',url, urllib.unquote_plus(regexs),url
                    liz.setProperty('IsPlayable', 'true')
            else:
                liz.setProperty('IsPlayable', 'true')
        else:
            addon_log( 'NOT setting isplayable'+url)
       
        
       
        if not playlist is None:
            if addon.getSetting('add_playlist') == "false":
                playlist_name = name.split(') ')[1]
                contextMenu_ = [
                    ('Play '+playlist_name+' PlayList','XBMC.RunPlugin(%s?mode=13&name=%s&playlist=%s)'
                     %(sys.argv[0], urllib.quote_plus(playlist_name), urllib.quote_plus(str(playlist).replace(',','||'))))
                     ]
                liz.addContextMenuItems(contextMenu_)
        #print 'adding',name
 #       print url,totalitems
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,totalItems=total)
        #print 'added',name
        return ok

def keyboard():
    keyboard = xbmc.Keyboard('', 'Enter URL:', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        url=query
        #urlsolver(url)
        xbmc.Player().play(url)



def playsetresolved(url,name,iconimage,setresolved=True):
    if setresolved:
        liz = xbmcgui.ListItem(name, iconImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    else:
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')      


def AddBvls():
    i=0
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Scanning Bvls2016.sc')
    xmlurl = 'http://dutchsportstreams.com/xml/ds.xml'
    req = urllib2.Request(xmlurl,None)
    response = urllib2.urlopen(req)
    xml = response.read()
    response.close()
    root = ET.fromstring(xml)
    items = root.findall('item')
    for item in items:
        cname = item.find('title').text
        lnk = item.find('url').text
        print cname
        addon_log("streamUrl: "+lnk)
        frameHtml = bitly.OPEN_URL2(lnk, sourceSitebvls, bitly.getUserAgent())
        b64coded = bitly.getBaseEncodedString(frameHtml)
        streamUrl = bitly.getStreamUrl(b64coded)
        addon_log("streamUrl: "+streamUrl)
        i+=1
        progress.update( 20+ (i*20), "", "Finding links.. stream%d"%i, "" )

        if (bitly.getResponse(streamUrl)) :
            color = 'green'
        else :
            color = 'red'
        if streamUrl[-4:] == '.flv' :
            streamUrl = bitly.VeetleId(streamUrl)
        
        addDir('[COLOR '+color+']Bvls2016.sc - ' + cname + '[/COLOR]',streamUrl,103,icon,fanart,'','','','',)
    progress.close()



def Catfeed2all():
        addDir('Football' ,'football.html',105,icon ,  FANART,'','','','')
        addDir('AM. Football' ,'american-football.html',105,icon ,  FANART,'','','','')
        addDir('Basketball' ,'basketball.html',105,icon ,  FANART,'','','','')
        addDir('Boxing/WWE/UFC' ,'boxing-wwe-ufc.html',105,icon ,  FANART,'','','','')
        addDir('Rugby' ,'rugby.html',105,icon ,  FANART,'','','','')
        addDir('Ice Hockey' ,'ice-hockey.html',105,icon ,  FANART,'','','','')
        addDir('Tennis' ,'tennis.html',105,icon ,  FANART,'','','','')
        addDir('Motorsport' ,'motosport.html',105,icon ,  FANART,'','','','')
        addDir('Golf' ,'golf.html',105,icon ,  FANART,'','','','')
        addDir('Baseball' ,'baseball.html',105,icon ,  FANART,'','','','')
        addDir('Darts' ,'darts.html',105,icon ,  FANART,'','','','')
        addDir('Snooker' ,'snooker.html',105,icon ,  FANART,'','','','')
        addDir('Handball' ,'handball.html',105,icon ,  FANART,'','','','')
        addDir('Cricket' ,'cricket.html',105,icon ,  FANART,'','','','')
        addDir('Aussie Rules' ,'aussie-rules.html',105,icon ,  FANART,'','','','')
        addDir('Others' ,'others.html',105,icon ,  FANART,'','','','')
	return



def Addthefeed2all(url):
    pagecontent=bitly.OPEN_URL2('http://www.feed2allnow.eu/type/'+url,'http://www.feed2allnow.eu/',bitly.getUserAgent())
    match1=re.compile('<span>\s*([^<]+)</span>\s*([^<]+) </a> </h3>.+?\s*.+?href=\'(.*?)\'',re.DOTALL).findall(pagecontent)
    for dsstime,dssgame,dsslink in match1:
        dsslink = 'http://www.feed2allnow.eu' + dsslink
        
        addDir('[B][COLOR yellow3]'+ dssgame+ '[/COLOR][/B]',dsslink,99,icon ,  FANART,'','','','')
    #except:
        #pass
    try:
        pagecontent=bitly.OPEN_URL2('http://www.feed2allnow.eu/type/'+url,'http://www.feed2allnow.eu/',bitly.getUserAgent())
        match1=re.compile('<span class="matchtime">([^<]+)</span> </span>\s*([^<]+)</a> </h3>.+?\s*.+?href=\'([^<]+)\'',re.DOTALL).findall(pagecontent)
        for dsstime,dssgame,dsslink in match1:
            try:
                dt = datetime.strptime(dsstime, "%H:%M")
                dsstime = str(dt.hour+1).rjust(2,'0') + ':' + str(dt.minute).rjust(2,'0')
            except :
                pass        
            dsslink = 'http://www.feed2allnow.eu' + dsslink
            addDir('[B][COLOR yellow3]''('+dsstime+') '+ dssgame+ '[/COLOR][/B]',dsslink,99,icon ,  FANART,'','','','')
    except:
        pass

def Addwiz():
    pagecontent = bitly.OPEN_URL2('http://www.wiz1.net/lag10_home.php','http://www.wiz1.net/',bitly.getUserAgent())
    match = re.compile(r'(\d{2}:\d{2}) <font color="#5185C9"><b>([^<]+)</b></font> ([^<]+)<a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(pagecontent)
    for dsstime, sport, game, dsslink in match:
        try:
            dt = datetime.strptime(dsstime, "%H:%M")
            dsstime = str(dt.hour+0).rjust(2,'0') + ':' + str(dt.minute).rjust(2,'0')
        except :
            pass
        #if 'Eredivisie' in sport or 'Belgium' in sport:
            #addDir('[B][COLOR yellow3]''('+dsstime+') '+ game+ '[/COLOR][/B]',dsslink,21,icon ,  FANART,'','','','',isItFolder=False)
        #if 'Netherlands' in game or 'Belgium' in game:
        addDir('[B][COLOR yellow3]''('+sport+') '+'('+dsstime+') '+ game+ '[/COLOR][/B]',dsslink,99,icon ,  FANART,'','','','')
        



def Addgoatd():
    dssport=''
    goatpage = bitly.OPEN_URL2('http://goatd.net/','http://goatd.net/',bitly.getUserAgent())
    match = re.compile(r'<b>ET</b></td>\s+<td[^<]+><img src="([^"]+)".*?href="([^"]+)"[^>]+>([^<]+)<.*?<b>([^<]+)<.*?<b>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(goatpage)
    for img, dsslink, dssgame, dsstime, dsszone in match:
        try:
            sport = re.compile('http://.*?/.*?/.*?/.*?/.*?/.*?/(.*?).gif', re.DOTALL | re.IGNORECASE).findall(img)
            if sport > 0 :
                for dssport in sport:
                    dssport = re.sub("[^A-Za-z]", "", dssport) 
        except:
            pass
        dsslink = 'http://goatd.net/' + dsslink
        addDir('[B][COLOR yellow3]''('+dssport+') '+'('+dsstime+') '+dsszone+' '+ dssgame+ '[/COLOR][/B]',dsslink,99,icon ,  FANART,'','','','')

def Colored(text = '', colorid = '', isBold = False):
    if colorid == 'ZM':
        color = 'FF11b500'
    elif colorid == 'EB':
        color = 'FFe37101'
    elif colorid == 'bold':
        return '[B]' + text + '[/B]'
    else:
        color = colorid
        
    if isBold == True:
        text = '[B]' + text + '[/B]'
    return '[COLOR ' + color + ']' + text + '[/COLOR]'	

def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)
        
def AddSports365Channels(url=None):
    errored=True
    import live365
    #addDir(Colored("All times in local timezone.",'red') ,"" ,0 ,"","","","","","")		#name,url,mode,icon
    videos=live365.getLinks()
    for nm,link,active in videos:
        if active:
           
            addDir(Colored(nm  ,'ZM'),link,98,icon ,  FANART,'','','','')
        else:
            addDir("[N/A]"+Colored(nm ,'blue') ,'',0,icon ,  FANART,'','','','')
        errored=False
    
    #if errored:
       #if RefreshResources([('live365.py','https:#')]):
            #dialog = xbmcgui.Dialog()
            #ok = dialog.ok('XBMC', 'No Links, so updated files dyamically, try again, just in case!')           
            #print 'Updated files'
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def wizhdsports():
    html = bitly.OPEN_URL2('http://wizhdsports.com/watch/live-football-streaming.html','http://wizhdsports.com/',bitly.getUserAgent())
    _regex_encodedstring = re.compile("<div class=\"box\">(.*?)<div style=\"clear:both;\"></div>" , re.DOTALL)
    html = _regex_encodedstring.search(html).group(1)
    events = re.findall('<li class=\"channelLink\" onclick=\"location=\'.+?\';\"><a href=\"(.*?)\">(.*?)</a></li>',html)
    for lnk, cname in events:
        print lnk
        print cname
        addDir('[B][COLOR grey]'+ cname+ '[/COLOR][/B]',lnk,99,icon ,  FANART,'','','','')
    html = bitly.OPEN_URL2('http://wizhdsports.com/index.html','http://wizhdsports.com/',bitly.getUserAgent())
    events = re.findall('<span id=\"startTime.*?\">\s*(.*?)</span> -\s*<span id=\".*?\">\s*.*?</span>\s*</div>\s*<div class=\"name\">(.*?)</div>',html)
    print events
    for dsstime, cname in events:
        lnk = cname.replace(' ', '-')
        _regex_encodedstring = re.compile('/watch/'+lnk+'/(.*?).html' , re.DOTALL)
        lnkend = _regex_encodedstring.search(html).group(1)
        lnk = 'http://wizhdsports.com/watch/'+lnk+'/'+lnkend+'.html'
        addDir('[B][COLOR yellow3]('+dsstime+')'+ cname+ '[/COLOR][/B]',lnk,99,icon ,  FANART,'','','','')


def playBvls(name,url):
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#    print "playing stream name: " + str(name)
    xbmc.executebuiltin('XBMC.Notification(Visit www.bvls2016.sc , And keep Streams Alive !! ,10000,'+icon+')')
    xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( url, listitem)



def playSports365(url):
    #print ('playSports365')
    import live365
    urlToPlay=live365.selectMatch(url)
    if urlToPlay and len(urlToPlay)>0:
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    #    print   "playing stream name: " + str(name)
        xbmc.executebuiltin('XBMC.Notification(Visit sport365.live , And keep Streams Alive !! ,10000,'+icon+')')
        xbmc.Player(  ).play( urlToPlay, listitem)  
    else:
        if RefreshResources([('live365.py','https://raw.githubusercontent.com/dutchsportstreams/DSS/master/plugin.video.cloudtv/live365.py')]):
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('XBMC', 'No Links, so updated files dyamically, try again, just in case!')           
            print 'Updated files'
    return	 


def resolver(url):
    import liveresolver
    resolved = liveresolver.resolve(url)
    xbmc.Player().play(resolved)

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
    pass

params=get_params()

url=None
name=None
mode=None
playlist=None
iconimage=None
fanart=FANART
playlist=None
fav_mode=None
regexs=None

try:
    url=urllib.unquote_plus(params["url"]).decode('utf-8')
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    playlist=eval(urllib.unquote_plus(params["playlist"]).replace('||',','))
except:
    pass
try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    regexs=params["regexs"]
except:
    pass


addon_log("Mode: "+str(mode))
if not url is None:
    addon_log("URL: "+str(url.encode('utf-8')))
addon_log("Name: "+str(name))
   
if mode==None:
    addon_log("Index")
    DCTVIndex()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==1:
    addon_log("getData")
    getData(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==2:
    addon_log("getChannelItems")
    getChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==3:
    addon_log("getSubChannelItems")
    getSubChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==4:
        Play()

elif mode==6:
    addon_log("getData")
    getData(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


elif mode==7:
    addon_log("addSource")
    addSource(url)

elif mode==8:
    addon_log("rmSource")
    rmSource(name)

elif mode==9:
    addon_log("download_file")
    download_file(name, url)

elif mode==10:
    CatIndex(url)

elif mode==11:
    addon_log("addSource")
    addSource(url)

elif mode==12:
    addon_log("setResolvedUrl")
    if not url.startswith("plugin://plugin") or not any(x in url for x in g_ignoreSetResolved):#not url.startswith("plugin://plugin.video.f4mTester") :
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    else:
        print 'Not setting setResolvedUrl'
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')


elif mode==13:
    addon_log("play_playlist")
    play_playlist(name, playlist)



elif mode==15:
    addon_log("browse_xml_database")
    get_xml_database(url, True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))



elif mode==17:
    addon_log("getRegexParsed")
    url,setresolved = getRegexParsed(regexs, url)
    if url:
        playsetresolved(url,name,iconimage,setresolved)
    else:
        xbmc.executebuiltin("XBMC.Notification(CloudTV,Failed to extract regex. - "+"this"+",4000,"+icon+")")

elif mode==19:
	addon_log("Genesiscommonresolvers")
	playsetresolved (urlsolver(url),name,iconimage,True)	


elif mode==25:
    addon_log("YouTube/DMotion")
    search(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==26:
    addon_log("YouTube/DMotion From Search History")
    name = name.split(':')
    search(url,search_term=name[1])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==27:
    addon_log("Using IMDB id to play in Pulsar")
    pulsarIMDB=search(url)
    xbmc.Player().play(pulsarIMDB) 
elif mode==30:
    GetSublinks(name,url,iconimage,fanart)
	
elif mode==40:
    SearchChannels()
    SetViewThumbnail()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==45:
    Privacy_Policy()

elif mode==46:
    Nieuws()

elif mode==47:
    keyboard()

elif mode==48:
    MyIndex()
    
	
elif mode==53:
    addon_log("Requesting JSON-RPC Items")
    pluginquerybyJSON(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==98:
    url=base64.b64decode(url)
    playSports365(url.split('Sports365:')[1])
    
    
elif mode==99:
    resolver(url)
    
    
elif mode==100:
    IndexSport()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==101:
    IndexDSS()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==102:
    AddBvls()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==103:
    playBvls(name,url)

elif mode==104:
    Catfeed2all()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==105:
    Addthefeed2all(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==106:
    Addwiz()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==107:
    Addgoatd()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==108:
    AddSports365Channels()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==109:
    wizhdsports()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    