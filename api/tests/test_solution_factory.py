import unittest

from entities.query import Query
from factories.solution_factory import SolutionFactory


class TestSolutionFactory(unittest.TestCase):
    '''Tests the solution factory'''

    def setUp(self):
        '''Initialize the test'''
        self.query = Query.generate_random()

    def test_execute(self):
        '''Tests the solution factory execution'''
        query = self.query
        SolutionFactory(query).execute()