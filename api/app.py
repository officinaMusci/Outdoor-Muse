import os
import traceback

import flask
import flask_jwt_extended as flask_jwt
import flask_cors
from dotenv import load_dotenv

import routes
from utils.json_encoder import CustomJSONEncoder


def response(result=None, error=None):
    '''Compose the standard app response.
    
    ARGS:
        results: The results of the request.
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
    request = flask.request.get_json()
    
    if (
        len(required_keys)
        and not all(k in request for k in required_keys)
    ):
        flask.abort(400)
    
    return request


def create_app():
    '''The Flask app factory'''
    app = flask.Flask(__name__)
    
    flask_jwt.JWTManager(app)
    flask_cors.CORS(app)

    load_dotenv()
    app.config.from_mapping(
        ENV=os.getenv('ENV'),
        SECRET_KEY=os.getenv('SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
    )

    app.json_encoder = CustomJSONEncoder
    
    app.register_error_handler(Exception, error)
    app.register_blueprint(routes.root.blueprint)
    app.register_blueprint(routes.auth.blueprint)
    app.register_blueprint(routes.search.blueprint)

    return app