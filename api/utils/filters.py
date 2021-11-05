from datetime import timedelta
import fnmatch
from typing import List

from entities.solution import Solution


def filter_solutions_by_trip_duration(
    solutions:List[Solution],
    max_walk:timedelta,
    max_travel:timedelta
) -> List[Solution]:
    '''Filters and orders the solutions by trip duration.
    
    ARGS:
        solutions: The solutions to filter and order.
        max_walk: The maximum walk duration of solutions.
        max_travel: The maximum travel duration of solutions.

    RETURNS:
        filtered_solutions: The filtered and ordered solution list.
    '''
    filtered_solutions = [
        solution
        for solution in solutions
        if solution.walk_duration <= max_walk
        and solution.travel_duration <= max_travel
    ]
    
    filtered_solutions = sorted(
        filtered_solutions,
        key=lambda solution: solution.total_trip_duration
    )

    return filtered_solutions


def filter_solutions_by_weather(
    solutions:List[Solution],
    weather_ids:List[int]
) -> List[Solution]:
    '''Filters the solutions by weather.
    
    ARGS:
        solutions: The solutions to filter.
        weather_ids: The accepted weather ids for the solutions.

    RETURNS:
        filtered_solutions: The filtered solution list.
    '''
    filtered_solutions = []
    for solution in solutions:
        solution_weather_ids = [
            w['id']
            for f in solution.forecasts
            for w in f.weather
        ]
        
        has_good_weather = not len(list(
            set(weather_ids)
            - set(solution_weather_ids)
        )) or not len(weather_ids)

        if has_good_weather:
            filtered_solutions.append(solution)

    return filtered_solutions