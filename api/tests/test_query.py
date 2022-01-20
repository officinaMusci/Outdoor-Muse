import os
from random import randrange
import unittest

from entities.query import Query, QueryPlaceRow, QueryPartnerRow
from entities.user import User
from entities.place import Place
from entities.partner import Partner


class TestQuery(unittest.TestCase):
    '''Tests the Query object'''

    def delete_db(self):
        '''Delete test database file'''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


    def create_query_with_relations(self):
        user = User.generate_random()
        user_id = user.save()

        query = Query.generate_random()
        query.user_id = user_id
        query_id = query.save()

        place = Place.generate_random()
        place_id = place.save()
        query.associate_place_row(place_id=place_id)
        
        partner = Partner.generate_random()
        partner_id = partner.save()
        query.associate_partner_row(partner_id=partner_id)

        return Query.get_from_id(query_id)


    def setUp(self):
        '''Initialize the test'''
        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_query.sqlite'
        )

        self.delete_db()
        
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"


    def test_create(self):
        '''Tests the creation in the database'''
        query = Query.generate_random()
        query_id = query.save()
        retrieved_query = Query.get_from_id(query_id)

        self.assertEqual(query, retrieved_query)
    

    def test_relations(self):
        '''Tests the relations in the database'''
        query = self.create_query_with_relations()

        retrieved_user = User.get_from_id(query.user_id)
        self.assertIsNotNone(retrieved_user)

        retrieved_place = Place.get_from_id(query.get_place_ids()[0])
        self.assertIsNotNone(retrieved_place)

        retrieved_partner = Partner.get_from_id(query.get_partner_ids()[0])
        self.assertIsNotNone(retrieved_partner)

        # On user deletion, the query should be anonymous
        retrieved_user.delete()
        self.assertIsNotNone(Query.get_from_id(query.id))

        # On place deletion, the association should be deleted
        retrieved_place.delete()
        self.assertListEqual(query.get_place_ids(), [])
        
        # On partner deletion, the association should be deleted
        retrieved_partner.delete()
        self.assertListEqual(query.get_partner_ids(), [])
        
        # On query deletion, the associations should be deleted
        query = self.create_query_with_relations()
        query.delete()
        self.assertListEqual(query.get_place_ids(), [])
        self.assertListEqual(query.get_partner_ids(), [])


    def test_update(self):
        '''Tests the update in the database'''
        query = Query.generate_random()
        query_id = query.save()

        query_2 = Query.generate_random()
        query_id_2 = query_2.save()

        query_2.radius = Query.generate_random().radius
        query_2.max_results = Query.generate_random().max_results

        query_2.save()

        retrieved_query = Query.get_from_id(query_id)
        retrieved_query_2 = Query.get_from_id(query_id_2)

        self.assertNotEqual(retrieved_query, retrieved_query_2)


    def test_delete(self):
        '''Tests the deletion from the database'''
        query = Query.generate_random()
        query_id = query.save()

        query_2 = Query.generate_random()
        query_id_2 = query_2.save()
        query_2.delete()

        retrieved_query = Query.get_from_id(query_id)
        retrieved_query_2 = Query.get_from_id(query_id_2)

        self.assertIsNotNone(retrieved_query)
        self.assertIsNone(retrieved_query_2)


    def tearDown(self):
        '''Finalise the test removing the test database file'''
        self.delete_db()