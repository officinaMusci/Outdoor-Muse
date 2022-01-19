import os
import unittest

from entities.place import Place, TEST_PLACE


class TestPlace(unittest.TestCase):
    '''Tests the Place object'''

    def delete_db(self):
        '''Delete test database file'''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


    def setUp(self):
        '''Initialize the test'''
        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_place.db'
        )

        self.delete_db()
        
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"


    def test_create(self):
        '''Tests the creation in the database'''
        place = Place.from_dict(TEST_PLACE)
        place_id = place.save()
        retrieved_place = Place.get_from_id(place_id)

        self.assertEqual(place, retrieved_place)


    def test_update(self):
        '''Tests the update in the database'''
        place = Place.from_dict(TEST_PLACE)
        place_id = place.save()

        place_2 = Place.from_dict(TEST_PLACE)
        place_id_2 = place_2.save()

        place_2.distance = 100000 
        place_2.difficulty = 10

        place_2.save()

        retrieved_place = Place.get_from_id(place_id)
        retrieved_place_2 = Place.get_from_id(place_id_2)

        self.assertNotEqual(retrieved_place, retrieved_place_2)


    def test_delete(self):
        '''Tests the deletion from the database'''
        place = Place.from_dict(TEST_PLACE)
        place_id = place.save()

        place_2 = Place.from_dict(TEST_PLACE)
        place_id_2 = place_2.save()
        place_2.delete()

        retrieved_place = Place.get_from_id(place_id)
        retrieved_place_2 = Place.get_from_id(place_id_2)

        self.assertIsNotNone(retrieved_place)
        self.assertIsNone(retrieved_place_2)


    def tearDown(self):
        '''Finalise the test removing the test database file'''
        self.delete_db()