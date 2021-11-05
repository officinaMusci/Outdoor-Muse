from dataclasses import dataclass
from typing import List

from .location import Location


@dataclass
class Place:
    '''Place dataclass.

    It mainly represents a Google Maps place, it can hold other place types too.
    Built on https://developers.google.com/maps/documentation/places
    
    Attributes:
        location: The place location.
        name: The place name.
        opening_hours: The place opening hours.
        photos: The place photos.
        place_id: The place ID.
        price_level: The place price level.
        rating: The place rating.
        types: The place type strings.
        user_ratings_total: The place ratings total.
    '''
    location:Location
    name:str=None
    opening_hours:dict=None
    photos:list=None
    place_id:str=None
    price_level:int=None
    rating:float=None
    types:List[str]=None
    user_ratings_total:int=None

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates a Place object from a dictionary.
        
        Creates a Place object using the Google API client response.

        ARGS:
            dictionary: The dictionary received from the Google API client.
        '''
        return Place(
            location=Location.from_dict(dictionary['geometry']['location']),
            name=dictionary['name']
                if 'name' in dictionary else None,
            opening_hours=dictionary['opening_hours']
                if 'opening_hours' in dictionary else None,
            photos=dictionary['photos']
                if 'photos' in dictionary else None,
            place_id=dictionary['place_id'],
            price_level=dictionary['price_level']
                if 'price_level' in dictionary else None,
            rating=dictionary['rating']
                if 'rating' in dictionary else None,
            types=dictionary['types']
                if 'types' in dictionary else None,
            user_ratings_total=dictionary['user_ratings_total']
                if 'user_ratings_total' in dictionary else None
        )