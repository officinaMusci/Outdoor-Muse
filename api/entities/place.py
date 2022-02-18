from dataclasses import dataclass
from datetime import datetime, timedelta
from random import randint
import statistics
from typing import List

from sqlalchemy import Column as ORMColumn
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import String as ORMString
from sqlalchemy import Float as ORMFloat
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import Interval as ORMInterval
from sqlalchemy import PickleType as ORMPickleType
from sqlalchemy.orm import relationship

from .location import Location
from .review import Review
from .relations import QueryPlaceRow
from utils import time
from utils.faker import faker
from services import database


TYPES = ['hike']


class PlaceRow(database.Base):
    '''ORM Place row representation'''
    __tablename__ = 'place'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    created = ORMColumn(ORMDateTime, default=datetime.utcnow)
    updated = ORMColumn(ORMDateTime, default=datetime.utcnow)
    location_lat = ORMColumn(ORMFloat)
    location_lng = ORMColumn(ORMFloat)
    name = ORMColumn(ORMString(255))
    difficulty = ORMColumn(ORMInteger)
    duration = ORMColumn(ORMInterval)
    distance = ORMColumn(ORMInteger)
    types = ORMColumn(ORMPickleType)

    query_relations = relationship('QueryPlaceRow', cascade='delete')
    reviews = relationship('ReviewRow', cascade='delete')
    solutions = relationship('SolutionRow', cascade='delete')


@dataclass
class Place:
    '''Place dataclass.

    It represents a Place.
    
    Attributes:
        id: The unique ID for the database.
        created: The date the database row was created.
        updated: The latest date the database row has been updated.
        location: The place location.
        name: The place name.
        difficulty: The difficulty level from 0 to 4.
        duration: The duration of the average visit.
        distance: The distance covered during the average visit.
        types: The types the place belongs to.
        review_count: The amount of reviews received.
        average_rating: The average rating obtained from reviews.
        query_count: The amount of query relations.
    '''
    name:str
    location:Location
    difficulty:int=None
    duration:timedelta=None
    distance:int=None
    types:List[str]=None

    review_count:int=0
    average_rating:int=0
    query_count:int=0

    id:int=None
    created:datetime=None
    updated:datetime=None


    def __post_init__(self):
        '''Get additional data from database relations'''
        reviews = Review.get_all(filter_by={'place_id': self.id})

        self.review_count = len(reviews)
        self.average_rating = statistics.mean([
            review.rating for review in reviews
        ]) if reviews else 0

        with database.create_session().begin() as db_session:
            self.query_count = len(
                db_session
                .query(QueryPlaceRow)
                .filter_by(place_id=self.id)
                .all()
            )
            
            db_session.close()


    @classmethod
    def generate_random(cls):
        '''Generates a random Place object'''
        coordinates = faker.local_latlng(
            country_code='CH'
        )

        return Place(
            name=coordinates[2],
            duration=timedelta(hours=randint(1, 4)),
            distance=randint(1, 100) *  1000,
            difficulty=randint(1, 4),
            location=Location.from_dict({
                'lat': coordinates[0],
                'lng': coordinates[1]
            }),
            types=TYPES
        )


    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates and returns a Place object from a dictionary'''
        return Place(
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
            name=dictionary['name'],
            location=Location.from_dict(
                dictionary['location']
                if 'location' in dictionary
                else dictionary['geometry']['location'] # Google Places API
            ),
            difficulty=dictionary['difficulty']
                if 'difficulty' in dictionary else None,
            duration=time.str_to_delta(dictionary['duration'])
                if 'duration' in dictionary else None,
            distance=dictionary['distance']
                if 'distance' in dictionary else None,
            types=dictionary['types']
                if 'types' in dictionary else None
        )
    

    @classmethod
    def _from_row(cls, row:PlaceRow):
        '''Returns a Place object obtained from a PlaceRow object'''
        return Place(
            id=row.id,
            created=time.localize_datetime(row.created),
            updated=time.localize_datetime(row.updated),
            name=row.name,
            location=Location(
                lat=row.location_lat,
                lng=row.location_lng
            ),
            difficulty=row.difficulty,
            duration=row.duration,
            distance=row.distance,
            types=row.types
        )
    

    def _to_row(self) -> PlaceRow:
        '''Returns a PlaceRow object obtained from a Place object'''
        return PlaceRow(
            id=self.id,
            created=self.created,
            updated=self.updated,
            name=self.name,
            location_lat=self.location.lat,
            location_lng=self.location.lng,
            difficulty=self.difficulty,
            duration=self.duration,
            distance=self.distance,
            types=self.types
        )


    def _insert_row(self) -> int:
        '''Insert the Place row in the database'''
        place_row = self._to_row()

        with database.create_session().begin() as db_session:
            db_session.add(place_row)
            db_session.flush()
            place_id = place_row.id
        
        with database.create_session().begin() as db_session:
            place_row = db_session.query(PlaceRow).get(place_id)
            db_session.close()
        
        self.id = place_row.id
        self.created = time.localize_datetime(place_row.created)
        self.updated = time.localize_datetime(place_row.updated)

        return self.id


    def _update_row(self) -> int:
        '''Update the Place row in the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                place_row = db_session.query(PlaceRow).get(self.id)

                place_row.updated = datetime.utcnow()
                place_row.name = self.name
                place_row.location_lat = self.location.lat
                place_row.location_lng = self.location.lng
                place_row.difficulty = self.difficulty
                place_row.duration = self.duration
                place_row.distance = self.distance
                place_row.types = self.types

                db_session.flush()
                
            return self.id
        
        return None
    

    def _delete_row(self) -> bool:
        '''Delete the Place row from the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                place_row = db_session.query(PlaceRow).get(self.id)
                db_session.delete(place_row)
                db_session.flush()
            
            return True
        
        return False
    

    def save(self) -> int:
        '''Save the Place in the database'''
        return self._update_row() or self._insert_row()


    def delete(self) -> bool:
        '''Delete the Place from the database'''
        return self._delete_row()


    @classmethod
    def get_from_id(cls, id:int):
        '''Returns a Place object obtained from a PlaceRow id'''
        with database.create_session().begin() as db_session:
            place_row = db_session.query(PlaceRow).get(id)
            place = Place._from_row(place_row) if place_row else None
            
            db_session.close()
        
        return place
    

    @classmethod
    def get_all(cls, filter_by:dict={}):
        '''Returns all Place objects from the database with optional filters'''
        with database.create_session().begin() as db_session:
            rows = db_session.query(PlaceRow).filter_by(**filter_by).all()
            places = [Place._from_row(row) for row in rows]
            
            db_session.close()
        
        return places
    

    @classmethod
    def get_count(cls, filter_by:dict={}):
        '''Counts all Place objects in the database with optional filters'''
        with database.create_session().begin() as db_session:
            count = len(
                db_session.query(PlaceRow).filter_by(**filter_by).all()
            )
            
            db_session.close()
        
        return count