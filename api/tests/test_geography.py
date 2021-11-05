import unittest

from entities.query import Query
from entities.place import Place
from services import geography

from . import resources


class TestGeography(unittest.TestCase):
    '''Tests the geography service'''

    def setUp(self):
        '''Initialize the test'''
        self.query = Query.from_dict(resources.QUERY_DICT)
        self.place = Place.from_dict(resources.PLACE_DICT)

    def test_geography_fetch_places_nearby(self):
        '''Tests the geography nearby search'''
        query = self.query
        geography.fetch_places_nearby(
            location=query.location,
            place_type=query.place_type,
            radius=query.radius
        )
    
    def test_geography_fetch_itinerary(self):
        '''Tests the geography itinerary search'''
        query = self.query
        place = self.place
        geography.fetch_itinerary(
            start_location=query.location,
            end_location=place.location,
            departure_time=query.interval.start
        )