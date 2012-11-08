import urllib2
import simplejson as json
import VeetleData

URL_VEETLE = 'http://www.veetle.com'
URL_VEETLE_STREAM_URL = URL_VEETLE + '/index.php/channel/ajaxStreamLocation/%s/flash'

URL_VEETLE_GUIDE_LOAD_CHANNELS = "http://veetleguide.appspot.com/load-channels"
URL_VEETLE_GUIDE_LOAD_CHANNEL = "http://veetleguide.appspot.com/load-channel?id="

try:
    import StorageServer
except:
    import StorageServerDummy as StorageServer


class VeetleGuideDataSource:

    def __init__(self):
        self.cache = StorageServer.StorageServer("veetle", 1)

    def loadChannels(self):

        channels = []

        try:

            jsonData = self.cache.get("channels")

            if jsonData is None or len(jsonData) == 0:
                response = urllib2.urlopen(URL_VEETLE_GUIDE_LOAD_CHANNELS)
                jsonData = response.read().decode("utf-8")
                self.cache.set("channels", jsonData)

            jsonChannels = json.loads(jsonData)

            for jsonChannel in jsonChannels:
                channels.append(parseChannel(jsonChannel))

        except ValueError, error_info:
            print 'Error loading channel list: ' + repr(error_info)

        return channels

    def loadChannelStreamUrl(self, channelId):

        url = URL_VEETLE_STREAM_URL % channelId

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

        currentItem = VeetleData.VeetleScheduleItem()
        currentItem.title = jsonScheduleItem['title']
        currentItem.description = jsonScheduleItem['description']
        currentItem.duration = jsonScheduleItem['duration']
        currentItem.startTime = jsonScheduleItem['startTime']

        channel.currentItem = currentItem

    return channel
