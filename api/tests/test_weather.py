import unittest

from entities.query import Query
from services import weather


class TestWeather(unittest.TestCase):
    '''Tests the weather service'''

    def setUp(self):
        '''Initialize the test'''
        self.query = Query.generate_random()

    def test_get_forecasts(self):
        '''Tests the weather daily forecasts'''
        query = self.query
        weather.get_daily_forecasts(
            location=query.location,
            interval=query.interval
        )