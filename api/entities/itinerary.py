from dataclasses import dataclass
from datetime import timedelta

from entities.location import Location
from entities.interval import Interval


@dataclass
class Itinerary:
    '''Itinerary dataclass.
    
    It mainly represents a Google Maps itinerary, it can hold other itinerary
    types too.
    Built on
    https://developers.google.com/maps/documentation/directions/get-directions

    Attributes:
        start_location: The location where the itinerary begins.
        end_location: The location where the itinerary ends.
        interval: The interval in which the itinerary should be performed.
        walk_duration: The walk duration of the itinerary.
        travel_duration: The travel duration of the itinerary.
        distance: The distance covered by the itinerary in meters.
        steps: The steps that make up the itinerary.
    '''
    start_location:Location
    end_location:Location
    interval:Interval
    distance:int
    steps:list
    walk_duration:timedelta=None
    travel_duration:timedelta=None

    def __post_init__(self):
        '''Calculate the walk and travel durations'''
        walk_seconds = 0
        travel_seconds = 0

        for step in self.steps:
            if step['travel_mode'] == 'WALKING':
                walk_seconds += step['duration']['value']
            else:
                travel_seconds += step['duration']['value']

        self.walk_duration=timedelta(seconds=walk_seconds)
        self.travel_duration=timedelta(seconds=travel_seconds)

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates an Itinerary object from a dictionary.
        
        Creates an Itinerary object using the Google API client response.

        ARGS:
            dictionary: The dictionary received from the Google API client.
        '''
        return Itinerary(
            start_location=Location.from_dict(dictionary['start_location']),
            end_location=Location.from_dict(dictionary['end_location']),
            interval=Interval.from_dict({
                'start': dictionary['departure_time']['value'],
                'end': dictionary['arrival_time']['value']
            }),
            distance=dictionary['distance']['value'],
            steps=dictionary['steps']
        )