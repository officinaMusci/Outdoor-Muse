from dataclasses import dataclass
from datetime import datetime
from typing import List

from entities.location import Location


@dataclass
class Forecast:
    '''Forecast dataclass.
    
    It mainly represents an OpenWeather One Call forecast (daily), it can hold
    other forecasts types too.
    Built on https://openweathermap.org/api/one-call-api

    Attributes:

    '''
    location:Location
    datetime:datetime
    temperatures:dict
    feels_like:dict
    pressure:int
    humidity:int
    wind_speed:float
    weather:List[dict]

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates a Forecast object from a dictionary.
        
        Creates a Forecast object using the OpenWeather API client response.

        ARGS:
            dictionary: The dictionary received from the OpenWeather API client.
        '''
        return Forecast(
            location=Location.from_dict(dictionary['location']),
            datetime=datetime.fromtimestamp(dictionary['dt']),
            temperatures=dictionary['temp'],
            feels_like=dictionary['feels_like'],
            pressure=dictionary['pressure'],
            humidity=dictionary['humidity'],
            wind_speed=dictionary['wind_speed'],
            weather=dictionary['weather']
        )