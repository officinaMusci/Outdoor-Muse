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


class PlaceRow( database.Base ):
    '''ORM Place row representation'''
    __tablename__ = 'place'

    id = ORMColumn(ORMInteger, primary_key=True)
    location_lat = ORMColumn(ORMFloat, nullable=False)
    location_lng = ORMColumn(ORMFloat, nullable=False)
    name = ORMColumn(ORMString, nullable=False)
    notes = ORMColumn(ORMString)
    diff_degree = ORMColumn(ORMString)
    duration = ORMColumn(ORMInterval)
    distance = ORMColumn(ORMInteger)
    diff_level = ORMColumn(ORMInteger)
    types = ORMColumn(ORMPickleType)


@dataclass
class Place:
    '''Place dataclass.

    It represents a Place.
    
    Attributes:
        location: The place location.
        name: The place name.
        notes
        diff_degree
        duration
        distance
        diff_level
        types
    '''
    location:Location
    name:str
    notes:str=None
    diff_degree:str=None
    duration:timedelta=None
    distance:int=None
    diff_level:int=None
    types:List[str]=None

    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates a Place object from a dictionary.

        ARGS:
            dictionary: The dictionary received from Flask.
        '''
        return Place(
            location=Location.from_dict(
                dictionary['location']
                if 'location' in dictionary
                else dictionary['geometry']['location'] # Google Places API
            ),
            name=dictionary['name'],
            notes=dictionary['notes']
                if 'notes' in dictionary else None,
            diff_degree=dictionary['diff_degree']
                if 'diff_degree' in dictionary else None,
            duration=time.str_to_delta(dictionary['duration'])
                if 'duration' in dictionary else None,
            distance=dictionary['distance']
                if 'distance' in dictionary else None,
            diff_level=dictionary['diff_level']
                if 'diff_level' in dictionary else None,
            types=dictionary['types']
                if 'types' in dictionary else None
        )
    
    @classmethod
    def from_row(cls, row:PlaceRow):
        '''Returns a Place object obtained from a PlaceRow object'''
        return Place(
            location=Location(
                lat=row.location_lat,
                lng=row.location_lng
            ),
            name=row.name,
            notes=row.notes,
            diff_degree=row.diff_degree,
            duration=row.duration,
            distance=row.distance,
            diff_level=row.diff_level,
            types=row.types
        )
    
    @classmethod
    def from_row_id(cls, id:int):
        '''Returns a Place object obtained from a PlaceRow id'''
        with database.create_session().begin() as db_session:
            place_row = db_session.query(PlaceRow).get(id)
            place = Place.from_row(place_row)
            db_session.close()
        
        return place
    
    def to_row(self) -> PlaceRow:
        '''Returns a PlaceRow object obtained from a Place object'''
        return PlaceRow(
            location_lat=self.location.lat,
            location_lng=self.location.lng,
            name=self.name,
            notes=self.notes,
            diff_degree=self.diff_degree,
            duration=self.duration,
            distance=self.distance,
            diff_level=self.diff_level,
            types=self.types
        )
    
    def store_row(self) -> int:
        '''Store the Place in the database'''
        place_row = self.to_row()

        with database.create_session().begin() as db_session:
            db_session.add(place_row)
            db_session.flush()
            id = place_row.id
            db_session.commit()
        
        return id