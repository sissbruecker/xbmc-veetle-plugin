import urllib2
import xbmc, xbmcaddon, xbmcplugin, xbmcgui

addon = xbmcaddon.Addon()
akamaiProxyServer = xbmc.translatePath(addon.getAddonInfo('path') + "/akamaiSecureHD.py")

def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/13.0')
    response = urllib2.urlopen(req, timeout=30)
    link = response.read()
    response.close()
    return link

def run():
    try:
        getUrl("http://127.0.0.1:64653/version")
        proxyIsRunning = True
    except:
        proxyIsRunning = False
    if not proxyIsRunning:
        xbmc.executebuiltin('RunScript(' + akamaiProxyServer + ')')