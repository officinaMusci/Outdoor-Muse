import os

import flask
import flask_jwt_extended as flask_jwt
import flask_cors
from dotenv import load_dotenv

from routes import root, auth, users, places, partners, queries, reviews, search
from utils.json_encoder import CustomJSONEncoder
from utils.app import error


# Avoid not found error
from entities.user import User
from entities.place import Place
from entities.partner import Partner
from entities.query import Query
from entities.relations import QueryPlaceRow, QueryPartnerRow
from entities.review import ReviewRow


def create_app():
    '''The Flask app factory'''
    app = flask.Flask(__name__)
    
    flask_cors.CORS(app)
    flask_jwt.JWTManager(app)

    load_dotenv()
    app.config.from_mapping(
        ENV=os.getenv('FLASK_ENV'),
        SECRET_KEY=os.getenv('SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    )

    app.json_encoder = CustomJSONEncoder
    
    app.register_error_handler(Exception, error)
    app.register_blueprint(root.blueprint)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(users.blueprint)
    app.register_blueprint(places.blueprint)
    app.register_blueprint(partners.blueprint)
    app.register_blueprint(queries.blueprint)
    app.register_blueprint(reviews.blueprint)
    app.register_blueprint(search.blueprint)

    return app