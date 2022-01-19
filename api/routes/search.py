import flask

from utils import app
from entities.query import Query
from factories.solution_factory import SolutionFactory


blueprint = flask.Blueprint(
    'search',
    __name__,
    url_prefix='/search'
)


@blueprint.route('/', methods=['POST'])
@app.jwt_required()
def execute():
    '''The API route to get query results.
    
    RETURNS:
        response: The JSON response containing the results.
    
    RAISES:
        400 response: Bad request if the search query has not been found.
    '''
    
    request = app.get_request()

    query = Query.from_dict(request)
    query.save()
    solution_factory = SolutionFactory(query)
    results = solution_factory.execute()
    
    return app.response(results)