import unittest

from entities.query import Query
from factories.solution_factory import SolutionFactory

from . import resources


class TestSolutionFactory(unittest.TestCase):
    '''Tests the solution factory'''

    def setUp(self):
        '''Initialize the test'''
        self.query = Query.from_dict(resources.QUERY_DICT)

    def test_execute(self):
        '''Tests the solution factory execution'''
        query = self.query
        SolutionFactory(query).execute()