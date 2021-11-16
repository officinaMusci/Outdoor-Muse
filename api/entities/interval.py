from dataclasses import dataclass
from datetime import datetime, timedelta

from utils import time


@dataclass
class Interval:
    '''Interval dataclass.
    
    It represents the time between a start time and an end time.

    Attributes:
        start: The time at the beginning of the interval.
        end: The time at the end of the interval.
    '''
    start:datetime
    end:datetime
    duration:timedelta=None

    def __post_init__(self):
        '''Automatically get duration after dataclass init.
        
        It allows Flask to perform a correct json conversion based on this
        dataclass field.
        '''
        self.duration = self._get_duration()

    def _get_duration(self) -> timedelta:
        '''Get the difference between start and end'''
        duration = self.end - self.start
        return timedelta(seconds=duration.total_seconds())
    
    def contains(self, dt:datetime) -> bool:
        '''Checks if a datetime is between the interval start and end'''
        return self.start <= time.localize_datetime(dt) <= self.end

    def to_dict(self) -> dict:
        '''Creates a dictionary from the Interval object'''
        return {
            'start': self.start,
            'end': self.end,
            'duration': self.duration
        }

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates a Location object from a dictionary.
        
        Creates a Location object using a Flask POST request dict.

        ARGS:
            dictionary: The dictionary received from Flask.
        '''
        return Interval(
            start=time.str_to_datetime(dictionary['start'])
                if isinstance(dictionary['start'], str)
                else time.localize_datetime(
                    datetime.fromtimestamp(dictionary['start'])
                ),
            end=time.str_to_datetime(dictionary['end'])
                if isinstance(dictionary['end'], str)
                else time.localize_datetime(
                    datetime.fromtimestamp(dictionary['end']
                ))
        )