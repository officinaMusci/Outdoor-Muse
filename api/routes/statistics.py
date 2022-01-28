import flask

from utils import app
from entities.user import User
from entities.place import Place
from entities.partner import Partner
from entities.query import Query
from entities.review import Review


blueprint = flask.Blueprint(
    'statistics',
    __name__,
    url_prefix='/statistics'
)


@blueprint.route('/overview', methods=['GET'])
@app.jwt_required(roles=['admin'])
def overview():
    '''The API route to get statistics overview.
    
    RETURNS:
        response: The JSON response containing the statistics.
    
    RAISES:
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the review hasn't one of the required roles.
    '''

    users = {
        'total_count': User.get_count({'role': 'user'}),
        'confirmed_count': User.get_count({'role': 'user', 'confirmed': True})
    }

    queries = {
        'total_count': Query.get_count(),
        'anonymous_count': Query.get_count({'user_id': None})
    }

    places = {
        'total_count': Place.get_count()
    }

    partners = {
        'total_count': Partner.get_count()
    }

    reviews = {
        'total_count': Review.get_count()
    }

    return app.response({
        'users': users,
        'partners': partners,
        'places': places,
        'queries': queries,
        'reviews': reviews
    })


@blueprint.route('/over-time', methods=['GET'])
@app.jwt_required(roles=['admin'])
def over_time():
    '''The API route to get entity based statistics.
    
    RETURNS:
        response: The JSON response containing the statistics.
    
    RAISES:
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the review hasn't one of the required roles.
    '''

    def create_over_time(entity_class):
        '''Create a series showing entity growing over time'''
        over_time = []
        records = entity_class.get_all()
        
        records.sort(key=lambda record: record.created)
        for record in records:
            over_time.append({
                'count': len(over_time) + 1,
                'datetime': record.created
            })
        
        return over_time
    
    result = {
        'users': create_over_time(User),
        'partners': create_over_time(Query),
        'places': create_over_time(Place),
        'queries': create_over_time(Partner),
        'reviews': create_over_time(Review)
    }
    
    return app.response(result)