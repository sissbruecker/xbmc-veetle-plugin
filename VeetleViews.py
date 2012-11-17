import Logger
import VeetleData
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import base64

__settings__ = xbmcaddon.Addon(id='plugin.video.veetle')
__language__ = __settings__.getLocalizedString

URL_VIEW_CHANNEL = '?channel='
URL_VIEW_CATEGORY = '?category='
URL_VIEW_CATEGORIES = '?categories'
URL_VIEW_SCHEDULE = '?schedule'
URL_VIEW_SEARCH = '?search'

URL_AKAMAI_PROXY = 'http://127.0.0.1:64653/veetle/%s'

log = Logger.Logger("VeetleViews")

class VeetleViews:

    def __init__(self, pluginUrl, pluginHandle, dataSource):
        self.baseUrl = pluginUrl
        self.pluginHandle = pluginHandle
        self.dataSource = dataSource

    def buildChannelUrl(self, channelId):
        return self.baseUrl + URL_VIEW_CHANNEL + channelId

    def buildCategoryUrl(self, categoryId):
        return self.baseUrl + URL_VIEW_CATEGORY + str(categoryId)

    def createChannelListItem(self, channel, scheduleItems):

        channelDisplayTitle = channel.title

        if channel.currentItem:
            channelDisplayTitle += ' ([COLOR=blue]%s[/COLOR])' %channel.currentItem.title

        listItem = xbmcgui.ListItem(
            channelDisplayTitle,
            iconImage=channel.logoUrl,
            thumbnailImage=channel.logoUrl)

        infoLabels = {
            'title': channel.title,
            'director': channel.userName,
            'genre': VeetleData.CategoryMap[channel.categoryId].title,
            'tagline': channel.description,
            'plot': channel.createScheduleSummary(scheduleItems),
        }

        listItem.setInfo('video', infoLabels)
        listItem.setProperty('IsPlayable', 'true')

        return listItem

    def createScheduleListItem(self, scheduleItem):

        displayTitle = scheduleItem.label()

        listItem = xbmcgui.ListItem(
            displayTitle)

        infoLabels = {'title': scheduleItem.title}
        listItem.setInfo('video', infoLabels)
        listItem.setProperty('IsPlayable', 'true')

        return listItem

    def renderHome(self, queryUrl):

        categoriesListItem = xbmcgui.ListItem(
            'Categories',
            iconImage='',
            thumbnailImage='')

        xbmcplugin.addDirectoryItem(
                self.pluginHandle,
                self.baseUrl + URL_VIEW_CATEGORIES,
                categoriesListItem,
                isFolder=True)

        categoriesListItem = xbmcgui.ListItem(
            'Schedule',
            iconImage='',
            thumbnailImage='')

        xbmcplugin.addDirectoryItem(
                self.pluginHandle,
                self.baseUrl + URL_VIEW_SCHEDULE,
                categoriesListItem,
                isFolder=True)

        xbmcplugin.endOfDirectory(self.pluginHandle)

    def renderCategories(self, queryUrl):

        # Load the channel list
        channels = self.dataSource.loadChannels()

        for category in VeetleData.Categories:

            # Get channel count for category
            channelCount = len(channels) if category.id == VeetleData.CategoryAll.id else len([channel for channel in channels if channel.categoryId == category.id])

            listItem = xbmcgui.ListItem(
                category.title + (' ([COLOR=blue]%s[/COLOR])' % str(channelCount)),
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
        scheduleItems = self.dataSource.loadSchedule()

        # Filter channel for specified category
        channels = channels if categoryId == VeetleData.CategoryAll.id else [channel for channel in channels if channel.categoryId == categoryId]

        # Sort channels by popularity
        channels = sorted(channels, key=lambda channel: channel.popularityIndex, reverse=True)

        for channel in channels:

            url = self.buildChannelUrl(channel.channelId)
            listItem = self.createChannelListItem(channel, scheduleItems)

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

    def renderSchedule(self, queryUrl):

        # Load the schedule list
        schedule = self.dataSource.loadSchedule()

        for scheduleItem in schedule:

            url = self.buildChannelUrl(scheduleItem.channelId)
            listItem = self.createScheduleListItem(scheduleItem)

            xbmcplugin.addDirectoryItem(
                self.pluginHandle,
                url,
                listItem,
                isFolder=False)

        xbmcplugin.endOfDirectory(self.pluginHandle)

    def renderUrl(self, queryUrl):

        log.debug("Rendering URL: %s%s" % (self.baseUrl, queryUrl))

        if queryUrl.startswith(URL_VIEW_CHANNEL):
            self.renderChannel(queryUrl)
            return

        if queryUrl.startswith(URL_VIEW_CATEGORIES):
            self.renderCategories(queryUrl)
            return

        if queryUrl.startswith(URL_VIEW_CATEGORY):
            self.renderCategory(queryUrl)
            return

        if queryUrl.startswith(URL_VIEW_SCHEDULE):
            self.renderSchedule(queryUrl)
            return

        self.renderHome(queryUrl)