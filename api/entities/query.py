from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List
import random
from random import randint, randrange

from sqlalchemy import Column as ORMColumn
from sqlalchemy import String as ORMString
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import Float as ORMFloat
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import Interval as ORMInterval
from sqlalchemy import PickleType as ORMPickleType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .location import Location
from .interval import Interval
from .place import TYPES
from .relations import QueryPartnerRow, QueryPlaceRow
from utils import time
from utils.faker import faker
from services import database, weather


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
    types = ORMColumn(ORMPickleType, nullable=False)
    max_travel = ORMColumn(ORMInterval)
    max_walk = ORMColumn(ORMInterval)
    weather_ids = ORMColumn(ORMPickleType)
    max_results = ORMColumn(ORMInteger)
    language = ORMColumn(ORMString)

    user_id = ORMColumn(ORMInteger, ForeignKey('user.id'), nullable=True)

    place_relations = relationship('QueryPlaceRow', cascade='delete')
    partner_relations = relationship('QueryPartnerRow', cascade='delete')


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
        types: The types of place to search.
        max_travel: The maximum travel time (including walk time).
        max_walk: The maximum walk time.
        weather_ids: The forecasts accepted for the query.
        max_results: The maximum amount of results to get.
        language: The language to use in results.
        user_id: The user id of the author.
    '''
    location:Location
    interval:Interval
    radius:int
    types:List[str]
    max_travel:timedelta
    max_walk:timedelta
    weather_ids:List[int]
    max_results:int=10
    language:str=None
    
    user_id:int=None

    id:int=None
    created:datetime=None
    updated:datetime=None
    

    @classmethod
    def generate_random(cls):
        '''Generates a random Query object'''
        delta_days = randrange(7)

        datetime_format = time.datetime_format()
        datetime_start = (
            datetime.now(timezone.utc).replace(
                hour=(randrange(8) + 9),
                minute=0,
                second=0
            )
            + timedelta(days=delta_days)
        )
        datetime_end = datetime_start + timedelta(hours=randrange(8) - delta_days)

        coordinates = faker.local_latlng(
            country_code='CH',
            coords_only=True
        )

        weather_ids = random.sample(
            [v[0] for k, v in weather.id_groups.items()],
            randint(1, len(weather.id_groups.keys()))
        )

        return Query(
            location=Location.from_dict({
                'lat': coordinates[0],
                'lng': coordinates[1]
            }),
            interval=Interval.from_dict({
                'start': datetime_start.strftime(datetime_format),
                'end': datetime_end.strftime(datetime_format)
            }),
            radius=randint(1, 100) *  1000,
            types=TYPES,
            max_travel=timedelta(hours=randint(1, 4)),
            max_walk=timedelta(hours=randrange(2) + .5),
            weather_ids=weather_ids,
            max_results=10,
            user_id=None
        )


    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates and returns a Query object from a dictionary'''
        return Query(
            id=dictionary['id']
                if 'id' in dictionary else None,
            created=time.localize_datetime(
                    time.str_to_datetime(dictionary['created'])
                        if isinstance(dictionary['created'], str)
                        else dictionary['created']
                )
                if 'created' in dictionary else None,
            updated=time.localize_datetime(
                    time.str_to_datetime(dictionary['updated'])
                        if isinstance(dictionary['updated'], str)
                        else dictionary['updated']
                )
                if 'updated' in dictionary else None,
            location=Location.from_dict(dictionary['location']),
            interval=Interval.from_dict(dictionary['interval']),
            radius=dictionary['radius'],
            types=dictionary['types'],
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
                if 'language' in dictionary else cls.language,
            user_id=dictionary['user_id']
                if 'user_id' in dictionary else None
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
            types=row.types,
            max_travel=row.max_travel,
            max_walk=row.max_walk,
            weather_ids=row.weather_ids,
            max_results=row.max_results,
            language=row.language,
            user_id=row.user_id
        )


    def _to_row(self) -> QueryRow:
        '''Returns a QueryRow object obtained from a Query object'''
        return QueryRow(
            id=self.id,
            created=self.created,
            updated=self.updated,
            location_lat=self.location.lat,
            location_lng=self.location.lng,
            interval_start=self.interval.start,
            interval_end=self.interval.end,
            radius=self.radius,
            types=self.types,
            max_travel=self.max_travel,
            max_walk=self.max_walk,
            weather_ids=self.weather_ids,
            max_results=self.max_results,
            language=self.language,
            user_id=self.user_id
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
    

    def _update_row(self) -> int:
        '''Update the Query row in the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                query_row = db_session.query(QueryRow).get(self.id)

                query_row.updated = datetime.utcnow()
                query_row.location = self.location
                query_row.interval = self.interval
                query_row.radius = self.radius
                query_row.types = self.types
                query_row.max_travel = self.max_travel
                query_row.max_walk = self.max_walk
                query_row.weather_ids = self.weather_ids
                query_row.max_results = self.max_results
                query_row.language = self.language
                query_row.user_id = self.user_id

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


    def save(self) -> int:
        '''Save the Query in the database'''
        return self._update_row() or self._insert_row()


    def delete(self) -> bool:
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
    

    @classmethod
    def get_all(cls, filter_by:dict={}):
        '''Returns all Query objects from the database with optional filters'''
        with database.create_session().begin() as db_session:
            rows = db_session.query(QueryRow).filter_by(**filter_by).all()
            queries = [Query._from_row(row) for row in rows]
            
            db_session.close()
        
        return queries


    def associate_place_row(self, place_id=int) -> int:
        '''Insert a QueryPlace association row in the database'''
        query_place_row = QueryPlaceRow(
            query_id=self.id,
            place_id=place_id
        )

        with database.create_session().begin() as db_session:
            db_session.add(query_place_row)
            db_session.flush()
            query_place_row_id = query_place_row.id

        return query_place_row_id
    

    def associate_partner_row(self, partner_id=int) -> int:
        '''Insert a QueryPartner association row in the database'''
        query_partner_row = QueryPartnerRow(
            query_id=self.id,
            partner_id=partner_id
        )

        with database.create_session().begin() as db_session:
            db_session.add(query_partner_row)
            db_session.flush()
            query_partner_row_id = query_partner_row.id

        return query_partner_row_id
    

    def get_place_ids(self):
        '''Get all the Place ids linked to the Query object'''
        place_ids = []

        if self.id:
            with database.create_session().begin() as db_session:
                query_place_rows = db_session.query(QueryPlaceRow).filter_by(
                    query_id=self.id
                ).all()

                place_ids = [
                    query_place_row.place_id
                    for query_place_row in query_place_rows
                ]
                
                db_session.close()
        
        return place_ids


    def get_partner_ids(self):
        '''Get all the Partner ids linked to the Query object'''
        partner_ids = []

        if self.id:
            with database.create_session().begin() as db_session:
                query_partner_rows = db_session.query(QueryPartnerRow).filter_by(
                    query_id=self.id
                ).all()

                partner_ids = [
                    query_partner_row.partner_id
                    for query_partner_row in query_partner_rows
                ]
                
                db_session.close()
        
        return partner_ids