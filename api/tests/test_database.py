import os
import unittest

from . import resources
from services import database

from entities.query import Query
from entities.place import Place


class TestDatabase(unittest.TestCase):
    '''Tests the database'''

    def delete_db(self):
        ''''''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def setUp(self):
        '''Initialize the test'''
        self.query = Query.from_dict(resources.QUERY_DICT)
        self.place = Place.from_dict(resources.PLACE_DICT)

        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test.db'
        )
        self.delete_db()
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"

    def test_query_table(self):
        '''Tests the query registration in the database'''
        query = self.query
        
        query_row_id = query.store_row()
        reconverted_query = Query.from_row_id(query_row_id)

        self.assertEqual(query, reconverted_query)

    def test_place_table(self):
        '''Tests the place registration in the database'''
        place = self.place
        
        place_row_id = place.store_row()
        reconverted_place = Place.from_row_id(place_row_id)

        self.assertEqual(place, reconverted_place)
    
    def tearDown(self):
        '''Finalise the test'''
        self.delete_db()