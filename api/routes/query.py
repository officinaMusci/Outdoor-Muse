import flask

from utils import app
from entities.query import Query


blueprint = flask.Blueprint(
    'queries',
    __name__,
    url_prefix='/queries'
)


@blueprint.route('', methods=['GET'])
@app.jwt_required(roles=['admin'])
def get():
    '''The API route to get the queries.
    
    RETURNS:
        response: The JSON response containing the queries.
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the query hasn't one of the required roles.
    '''
    request = app.get_request()

    queries = Query.get_all(request)
    return app.response(queries)


@blueprint.route('/<query_id>', methods=['GET'])
@app.jwt_required(roles=['admin'])
def get_one(query_id):
    '''The API route to get a query.
    
    RETURNS:
        response: The JSON response containing the query.
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the query hasn't one of the required roles.
    '''
    query = Query.get_from_id(query_id)

    if flask.request.method == 'GET':
        return app.response(query)