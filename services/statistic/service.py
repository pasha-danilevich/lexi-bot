from mock.statistic.service import StatisticMockService


class StatisticService(StatisticMockService):
    def __str__(self):
        return self.__class__.__name__
