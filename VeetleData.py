class VeetleCategory:

    def __init__(self, id, title):
        self.id = id
        self.title = title

class VeetleChannel:

    def __init__(self):

        self.channelId = 0
        self.title = ''
        self.description = ''
        self.categoryId = ''

        self.popularityIndex = 0
        self.bitRate = 0

        self.logoUrl = ''

        self.currentItem = None


class VeetleScheduleItem:

    def __init__(self):

        self.title = ''
        self.description = ''
        self.duration = 0
        self.startTime = 0

CategoryAll = VeetleCategory('0', 'All')
CategoryEntertainment = VeetleCategory('10', 'Entertainment')
CategoryShows = VeetleCategory('20', 'Shows')
CategoryAnimation = VeetleCategory('60', 'Animation')
CategorySports = VeetleCategory('80', 'Sports')
CategoryComedy = VeetleCategory('50', 'Comedy')
CategoryMusic = VeetleCategory('70', 'Music')
CategoryEducation = VeetleCategory('90', 'Education')
CategoryGaming = VeetleCategory('40', 'Gaming')
CategoryNews = VeetleCategory('30', 'News')
CategoryReligion = VeetleCategory('100', 'Religion')
CategoryMobile = VeetleCategory('110', 'Mobile')

Categories = [
    CategoryAll,
    CategoryEntertainment,
    CategoryShows,
    CategoryAnimation,
    CategorySports,
    CategoryComedy,
    CategoryMusic,
    CategoryEducation,
    CategoryGaming,
    CategoryNews,
    CategoryReligion,
    CategoryMobile
    ]

CategoryMap = {
    CategoryAll.id: CategoryAll,
    CategoryAnimation.id: CategoryAnimation,
    CategoryComedy.id: CategoryComedy,
    CategoryEducation.id: CategoryEducation,
    CategoryGaming.id: CategoryGaming,
    CategoryMobile.id: CategoryMobile,
    CategoryEntertainment.id: CategoryEntertainment,
    CategoryShows.id: CategoryShows,
    CategorySports.id: CategorySports,
    CategoryMusic.id: CategoryMusic,
    CategoryNews.id: CategoryNews,
    CategoryReligion.id: CategoryReligion
}
