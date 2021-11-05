from dataclasses import dataclass
from datetime import timedelta
from typing import List

from sqlalchemy import Column as ORMColumn
from sqlalchemy import String as ORMString
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import Float as ORMFloat
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import Interval as ORMInterval
from sqlalchemy import PickleType as ORMPickleType

from .location import Location
from .interval import Interval
from utils import time
from services import database


class QueryRow( database.Base ):
    '''ORM Query row representation'''
    __tablename__ = 'query'

    id = ORMColumn(ORMInteger, primary_key=True)
    location_lat = ORMColumn(ORMFloat, nullable=False)
    location_lng = ORMColumn(ORMFloat, nullable=False)
    interval_start = ORMColumn(ORMDateTime)
    interval_end = ORMColumn(ORMDateTime)
    radius = ORMColumn(ORMInteger, nullable=False)
    place_type = ORMColumn(ORMString, nullable=False)
    max_travel = ORMColumn(ORMInterval)
    max_walk = ORMColumn(ORMInterval)
    weather_ids = ORMColumn(ORMPickleType)
    max_results = ORMColumn(ORMInteger)


@dataclass
class Query:
    '''Query dataclass.

    It represents a search query containing all the API search criteria.
    
    Attributes:
        location: The start location.
        interval: The interval available for the travel.
        radius: The radius within to search.
        place_type: The type of place to search.
        max_travel: The maximum travel time (including walk time).
        max_walk: The maximum walk time.
        weather_ids: The forecasts accepted for the query.
        max_results: The maximum amount of results to get.
    '''
    location:Location
    interval:Interval
    radius:int
    place_type:str
    max_travel:timedelta
    max_walk:timedelta
    weather_ids:List[int]
    max_results:int

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates a Query object from a dictionary.
        
        Creates a Query object using a Flask POST request dict.

        ARGS:
            dictionary: The dictionary received from Flask.
        '''
        return Query(
            location=Location.from_dict(dictionary['location']),
            interval=Interval.from_dict(dictionary['interval']),
            radius=dictionary['radius'],
            place_type=dictionary['type'],
            max_travel=time.str_to_delta(dictionary['max_travel']),
            max_walk=time.str_to_delta(dictionary['max_walk']),
            weather_ids=dictionary['weather_ids'],
            max_results=dictionary['max_results'],
        )

    @classmethod
    def from_row(cls, row:QueryRow):
        '''Returns a Query object obtained from the QueryRow object'''
        return Query(
            location=Location(
                lat=row.location_lat,
                lng=row.location_lng
            ),
            interval=Interval(
                start=time.localize_datetime(row.interval_start),
                end=time.localize_datetime(row.interval_end)
            ),
            radius=row.radius,
            place_type=row.place_type,
            max_travel=row.max_travel,
            max_walk=row.max_walk,
            weather_ids=row.weather_ids,
            max_results=row.max_results
        )
    
    @classmethod
    def from_row_id(cls, id:int):
        '''Returns a Query object obtained from the QueryRow id'''
        with database.create_session().begin() as db_session:
            query_row = db_session.query(QueryRow).one()
            query = Query.from_row(query_row)
            db_session.close()
        
        return query

    def to_row(self) -> QueryRow:
        '''Returns a QueryRow object obtained from the Query object'''
        return QueryRow(
            location_lat=self.location.lat,
            location_lng=self.location.lng,
            interval_start=self.interval.start,
            interval_end=self.interval.end,
            radius=self.radius,
            place_type=self.place_type,
            max_travel=self.max_travel,
            max_walk=self.max_walk,
            weather_ids=self.weather_ids,
            max_results=self.max_results
        )
    
    def store_row(self) -> int:
        '''Store the Query in the database'''
        query_row = self.to_row()

        with database.create_session().begin() as db_session:
            db_session.add(query_row)
            db_session.flush()
            id = query_row.id
            db_session.commit()
        
        return id