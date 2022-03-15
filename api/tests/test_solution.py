import os
from random import randrange
import unittest

from entities.solution import Solution
from entities.relations import SolutionPartnerRow
from entities.query import Query
from entities.partner import Partner
from entities.user import User


class TestSolution(unittest.TestCase):
    '''Tests the Solution object'''

    def delete_db(self):
        '''Delete test database file'''
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    

    def create_solution_with_relations(self):
        user = User.generate_random()
        user_id = user.save()

        query = Query.generate_random()
        query_id = query.save()

        solution = Solution.generate_random()
        solution.query_id = query_id
        solution.user_id = user_id
        solution_id = solution.save()
        
        partner = Partner.generate_random()
        partner_id = partner.save()
        solution.associate_partner_row(partner_id=partner_id)

        return Solution.get_from_id(solution_id)
    

    def setUp(self):
        '''Initialize the test'''
        self.db_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_solution.sqlite'
        )

        self.delete_db()
        
        os.environ['DB_ENGINE'] = f"sqlite:///{self.db_path}"
    

    def test_create(self):
        '''Tests the creation in the database'''
        solution = Solution.generate_random()
        solution_id = solution.save()
        retrieved_solution = Solution.get_from_id(solution_id)

        self.assertEqual(solution, retrieved_solution)
    

    def test_relations(self):
        '''Tests the relations in the database'''
        solution = self.create_solution_with_relations()

        retrieved_query = Query.get_from_id(solution.query_id)
        self.assertIsNotNone(retrieved_query)

        retrieved_user = User.get_from_id(solution.user_id)
        self.assertIsNotNone(retrieved_user)

        retrieved_partner = Partner.get_from_id(solution.get_partner_ids()[0])
        self.assertIsNotNone(retrieved_partner)

        # On query deletion, the ssolution should be unlinked
        retrieved_query.delete()
        self.assertIsNotNone(Solution.get_from_id(solution.id))

        # On user deletion, the solution should be deleted
        retrieved_user.delete()
        self.assertIsNone(Solution.get_from_id(solution.id))
        
        # On partner deletion, the association should be deleted
        retrieved_partner.delete()
        self.assertListEqual(solution.get_partner_ids(), [])
        
        # On solution deletion, the associations should be deleted
        solution = self.create_solution_with_relations()
        solution.delete()
        self.assertListEqual(solution.get_partner_ids(), [])


    def test_update(self):
        '''Tests the update in the database'''
        solution = Solution.generate_random()
        solution_id = solution.save()

        solution_2 = Solution.generate_random()
        solution_id_2 = solution_2.save()

        solution_2.start_location = Solution.generate_random().start_location
        solution_2.interval = Solution.generate_random().interval

        solution_2.save()

        etrieved_ssolution = Solution.get_from_id(solution_id)
        etrieved_ssolution_2 = Solution.get_from_id(solution_id_2)

        self.assertNotEqual(etrieved_ssolution, etrieved_ssolution_2)


    def test_delete(self):
        '''Tests the deletion from the database'''
        solution = Solution.generate_random()
        solution_id = solution.save()

        solution_2 = Solution.generate_random()
        solution_id_2 = solution_2.save()
        solution_2.delete()

        etrieved_ssolution = Solution.get_from_id(solution_id)
        etrieved_ssolution_2 = Solution.get_from_id(solution_id_2)

        self.assertIsNotNone(etrieved_ssolution)
        self.assertIsNone(etrieved_ssolution_2)


    def tearDown(self):
        '''Finalise the test removing the test database file'''
        self.delete_db()