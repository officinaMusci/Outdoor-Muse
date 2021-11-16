import os
from math import cos, sin, pi, atan2, sqrt
from datetime import datetime, timedelta
from typing import List

from dotenv import load_dotenv
import googlemaps

from services import database
from entities.place import Place, PlaceRow
from entities.itinerary import Itinerary
from entities.location import Location


load_dotenv()
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_KEY'))
language = os.getenv('LANGUAGE')


def get_distance(location_from:Location, location_to:Location) -> int:
    '''Calculates the distance from a location to another.
    
    ARGS:
        location_from: The first location.
        location_to: The second location.
    
    RETURNS:
        distance: The distance between the two points in meters.
    '''

    lat_from = location_from.lat
    lng_from = location_from.lng

    lat_to = location_to.lat
    lng_to = location_to.lng

    r = 6371.0
    phi_1 = lat_from * pi/180.0
    phi_2 = lat_to * pi/180.0
    delta_phi = (lat_to - lat_from) * pi/180.0
    delta_lambda = (lng_to - lng_from) * pi/180.0
    a = sin(delta_phi/2)**2 + (cos(phi_1) + cos(phi_2)) * sin(delta_lambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = r * c

    return d * 1000


def filter_places_by_distance(
    location:Location,
    places:List[Place],
    radius:int=0
) -> List[Place]:
    '''Filters and orders a place list in a radius.
    
    ARGS:
        location: The location from which to calculate.
        places: The places to filter and order.
        radius: The radius in which to keep places.

    RETURNS:
        places: The filtered and ordered place list.
    '''
    distances = map(lambda x: get_distance(location, x.location), places)
    with_distance = zip(places, distances)
    filtered = filter(lambda x: x[1] < radius, with_distance) if radius else 0
    srtd = sorted(filtered or with_distance, key=lambda x: x[1])

    return [x[0] for x in srtd]


def fetch_places_nearby(
    location:Location,
    radius:int,
    place_type:str,
    language:str=language
) -> List[Place]:
    '''Uses database places and Google Places API to make a Nearby Search.
    
    ARGS:
        location: The position from which to search.
        place_type: The place type to search for.
        radius: The search radius in meters.

    RETURNS:
        places: A place list.
    '''
    db_places = []
    
    with database.create_session().begin() as db_session:
        db_places = filter_places_by_distance(
            location,
            [
                Place.from_row(x)
                for x in db_session.query(PlaceRow).all()
            ],
            radius
        )

    '''
    response = gmaps.places_nearby(
        location=(location.lat, location.lng),
        radius=radius,
        type=place_type,
        language=language
    )
    '''
    response = None

    if response and 'results' in response:
        return db_places + [
            Place.from_dict(result)
            for result in response['results']
        ]
    else:
        return db_places


def fetch_itinerary(
    start_location:Location,
    end_location:Location,
    mode:str='transit',
    departure_time:datetime=None,
    arrival_time:datetime=None,
    language:str=language
) -> Itinerary:
    '''Uses Google Directions API to make an itinerary search.
    
    ARGS:
        start_location: The location from which to start.
        end_location: The location where the itinerary has to end.
        mode: The mode of transport. "driving", "walking", "bicycling"
              or "transit".
        departure_time: The desired time of departure.
        arrival_time: The desired time of arrival. Note: you can't specify both
                      departure_time and arrival_time.

    RETURNS:
        itinerary: An itinerary object.
    '''
    response = gmaps.directions(
        origin=start_location.to_dict(),
        destination=end_location.to_dict(),
        mode=mode or 'transit',
        departure_time=departure_time,
        arrival_time=arrival_time,
        language=language,
        units='metric'
    )

    if len(response):
        response = response[0]['legs'][0]

        '''If the itinerary is just a walk, Google doesn't give nor the
           departure_time neither the arrival_time'''
        if (
            'departure_time' not in response
            or 'arrival_time' not in response
        ):
            duration = timedelta(seconds=response['duration']['value'])
            
            if departure_time:
                response['departure_time'] = departure_time
                response['arrival_time'] = departure_time + duration
            
            elif arrival_time:
                response['departure_time'] = arrival_time - duration
                response['arrival_time'] = arrival_time
            
            response['departure_time'] = {
                'value': response['departure_time'].timestamp()
            }
            response['arrival_time'] = {
                'value': response['arrival_time'].timestamp()
            }

        return Itinerary.from_dict(response)

    else:
        return None