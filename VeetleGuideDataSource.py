import urllib2
import simplejson as json
import VeetleData

__author__ = 'sissbruecker'

URL_VEETLE = 'http://www.veetle.com'
URL_STREAM = URL_VEETLE + '/index.php/channel/ajaxStreamLocation/%s/flash'

try:
    import StorageServer
except:
    import StorageServerDummy as StorageServer


class VeetleGuideDataSource:

    def __init__(self):
        self.loadChannelsUrl = "http://veetleguide.appspot.com/load-channels"
        self.loadChannelUrl = "http://veetleguide.appspot.com/load-channel?id="
        self.cache = StorageServer.StorageServer("veetle", 1)
        self.cache.dbg = True

    def loadChannels(self):

        channels = []

        try:

            jsonData = self.cache.get("channels")

            if jsonData is None or len(jsonData) == 0:
                print("Loading channels...")
                response = urllib2.urlopen(self.loadChannelsUrl)
                jsonData = response.read()
                print("Response type: " + str(type(jsonData)))
                jsonData = jsonData.decode("utf-8")
                self.cache.set("channels", jsonData)

            jsonChannels = json.loads(jsonData)

            for jsonChannel in jsonChannels:
                channels.append(parseChannel(jsonChannel))

        except ValueError, error_info:
            print 'Error loading channel list: ' + repr(error_info)

        return channels

    def loadChannelStreamUrl(self, channelId):

        url = URL_STREAM % channelId

        response = urllib2.urlopen(url)
        jsonContent = json.loads(response.read())

        return jsonContent['payload']


def parseChannel(jsonChannel):

    channel = VeetleData.VeetleChannel()
    channel.channelId = jsonChannel['channelId']
    channel.title = jsonChannel['title']
    channel.description = jsonChannel['description']
    channel.categoryId = str(jsonChannel['categoryId'])
    channel.smallLogoUrl = jsonChannel['logoUrl']
    channel.largeLogoUrl = jsonChannel['logoUrl']

    if 'currentItem' in jsonChannel:

        jsonScheduleItem = jsonChannel['currentItem']
        jsonPlayListItem = jsonScheduleItem['playListItem']

        currentItem = VeetleData.VeetleScheduleItem()
        currentItem.title = jsonPlayListItem['title']
        currentItem.description = jsonPlayListItem['description']
        currentItem.duration = jsonPlayListItem['duration']
        currentItem.startTime = jsonScheduleItem['startTime']

        channel.currentItem = currentItem

    return channel
