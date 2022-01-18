import unittest

from entities.query import Query, TEST_QUERY
from factories.solution_factory import SolutionFactory


class TestSolutionFactory(unittest.TestCase):
    '''Tests the solution factory'''

    def setUp(self):
        '''Initialize the test'''
        self.query = Query.from_dict(TEST_QUERY)

    def test_execute(self):
        '''Tests the solution factory execution'''
        query = self.query
        SolutionFactory(query).execute()