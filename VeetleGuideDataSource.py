from datetime import date
import urllib2
import simplejson as json
import datetime
import Logger
import VeetleCache
import VeetleData

URL_VEETLE = 'http://www.veetle.com'
URL_VEETLE_STREAM_URL = URL_VEETLE + '/index.php/channel/ajaxStreamLocation/%s/flash'

URL_VEETLE_GUIDE_LOAD_CHANNELS = "http://veetleguide.appspot.com/load-channels"
URL_VEETLE_GUIDE_LOAD_SCHEDULE = "http://veetleguide.appspot.com/load-schedule"

CACHE_DURATION_IN_MINUTES = 10

log = Logger.Logger("VeetleGuideDataSource")

class VeetleGuideDataSource:

    def __init__(self):
        self.cache = VeetleCache.VeetleCache(CACHE_DURATION_IN_MINUTES)

    def loadChannels(self):

        channels = []

        try:

            jsonChannels = self.cache.get("channels")

            if jsonChannels is None or len(jsonChannels) == 0:
                log.notice("Refreshing channel data from: %s" % (URL_VEETLE_GUIDE_LOAD_CHANNELS))
                response = urllib2.urlopen(URL_VEETLE_GUIDE_LOAD_CHANNELS)
                jsonChannels = response.read().decode("utf-8")
                self.cache.set("channels", jsonChannels)
            else:
                log.debug("Using cached channel data")

            jsonChannels = json.loads(jsonChannels)

            for jsonChannel in jsonChannels:
                channels.append(parseChannel(jsonChannel))

        except Exception, e:
            log.error('Error loading channel list: ' + repr(e))

        return channels

    def loadSchedule(self):

        schedule = []

        try:

            jsonSchedule = self.cache.get("schedule")

            if jsonSchedule is None or len(jsonSchedule) == 0:
                log.notice("Refreshing schedule data from: %s" %(URL_VEETLE_GUIDE_LOAD_SCHEDULE))
                response = urllib2.urlopen(URL_VEETLE_GUIDE_LOAD_SCHEDULE)
                jsonSchedule = response.read().decode("utf-8")
                self.cache.set("schedule", jsonSchedule)
            else:
                log.debug("Using cached schedule data")

            jsonSchedule = json.loads(jsonSchedule)

            for jsonScheduleItem in jsonSchedule:
                schedule.append(parseScheduleItem(jsonScheduleItem))

        except Exception, e:
            log.error('Error loading schedule: ' + repr(e))

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
    channel.userName = str(jsonChannel['userName'])
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
