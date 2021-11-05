from dataclasses import dataclass


@dataclass
class Location:
    '''Location dataclass.

    It represents a physical location identified by latitude and longitude
    coordinates.
    
    Attributes:
        lat: The location latitude.
        lng: The location longitude.
    '''
    lat:float
    lng:float

    def to_dict(self):
        '''Creates a dictionary from the Location object'''
        return {
            'lat': self.lat,
            'lng': self.lng
        }

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates a Location object from a dictionary.
        
        Creates a Location object using a Flask POST request dict.

        ARGS:
            dictionary: The dictionary received from Flask.
        '''
        return Location(
            lat=dictionary['lat'],
            lng=dictionary['lng']
        )