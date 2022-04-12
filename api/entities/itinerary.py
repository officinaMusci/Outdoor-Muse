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
        distance: The distance covered by the itinerary in meters.
        steps: The steps that make up the itinerary (main route).
        routes: The posssible routes.
        walk_duration: The walk duration of the itinerary.
        travel_duration: The travel duration of the itinerary.
    '''
    start_location:Location
    end_location:Location
    interval:Interval
    distance:int
    
    bounds:any
    copyrights:any
    fare:any
    legs:any
    overview_path:any
    overview_polyline:any
    summary:any
    warnings:any
    waypoint_order:any

    walk_duration:timedelta=None
    travel_duration:timedelta=None

    def __post_init__(self):
        '''Calculate the walk, travel and waiting durations'''
        walk_seconds = 0
        travel_seconds = 0

        for step in self.legs[0]['steps']:
            if step['travel_mode'] == 'WALKING':
                walk_seconds += step['duration']['value']
            else:
                travel_seconds += step['duration']['value']

        self.walk_duration = timedelta(seconds=walk_seconds)
        self.travel_duration = timedelta(seconds=travel_seconds)

        waiting_duration = self.interval.duration - (
            self.walk_duration
            + self.travel_duration
        )

        self.travel_duration += waiting_duration

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates an Itinerary object from a dictionary.
        
        Creates an Itinerary object using the Google API client response.

        ARGS:
            dictionary: The dictionary received from the Google API client.
        '''
        main_leg = dictionary['legs'][0]

        return Itinerary(
            start_location=Location.from_dict(main_leg['start_location']),
            end_location=Location.from_dict(main_leg['end_location']),
            interval=Interval.from_dict({
                'start': main_leg['departure_time']['value'],
                'end': main_leg['arrival_time']['value']
            }),
            distance=main_leg['distance']['value'],
            bounds=dictionary['bounds'],
            copyrights=dictionary['copyrights'],
            fare=dictionary['fare'] if 'fare' in dictionary else None,
            legs=[main_leg],
            overview_path=dictionary['overview_path']
                if 'overview_path' in dictionary else None,
            overview_polyline=dictionary['overview_polyline']
                if 'overview_polyline' in dictionary else None,
            summary=dictionary['summary']
                if 'summary' in dictionary else None,
            warnings=dictionary['warnings']
                if 'warnings' in dictionary else None,
            waypoint_order=dictionary['waypoint_order']
                if 'waypoint_order' in dictionary else None
        )