from dataclasses import dataclass
from datetime import timedelta
from typing import List

from entities.location import Location
from entities.place import Place
from entities.itinerary import Itinerary
from entities.forecast import Forecast
from entities.interval import Interval


@dataclass
class Solution:
    '''Solution dataclass.

    It represents a Solution composed by a start location, a destination and
    the two itineraries to make a round trip.

    Attributes:
        start_location: The location where the round trip starts and ends.
        destination: The destination to reach.
        interval: The interval in which the solution should be performed.
        outward_itinerary: The itinerary to go to the destination.
        return_itinerary: The itinerary to return to the start_location.
        forecasts: A list of forecasts for the destination.
    '''
    start_location:Location
    destination:Place
    interval:Interval
    outward_itinerary:Itinerary
    return_itinerary:Itinerary
    forecasts:List[Forecast]
    info:dict=None

    def __post_init__(self):
        '''Automatically get solution infos after dataclass init.
        
        It allows Flask to perform a correct json conversion based on this
        dataclass field.
        '''
        self.info = self.get_info()

    @property
    def walk_duration(self) -> timedelta:
        '''Calculate and return the walk duration'''
        return (
            self.outward_itinerary.walk_duration
            + self.return_itinerary.walk_duration
        )

    @property
    def travel_duration(self) -> timedelta:
        '''Calculate and return the travel duration'''
        return (
            self.outward_itinerary.travel_duration
            + self.return_itinerary.travel_duration
        )
    
    @property
    def total_trip_duration(self) -> timedelta:
        '''Calculate and return the total trip duration'''
        return (
            self.walk_duration
            + self.travel_duration
        )

    @property
    def free_time(self) -> timedelta:
        '''Calculate the free time remaining'''
        return (
            self.interval.duration
            - self.total_trip_duration
        )
    
    def get_info(self) -> dict:
        '''Populates solution info'''
        return {
            'walk_duration': self.walk_duration,
            'travel_duration': self.travel_duration,
            'total_trip_duration': self.total_trip_duration,
            'free_time': self.free_time
        }
