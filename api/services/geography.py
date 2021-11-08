import os
from datetime import datetime, timedelta
from typing import List

from dotenv import load_dotenv
import googlemaps

from services import database
from entities.place import Place
from entities.itinerary import Itinerary
from entities.location import Location


load_dotenv()
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_KEY'))
language = os.getenv('LANGUAGE')


def fetch_places_nearby(
    location:Location,
    radius:int,
    place_type:str,
    language:str=language
) -> List[Place]:
    '''Uses web wrapping and Google Places API to make a Nearby Search.
    
    ARGS:
        location: The position from which to search.
        place_type: The place type to search for.
        radius: The search radius in meters.

    RETURNS:
        places: A place list.
    '''
    ww_list = []
    sql_query = '''
        SELECT *, (
            3959 * acos(
                cos(radians(:lat))
                * cos(radians(location_lat))
                * cos(radians(location_lng) - radians(:lng))
                + sin(radians(:lat))
                * sin(radians(location_lat))
            )
        ) AS distance
        FROM place
        WHERE distance < m_to_mi(:radius)
        AND types LIKE '%'||:type||'%'
        ORDER BY distance ASC;
    '''
    with database.create_session().begin() as db_session:
        ww_list = [Place.from_row(x) for x in db_session.execute(
            sql_query,
            {
                'lat': location.lat,
                'lng': location.lng,
                'radius': radius,
                'type': place_type
            }
        )]

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
        return ww_list + [
            Place.from_dict(result)
            for result in response['results']
        ]
    else:
        return ww_list


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