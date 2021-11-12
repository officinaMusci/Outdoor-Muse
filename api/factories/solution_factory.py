from typing import List

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

    def _fetch_places(self):
        '''Makes a Place search within the Query radius.

        It searches the places of the chosen type inside the specified radius,
        around the location defined. Each Place is added to the 'places' list
        attribute to go on with the solution list production.
        '''
        query = self.query
        
        self._places = geography.fetch_places_nearby(
            location=query.location,
            radius=query.radius,
            place_type=query.place_type
        )
    
    def _fetch_itineraries(self):
        '''Gets the outward itinerary and the return itinerary for each Place.

        For each Place found, it searches the outward itinerary and the return
        itinerary. Then, it creates a Solution object and assign to it the Place
        and the two itineraries. If the Solution free time is positive, then it
        appends the Solution to the 'solutions' list attribute.
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

            if (outward_itinerary and return_itinerary):
                solution = Solution(
                    start_location=query.location,
                    destination=place,
                    interval=Interval(
                        start=query.interval.start,
                        end=query.interval.end
                    ),
                    outward_itinerary=outward_itinerary,
                    return_itinerary=return_itinerary,
                    forecasts=[]
                )

                if solution.free_time.total_seconds() >= 0:
                    self._solutions.append(solution)
    
    def _filter_by_trip_duration(self):
        '''Filters and orders the solutions by trip duration.
        
        It keeps in the 'solutions' list attribute the solutions which respect
        the maximum walk and maximum travel durations requested by the Query.
        '''
        query = self.query
        solutions = self.solutions
        
        filtered_solutions = [
            solution
            for solution in solutions
            if solution.walk_duration <= query.max_walk
            and solution.travel_duration <= query.max_travel
        ]
        
        filtered_solutions = sorted(
            filtered_solutions,
            key=lambda solution: solution.total_trip_duration
        )

        self._solutions = filtered_solutions
    
    def _fetch_forecasts(self):
        '''Get forecasts for the solutions.
        
        It gets the weather conditions during the interval defined by the Query
        for each Place found, then it updates the Solution with the Forecast
        obtained.
        '''
        solutions = []
        for solution in self.solutions:
            solution.forecasts = weather.get_daily_forecasts(
                location=solution.destination.location,
                interval=solution.interval
            )
            solutions.append(solution)

        self._solutions = solutions
    
    def  _filter_by_forecasts(self):
        '''Filters and orders the solutions by forecasts.
        
        It keeps in the 'solutions' list attribute the solutions which respect
        the weather conditions requested by the Query.
        '''
        query = self.query
        solutions = self.solutions
        
        filtered_solutions = []
        for solution in solutions:
            solution_weather_ids = [
                w['id']
                for f in solution.forecasts
                for w in f.weather
            ]

            has_good_weather = not len(list(
                set(solution_weather_ids)
                - set(query.weather_ids)
            )) or not len(query.weather_ids)

            if has_good_weather:
                filtered_solutions.append(solution)

        self._solutions = filtered_solutions

    def execute(self) -> List[Solution]:
        '''Executes the query and returns the solutions.
        
        It runs the method sequence which generates the Solutions requested by
        the Query, then it returns the populated 'solutions' list attribute.

        RETURNS:
            solutions: The list of solutions which match the search Query.
        '''
        max_results = self.query.max_results

        self._fetch_places()
        self._fetch_itineraries()
        self._filter_by_trip_duration()
        self._fetch_forecasts()
        self._filter_by_forecasts()
        
        return self.solutions[:max_results]