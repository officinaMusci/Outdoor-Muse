from factories.solution_factory import SolutionFactory
from entities.query import Query


def execute_query(request_dict):
    '''Executes the search query and get results.

    ARGS:
        request_dict: The dictionary containing the search query.
    
    RETURNS:
        results: The search query results.
    '''

    query = Query.from_dict(request_dict)
    query.store_row()
    solution_factory = SolutionFactory(query)
    results = solution_factory.execute()

    return results