import os
import re
from datetime import datetime, timedelta
from random import randrange

import pytz
from dotenv import load_dotenv


load_dotenv()


def datetime_format() -> str:
    '''Get the datetime format declared in .env'''
    return os.getenv('DATETIME_FORMAT')


def localize_datetime(dt:datetime) -> datetime:
    '''Localize the datetime to the UTC'''
    return pytz.utc.localize(dt)


def str_to_datetime(string:str) -> datetime:
    '''Converts a string to datetime using the .env format'''
    return localize_datetime(datetime.strptime(
        string,
        datetime_format()
    ))


def str_to_delta(string:str) -> timedelta:
    '''Converts a string to timedelta'''
    if 'day' in string:
        match = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                     r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', string)
    else:
        match = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                     r'(?P<s>\d[\.\d+]*)', string)
    if not match:
        return ''

    time_dict = {key: float(val) for key, val in match.groupdict().items()}

    if 'd' in time_dict:
        return timedelta(days=time_dict['d'], hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
    else:
        return timedelta(hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])


def random_datetime(start, end):
    '''Generates a random datetime between two datetimes'''
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta) if int_delta else 0

    return start + timedelta(seconds=random_second)