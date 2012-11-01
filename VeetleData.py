__author__ = 'sasch_000'

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

        self.logoUrl = ''

        self.currentItem = None


class VeetleScheduleItem:

    def __init__(self):

        self.title = ''
        self.description = ''
        self.duration = 0
        self.startTime = 0

CategoryAll = VeetleCategory('0', 'All')
CategoryAnimation = VeetleCategory('60', 'Animation')
CategoryComedy = VeetleCategory('50', 'Comedy')
CategoryEducation = VeetleCategory('90', 'Education')
CategoryGaming = VeetleCategory('40', 'Gaming')
CategoryMobile = VeetleCategory('110', 'Mobile')
CategoryEntertainment = VeetleCategory('10', 'Entertainment')
CategoryShows = VeetleCategory('20', 'Shows')
CategorySports = VeetleCategory('80', 'Sports')
CategoryMusic = VeetleCategory('70', 'Music')
CategoryNews = VeetleCategory('30', 'News')
CategoryReligion = VeetleCategory('100', 'Religion')

Categories = [
    CategoryAll,
    CategoryAnimation,
    CategoryComedy,
    CategoryEducation,
    CategoryGaming,
    CategoryMobile,
    CategoryEntertainment,
    CategoryShows,
    CategorySports,
    CategoryMusic,
    CategoryNews,
    CategoryReligion
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
