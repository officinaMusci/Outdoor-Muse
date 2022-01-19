from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
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


datetime_format = time.datetime_format()

datetime_start = datetime.now(timezone.utc).replace(hour=9, minute=0, second=0) + timedelta(days=1)
datetime_end = datetime_start + timedelta(hours=10)

TEST_QUERY = {
    'location': {
        'lat': 46.204391,
        'lng': 6.143158
    },
    'interval': {
        'start': datetime_start.strftime(datetime_format),
        'end': datetime_end.strftime(datetime_format)
    },
    'radius': 150000,
    'type': 'hike',
    'max_travel': '4:00:00',
    'max_walk': '2:00:00',
    'weather_ids': [
		301,
		615,
		800
	],
	'max_results': 10
}


class QueryRow(database.Base):
    '''ORM Query row representation'''
    __tablename__ = 'query'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    created = ORMColumn(ORMDateTime, default=datetime.utcnow)
    updated = ORMColumn(ORMDateTime, default=datetime.utcnow)
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
    language = ORMColumn(ORMString)


@dataclass
class Query:
    '''Query dataclass.

    It represents a search query containing all the search criteria.
    
    Attributes:
        id: The unique ID for the database.
        created: The date the database row was created.
        updated: The latest date the database row has been updated.
        location: The start location.
        interval: The interval available for the travel.
        radius: The radius within to search.
        place_type: The type of place to search.
        max_travel: The maximum travel time (including walk time).
        max_walk: The maximum walk time.
        weather_ids: The forecasts accepted for the query.
        max_results: The maximum amount of results to get.
        language: The language to use in results.
    '''
    location:Location
    interval:Interval
    radius:int
    place_type:str
    max_travel:timedelta
    max_walk:timedelta
    weather_ids:List[int]
    max_results:int=10
    language:str=None

    id:int=0
    created:datetime=None
    updated:datetime=None
    

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates and returns a Query object from a dictionary'''
        return Query(
            id=dictionary['id']
                if 'id' in dictionary else None,
            created=time.localize_datetime(dictionary['created'])
                if 'created' in dictionary else None,
            updated=time.localize_datetime(dictionary['updated'])
                if 'updated' in dictionary else None,
            location=Location.from_dict(dictionary['location']),
            interval=Interval.from_dict(dictionary['interval']),
            radius=dictionary['radius'],
            place_type=dictionary['type'],
            max_travel=time.str_to_delta(dictionary['max_travel'])
                if isinstance(dictionary['max_travel'], str)
                else dictionary['max_travel'],
            max_walk=time.str_to_delta(dictionary['max_walk'])
                if isinstance(dictionary['max_walk'], str)
                else dictionary['max_walk'],
            weather_ids=dictionary['weather_ids'],
            max_results=dictionary['max_results']
                if 'max_results' in dictionary else cls.max_results,
            language=dictionary['language']
                if 'language' in dictionary else cls.language
        )


    @classmethod
    def _from_row(cls, row:QueryRow):
        '''Returns a Query object obtained from a QueryRow object'''
        return Query(
            id=row.id,
            created=time.localize_datetime(row.created),
            updated=time.localize_datetime(row.updated),
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
            max_results=row.max_results,
            language=row.language
        )


    def _to_row(self) -> QueryRow:
        '''Returns a QueryRow object obtained from a Query object'''
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
            max_results=self.max_results,
            language=self.language
        )


    def _insert_row(self) -> int:
        '''Insert the Query row in the database'''
        query_row = self._to_row()

        with database.create_session().begin() as db_session:
            db_session.add(query_row)
            db_session.flush()
            query_id = query_row.id
        
        with database.create_session().begin() as db_session:
            query_row = db_session.query(QueryRow).get(query_id)
            db_session.close()
        
        self.id = query_row.id
        self.created = time.localize_datetime(query_row.created)
        self.updated = time.localize_datetime(query_row.updated)

        return self.id
    

    def _update_row(self) -> bool:
        '''Update the Query row in the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                query_row = db_session.query(QueryRow).get(self.id)

                query_row.updated = datetime.utcnow()
                query_row.location = self.location
                query_row.interval = self.interval
                query_row.radius = self.radius
                query_row.place_type = self.place_type
                query_row.max_travel = self.max_travel
                query_row.max_walk = self.max_walk
                query_row.weather_ids = self.weather_ids
                query_row.max_results = self.max_results
                query_row.language = self.language

                db_session.flush()
                
            return self.id
        
        return None


    def _delete_row(self) -> bool:
        '''Delete the Query row from the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                query_row = db_session.query(QueryRow).get(self.id)
                db_session.delete(query_row)
                db_session.flush()
            
            return True
        
        return False


    def save(self):
        '''Save the Query in the database'''
        return self._update_row() or self._insert_row()


    def delete(self):
        '''Delete the Query from the database'''
        return self._delete_row()


    @classmethod
    def get_from_id(cls, id:int):
        '''Returns a Query object obtained from a QueryRow id'''
        with database.create_session().begin() as db_session:
            query_row = db_session.query(QueryRow).get(id)
            query = Query._from_row(query_row) if query_row else None
            
            db_session.close()
        
        return query