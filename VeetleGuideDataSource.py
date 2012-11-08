from datetime import date
import urllib2
import simplejson as json
import datetime
import VeetleData

URL_VEETLE = 'http://www.veetle.com'
URL_VEETLE_STREAM_URL = URL_VEETLE + '/index.php/channel/ajaxStreamLocation/%s/flash'

URL_VEETLE_GUIDE_LOAD_CHANNELS = "http://veetleguide.appspot.com/load-channels"
URL_VEETLE_GUIDE_LOAD_CHANNEL = "http://veetleguide.appspot.com/load-channel?id="
URL_VEETLE_GUIDE_LOAD_SCHEDULE = "http://veetleguide.appspot.com/load-schedule"

try:
    import StorageServer
except:
    import StorageServerDummy as StorageServer


class VeetleGuideDataSource:

    def __init__(self):
        self.cache = StorageServer.StorageServer("plugin.video.veetle", 1)

    def loadChannels(self):

        channels = []

        try:

            jsonChannels = self.cache.get("channels")

            if jsonChannels is None or len(jsonChannels) == 0:
                response = urllib2.urlopen(URL_VEETLE_GUIDE_LOAD_CHANNELS)
                jsonChannels = response.read().decode("utf-8")
                self.cache.set("channels", jsonChannels)

            jsonChannels = json.loads(jsonChannels)

            for jsonChannel in jsonChannels:
                channels.append(parseChannel(jsonChannel))

        except ValueError, error_info:
            print 'Error loading channel list: ' + repr(error_info)

        return channels

    def loadSchedule(self):

        schedule = []

        try:

            jsonSchedule = self.cache.get("schedule")

            if jsonSchedule is None or len(jsonSchedule) == 0:
                response = urllib2.urlopen(URL_VEETLE_GUIDE_LOAD_SCHEDULE)
                jsonSchedule = response.read().decode("utf-8")
                self.cache.set("schedule", jsonSchedule)

            jsonSchedule = json.loads(jsonSchedule)

            for jsonScheduleItem in jsonSchedule:
                schedule.append(parseScheduleItem(jsonScheduleItem))

        except ValueError, error_info:
            print 'Error loading schedule: ' + repr(error_info)

        return schedule

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
    channel.popularityIndex = jsonChannel['popularityIndex']
    channel.bitRate = jsonChannel['bitRate']
    channel.logoUrl = jsonChannel['logoUrl']

    if 'currentItem' in jsonChannel:

        jsonScheduleItem = jsonChannel['currentItem']

        channel.currentItem = parseScheduleItem(jsonScheduleItem)

    return channel

def parseScheduleItem(jsonScheduleItem):

    scheduleItem = VeetleData.VeetleScheduleItem()
    scheduleItem.title = jsonScheduleItem['title']
    scheduleItem.description = jsonScheduleItem['description']
    scheduleItem.duration = datetime.timedelta(milliseconds=jsonScheduleItem['duration'])
    scheduleItem.startTime = datetime.datetime.fromtimestamp(jsonScheduleItem['startTime'] / 1000.0)
    scheduleItem.channelId = jsonScheduleItem['channelId']

    return scheduleItem
