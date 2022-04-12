from random import randrange, sample # TEMP

import flask
import flask_jwt_extended as flask_jwt

from utils import app
from entities.query import Query
from entities.user import User
from entities.place import Place
from entities.partner import Partner
from entities.solution import Solution
from factories.solution_factory import SolutionFactory


blueprint = flask.Blueprint(
    'search',
    __name__,
    url_prefix='/search'
)


@blueprint.route('', methods=['POST'])
@flask_jwt.jwt_required(optional=True)
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
    


    # TEMP
    solution_factory = SolutionFactory(query)
    solution_factory._solutions = Solution.get_all()
    solution_factory._filter_by_trip_duration()
    solution_factory._filter_by_forecasts()
    response = []
    for solution in solution_factory._solutions[:query.max_results]:
        solution.place = Place.get_from_id(solution.place_id)
        response.append(solution)
    return app.response(response)



    solution_factory = SolutionFactory(query)
    results = solution_factory.execute()

    response = []
    for solution in results:
        solution.save()

        solution.place = Place.get_from_id(solution.place_id)
        response.append(solution)
    
    return app.response(response)


@blueprint.route('/save', methods=['POST'])
@app.jwt_required()
def save():
    '''The API route to save a query.
    
    RETURNS:
        response: The JSON response containing the saved query.
    
    RAISES:
        400 response: Bad request if the search query has not been found.
    '''
    
    request = app.get_request()

    user = User.get_from_access_token()
    if user:
        request.update({'user_id': user.id})
    else:
        return app.response(True)

    query = Query.from_dict(request)
    query.favorited = True
    query.save()
    
    return app.response(True)


@blueprint.route('/favorites', methods=['GET'])
@app.jwt_required()
def favorites():
    '''The API route to get the user's favorites.
    
    RETURNS:
        response: The JSON response containing the user's favorites.
    
    RAISES:
        400 response: Bad request if the search query has not been found.
    '''
    
    user = User.get_from_access_token()
    if user:
        queries = Query.get_all({'user_id': user.id, 'favorited': True})
        return app.response(queries)
    else:
        return app.response([])



@blueprint.route('/select/<solution_id>', methods=['POST', 'DELETE'])
@app.jwt_required()
def select(solution_id):
    '''The API route to select or unselect a solution.
    
    RETURNS:
        response: The JSON response containing the solution (True if deleted).
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
    '''
    solution = Solution.get_from_id(solution_id)
    
    user = User.get_from_access_token()
    if user:
        if flask.request.method == 'POST':
            solution.user_id = user.id
            solution.save()
            
            return app.response(True)
        
        elif flask.request.method == 'DELETE':
            solution.user_id = None
            solution.save()
            
            return app.response(True)
    
    return app.response(False)


@blueprint.route('/fetch', methods=['GET'])
@app.jwt_required()
def fetch():
    '''The API route to fetch the selected solutions.
    
    RETURNS:
        response: The JSON response containing the solutions.
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
    '''
    user = User.get_from_access_token()
    if user:
        solutions = Solution.get_all({'user_id': user.id})
        response = []
        for solution in solutions:
            solution.place = Place.get_from_id(solution.place_id)
            response.append(solution)
        
        response = sorted(response, key=lambda solution: solution.interval.start, reverse=True)
        
        return app.response(response)
    
    return app.response([])