import os

import flask
import flask_jwt_extended as flask_jwt
import flask_cors
from dotenv import load_dotenv

from entities.user import User
from routes import root, auth, search, users
from utils.json_encoder import CustomJSONEncoder
from utils.app import error


def create_app():
    '''The Flask app factory'''
    app = flask.Flask(__name__)
    
    flask_jwt.JWTManager(app)
    flask_cors.CORS(app)

    load_dotenv()
    app.config.from_mapping(
        ENV=os.getenv('FLASK_ENV'),
        SECRET_KEY=os.getenv('SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
    )

    app.json_encoder = CustomJSONEncoder
    
    app.register_error_handler(Exception, error)
    app.register_blueprint(root.blueprint)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(search.blueprint)
    app.register_blueprint(users.blueprint)

    return app