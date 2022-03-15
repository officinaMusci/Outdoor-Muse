import flask

from utils import app
from entities.user import User


blueprint = flask.Blueprint(
    'users',
    __name__,
    url_prefix='/users'
)


@blueprint.route('', methods=['GET', 'POST'])
@app.jwt_required(roles=['admin'])
def get():
    '''The API route to get or create the users.
    
    RETURNS:
        response: The JSON response containing the users or the created user.
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the user hasn't one of the required roles.
    '''
    request = app.get_request()

    if flask.request.method == 'GET':
        users = User.get_all(request)
        return app.response(users)
    
    elif flask.request.method == 'POST':
        user = User.from_dict(request)
        user.save()
        return app.response(user)


@blueprint.route('/<user_id>', methods=['GET', 'DELETE', 'PUT'])
@app.jwt_required()
def get_one(user_id):
    '''The API route to get, delete or update a user.
    
    RETURNS:
        response: The JSON response containing the user (True if deleted).
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the user hasn't one of the required roles.
    '''
    user_id = int(user_id)

    current_user = User.get_from_access_token()
    user = User.get_from_id(user_id)

    if current_user.id != user_id and current_user.role != 'admin':
        flask.abort(403)

    if flask.request.method == 'GET':
        return app.response(user)
    
    elif flask.request.method == 'DELETE':
        return app.response(user.delete())
    
    elif flask.request.method == 'PUT':
        request = app.get_request()

        updated_user = User.from_dict(request)
        updated_user.id = user_id
        updated_user.save()
        
        return app.response(updated_user)