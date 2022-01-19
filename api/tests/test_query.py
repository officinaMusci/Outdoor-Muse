import os
import unittest

from entities.query import Query, TEST_QUERY


class TestQuery(unittest.TestCase):
    '''Tests the Query object'''

    def delete_db(self):
        '''Delete test database file'''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


    def setUp(self):
        '''Initialize the test'''
        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_query.db'
        )

        self.delete_db()
        
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"


    def test_create(self):
        '''Tests the creation in the database'''
        query = Query.from_dict(TEST_QUERY)
        query_id = query.save()
        retrieved_query = Query.get_from_id(query_id)

        self.assertEqual(query, retrieved_query)


    def test_update(self):
        '''Tests the update in the database'''
        query = Query.from_dict(TEST_QUERY)
        query_id = query.save()

        query_2 = Query.from_dict(TEST_QUERY)
        query_id_2 = query_2.save()

        query_2.radius = 100000
        query_2.max_results = 10

        query_2.save()

        retrieved_query = Query.get_from_id(query_id)
        retrieved_query_2 = Query.get_from_id(query_id_2)

        self.assertNotEqual(retrieved_query, retrieved_query_2)


    def test_delete(self):
        '''Tests the deletion from the database'''
        query = Query.from_dict(TEST_QUERY)
        query_id = query.save()

        query_2 = Query.from_dict(TEST_QUERY)
        query_id_2 = query_2.save()
        query_2.delete()

        retrieved_query = Query.get_from_id(query_id)
        retrieved_query_2 = Query.get_from_id(query_id_2)

        self.assertIsNotNone(retrieved_query)
        self.assertIsNone(retrieved_query_2)


    def tearDown(self):
        '''Finalise the test removing the test database file'''
        self.delete_db()