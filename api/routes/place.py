import flask

from utils import app
from entities.place import Place


blueprint = flask.Blueprint(
    'places',
    __name__,
    url_prefix='/places'
)


@blueprint.route('', methods=['GET', 'POST'])
@app.jwt_required(roles=['admin'])
def get():
    '''The API route to get or create the places.
    
    RETURNS:
        response: The JSON response containing the places or the created place.
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the place hasn't one of the required roles.
    '''
    request = app.get_request()

    if flask.request.method == 'GET':
        places = Place.get_all(request)
        return app.response(places)
    
    elif flask.request.method == 'POST':
        place = Place.from_dict(request)
        place.save()
        return app.response(place)


@blueprint.route('/<place_id>', methods=['GET', 'DELETE', 'PUT'])
@app.jwt_required(roles=['admin'])
def get_one(place_id):
    '''The API route to get, delete or update a place.
    
    RETURNS:
        response: The JSON response containing the place (True if deleted).
    
    RAISES:
        400 response: Bad request if some request keys have not been found.
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the place hasn't one of the required roles.
    '''
    place = Place.get_from_id(place_id)

    if flask.request.method == 'GET':
        return app.response(place)
    
    elif flask.request.method == 'DELETE':
        return app.response(place.delete())
    
    elif flask.request.method == 'PUT':
        request = app.get_request()

        updated_place = Place.from_dict(request)
        updated_place.id = place_id
        updated_place.save()
        
        return app.response(updated_place)