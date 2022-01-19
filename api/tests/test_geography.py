import unittest

from entities.query import Query
from entities.place import Place
from services import geography


class TestGeography(unittest.TestCase):
    '''Tests the geography service'''

    def test_geography_fetch_places_nearby(self):
        '''Tests the geography nearby search'''
        query = Query.generate_random()
        geography.fetch_places_nearby(
            location=query.location,
            types=query.types,
            radius=query.radius
        )
    
    def test_geography_fetch_itinerary(self):
        '''Tests the geography itinerary search'''
        query = Query.generate_random()
        place = Place.generate_random()
        geography.fetch_itinerary(
            start_location=query.location,
            end_location=place.location,
            departure_time=query.interval.start
        )