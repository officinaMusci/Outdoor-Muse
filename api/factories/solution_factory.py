from typing import List

from utils import filters
from services import geography, weather
from entities.query import Query
from entities.interval import Interval
from entities.place import Place
from entities.solution import Solution


class SolutionFactory:
    '''Holds a search query and creates a solution list from it.
    
    Attributes:
        query: The query to execute.
    '''
    def __init__(self, query:Query):
        self._query = query
        self._places = []
        self._solutions = []
    
    @property
    def query(self) -> Query:
        return self._query
    
    @property
    def places(self) -> List[Place]:
        return self._places
    
    @property
    def solutions(self) -> List[Solution]:
        return self._solutions

    def _fetch_places(self) -> List[Place]:
        '''Makes a place nearby search.
    
        ARGS:
            query: The query to execute.

        RETURNS:
            places: A place list.
        '''
        query = self.query
        
        self._places = geography.fetch_places_nearby(
            location=query.location,
            radius=query.radius,
            place_type=query.place_type
        )

        return self.places
    
    def _fetch_itineraries(self) -> List[Solution]:
        '''Makes an itinerary search.
    
        ARGS:
            query: The query to execute.
            places: The places to reach.

        RETURNS:
            solutions: A solution list.
        '''
        query = self.query
        places = self.places
        
        for place in places:
            outward_itinerary = geography.fetch_itinerary(
                start_location=query.location,
                end_location=place.location,
                departure_time=query.interval.start
            )
            
            return_itinerary = geography.fetch_itinerary(
                start_location=place.location,
                end_location=query.location,
                arrival_time=query.interval.end
            )

            if outward_itinerary and return_itinerary:
                self._solutions.append(Solution(
                    start_location=query.location,
                    destination=place,
                    interval=Interval(
                        start=query.interval.start,
                        end=query.interval.end
                    ),
                    outward_itinerary=outward_itinerary,
                    return_itinerary=return_itinerary,
                    forecasts=[]
                ))
            
        return self.solutions
    
    def _filter_by_trip_duration(self) -> List[Solution]:
        '''Filters and orders the solutions by trip duration'''
        query = self.query
        solutions = self.solutions
        
        self._solutions = filters.filter_solutions_by_trip_duration(
            solutions=solutions,
            max_travel=query.max_travel,
            max_walk=query.max_walk
        )

        return self.solutions
    
    def _fetch_forecasts(self) -> List[Solution]:
        '''Get forecasts for the solutions'''
        solutions = []
        for solution in self.solutions:
            solution.forecasts = weather.get_daily_forecasts(
                location=solution.destination.location,
                interval=solution.interval
            )
            solutions.append(solution)

        self._solutions = solutions
        return self.solutions
    
    def  _filter_by_forecasts(self) -> List[Solution]:
        '''Filters and orders the solutions by forecasts'''
        query = self.query
        solutions = self.solutions
        
        self._solutions = filters.filter_solutions_by_weather(
            solutions=solutions,
            weather_ids=query.weather_ids
        )

        return self.solutions

    def execute(self) -> List[Solution]:
        '''Executes the query and returns the solutions'''
        max_results = self.query.max_results

        self._fetch_places()
        self._fetch_itineraries()
        self._filter_by_trip_duration()
        self._fetch_forecasts()
        self._filter_by_forecasts()
        
        return self.solutions[:max_results]