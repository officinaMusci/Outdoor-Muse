import flask

from utils import app
from entities.solution import Solution
from entities.place import Place


blueprint = flask.Blueprint(
    'solutions',
    __name__,
    url_prefix='/solutions'
)


@blueprint.route('', methods=['GET', 'POST'])
@app.jwt_required(roles=['admin'])
def get():
    '''The API route to get or create the solutions.
    
    RETURNS:
        response: The JSON response containing the solutions or the created solution.
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the solution hasn't one of the required roles.
    '''
    request = app.get_request()

    if flask.request.method == 'GET':
        solutions = Solution.get_all(request)
        return app.response(solutions)
    
    elif flask.request.method == 'POST':
        solution = Solution.from_dict(request)
        solution.save()
        return app.response(solution)


@blueprint.route('/<solution_id>', methods=['GET', 'DELETE', 'PUT'])
@app.jwt_required()
def get_one(solution_id):
    '''The API route to get, delete or update a solution.
    
    RETURNS:
        response: The JSON response containing the solution (True if deleted).
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the solution hasn't one of the required roles.
    '''
    solution = Solution.get_from_id(solution_id)

    if flask.request.method == 'GET':
        solution.place = Place.get_from_id(solution.place_id)
        return app.response(solution)
    
    elif flask.request.method == 'DELETE':
        return app.response(solution.delete())
    
    elif flask.request.method == 'PUT':
        request = app.get_request()

        updated_solution = Solution.from_dict(request)
        updated_solution.id = solution_id
        updated_solution.save()
        
        return app.response(updated_solution)