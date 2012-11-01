import VeetleData
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import base64

__settings__ = xbmcaddon.Addon(id='plugin.video.veetle')
__language__ = __settings__.getLocalizedString

URL_VIEW_CHANNEL = '?channel='
URL_VIEW_CATEGORY = '?category='

URL_AKAMAI_PROXY = 'http://127.0.0.1:64653/veetle/%s'

class VeetleViews:

    def __init__(self, pluginUrl, pluginHandle, dataSource):
        self.baseUrl = pluginUrl
        self.pluginHandle = pluginHandle
        self.dataSource = dataSource

    def buildChannelUrl(self, channel):
        return self.baseUrl + URL_VIEW_CHANNEL + channel.channelId

    def buildCategoryUrl(self, categoryId):
        return self.baseUrl + URL_VIEW_CATEGORY + str(categoryId)

    def createChannelListItem(self, channel):

        listItem = xbmcgui.ListItem(
            channel.title,
            iconImage=channel.logoUrl,
            thumbnailImage=channel.logoUrl)

        infoLabels = {'title': channel.title}
        listItem.setInfo('video', infoLabels)
        listItem.setProperty('IsPlayable', 'true')

        return listItem

    def renderHome(self, queryUrl):

        for category in VeetleData.Categories:

            listItem = xbmcgui.ListItem(
                category.title,
                iconImage='',
                thumbnailImage='')

            xbmcplugin.addDirectoryItem(
                    self.pluginHandle,
                    self.buildCategoryUrl(category.id),
                    listItem,
                    isFolder=True)

        xbmcplugin.endOfDirectory(self.pluginHandle)

    def renderCategory(self, queryUrl):

        categoryId = queryUrl[len(URL_VIEW_CATEGORY):].strip()

        # Load the channel list
        channels = self.dataSource.loadChannels()

        # Filter channel for specified category
        channels = [channel for channel in channels if channel.categoryId == categoryId]

        for channel in channels:

            url = self.buildChannelUrl(channel)
            listItem = self.createChannelListItem(channel)

            xbmcplugin.addDirectoryItem(
                self.pluginHandle,
                url,
                listItem,
                isFolder=False,
                totalItems=len(channels))

        xbmcplugin.endOfDirectory(self.pluginHandle)

    def renderChannel(self, queryUrl):

        #Play a stream with the given channel id
        channelId = queryUrl[len(URL_VIEW_CHANNEL):].strip()
        channelStreamUrl = self.dataSource.loadChannelStreamUrl(channelId)
        VIDb64 = base64.encodestring(channelStreamUrl).replace('\n', '')
        fullUrl = URL_AKAMAI_PROXY % VIDb64

        if channelStreamUrl:
            xbmcplugin.setResolvedUrl(
                self.pluginHandle,
                True,
                xbmcgui.ListItem(path=fullUrl))
        else:
            xbmcplugin.setResolvedUrl(
                self.pluginHandle,
                False,
                xbmcgui.ListItem())

            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__language__(30000), __language__(30001))

    def renderUrl(self, queryUrl):

        if queryUrl.startswith(URL_VIEW_CHANNEL):
            self.renderChannel(queryUrl)
            return

        if queryUrl.startswith(URL_VIEW_CATEGORY):
            self.renderCategory(queryUrl)
            return

        self.renderHome(queryUrl)