import statistics
from datetime import timedelta

import flask

from utils import app
from entities.user import User
from entities.place import Place
from entities.partner import Partner
from entities.query import Query
from entities.review import Review
from services import weather


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


@blueprint.route('/all', methods=['GET'])
@app.jwt_required(roles=['admin'])
def all():
    '''The API route to get entity based statistics.
    
    RETURNS:
        response: The JSON response containing the statistics.
    
    RAISES:
        401 response: Unauthorized if the request has not the JWT.
        403 response: Forbidden if the review hasn't one of the required roles.
    '''

    all_queries = Query.get_all()
    weather_counts = {
        'clear': 0,
        'clouds': 0,
        'snow': 0,
        'rain': 0,
        'thunderstorm': 0,
        'other': 0
    }
    
    for query in all_queries:
        for name, ids in weather.id_groups.items():
            if not set(query.weather_ids).isdisjoint(ids):
                weather_counts[name] += 1
    

    radius_mean = statistics.mean([q.radius for q in all_queries])
    max_travel_mean = timedelta(seconds=statistics.mean([
        q.max_travel.total_seconds() for q in all_queries
    ]))
    max_walk_mean = timedelta(seconds=statistics.mean([
        q.max_walk.total_seconds() for q in all_queries
    ]))


    def create_over_time(entity_class):
        '''Create a series showing entity growing over time'''
        over_time = []
        records = entity_class.get_all()
        
        records.sort(key=lambda record: record.created)
        for record in records:
            over_time.append([
                record.created,
                len(over_time) + 1
            ])
        
        return over_time
    
    result = {
        'weather_counts': [[k, v] for k, v in weather_counts.items()],
        'radius_mean': radius_mean,
        'max_travel_mean': max_travel_mean,
        'max_walk_mean': max_walk_mean,
        'over_time': {
            'users': create_over_time(User),
            'queries': create_over_time(Partner),
            'reviews': create_over_time(Review)
        }
    }
    
    return app.response(result)