import traceback
import functools

import flask
import flask_jwt_extended as flask_jwt

from entities.user import User


def response(result=[], error=None):
    '''Compose the standard app response.
    
    ARGS:
        result: The result of the request.
        error: The error given by the request.
    RETURNS:
        response: The JSON response.
    '''
    app = flask.current_app
    is_dev = app.config['ENV'] == 'development'
    
    code = 200

    if error:
        code = error.code if hasattr(error, 'code') else 500

        error = {
            'type': type(error).__name__,
            'message': str(error),
        }

        if is_dev:
            error['traceback'] = traceback.format_exc()
            error['code'] = code

    return flask.make_response(
        flask.jsonify({
            'result': result,
            'error': error
        }),
        code,
        {'Content-Type': 'application/json'}
    )


def error(e):
    '''The handler for all app errors.
    
    ARGS:
        e: The error raised.
    RETURNS:
        response: The JSON response for the error.
    '''
    return response(None, e)


def get_request(required_keys:list=[]) -> dict:
    '''Get the request and optionnaly checks if it contains the required keys.
    
    ARGS:
        required_keys: a list containing the required keys.
    RETURNS:
        request: the JSON request.
    '''
    if flask.request.method == 'GET':
        request = flask.request.args.to_dict()
        
    else:
        request = flask.request.get_json()
    
    request_keys = list(request.keys())

    if (
        len(required_keys)
        and not all(k in request_keys for k in required_keys)
    ):
        flask.abort(400)
    
    return request


def jwt_required(roles=[]):
    '''Check if the current user has the required role'''
    
    def decorator(route):
        @functools.wraps(route)
        @flask_jwt.jwt_required()
        def wrapped_route(**kwargs):
            user = User.get_from_access_token()

            if not user:
                flask.abort(401)
            
            if len(roles) and user.role not in roles:
                flask.abort(403)

            if 'user' in kwargs.keys():
                return route(user=user, **kwargs)
            else:
                return route(**kwargs)
        
        return wrapped_route
    return decorator