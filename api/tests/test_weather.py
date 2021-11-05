import unittest

from entities.query import Query
from services import weather

from . import resources


class TestWeather(unittest.TestCase):
    '''Tests the weather service'''

    def setUp(self):
        '''Initialize the test'''
        self.query = Query.from_dict(resources.QUERY_DICT)

    def test_get_forecasts(self):
        '''Tests the weather daily forecasts'''
        query = self.query
        weather.get_daily_forecasts(
            location=query.location,
            interval=query.interval
        )