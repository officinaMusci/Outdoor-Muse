import os
import unittest

from entities.partner import Partner, TEST_PARTNER
from entities.location import Location


class TestPartner(unittest.TestCase):
    '''Tests the Partner object'''

    def delete_db(self):
        '''Delete test database file'''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


    def setUp(self):
        '''Initialize the test'''
        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_partner.db'
        )

        self.delete_db()
        
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"


    def test_create(self):
        '''Tests the creation in the database'''
        partner = Partner.from_dict(TEST_PARTNER)
        partner_id = partner.save()
        retrieved_partner = Partner.get_from_id(partner_id)

        self.assertEqual(partner, retrieved_partner)


    def test_update(self):
        '''Tests the update in the database'''
        partner = Partner.from_dict(TEST_PARTNER)
        partner_id = partner.save()

        partner_2 = Partner.from_dict(TEST_PARTNER)
        partner_id_2 = partner_2.save()

        partner_2.name = 100000
        partner_2.location = Location.from_dict({
            'lat': 46.204391,
            'lng': 6.143158
        })

        partner_2.save()

        retrieved_partner = Partner.get_from_id(partner_id)
        retrieved_partner_2 = Partner.get_from_id(partner_id_2)

        self.assertNotEqual(retrieved_partner, retrieved_partner_2)


    def test_delete(self):
        '''Tests the deletion from the database'''
        partner = Partner.from_dict(TEST_PARTNER)
        partner_id = partner.save()

        partner_2 = Partner.from_dict(TEST_PARTNER)
        partner_id_2 = partner_2.save()
        partner_2.delete()

        retrieved_partner = Partner.get_from_id(partner_id)
        retrieved_partner_2 = Partner.get_from_id(partner_id_2)

        self.assertIsNotNone(retrieved_partner)
        self.assertIsNone(retrieved_partner_2)


    def tearDown(self):
        '''Finalise the test removing the test database file'''
        self.delete_db()