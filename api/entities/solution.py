from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List
from random import randint, randrange

from sqlalchemy import Column as ORMColumn
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import Float as ORMFloat
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import PickleType as ORMPickleType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .location import Location
from .place import Place
from .itinerary import Itinerary
from .forecast import Forecast
from .interval import Interval
from .relations import SolutionPartnerRow
from utils import time
from utils.faker import faker
from services import database


class SolutionRow(database.Base):
    '''ORM Solution row representation'''
    __tablename__ = 'solution'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    created = ORMColumn(ORMDateTime, default=datetime.utcnow)
    updated = ORMColumn(ORMDateTime, default=datetime.utcnow)

    start_location_lat = ORMColumn(ORMFloat)
    start_location_lng = ORMColumn(ORMFloat)
    interval_start = ORMColumn(ORMDateTime)
    interval_end = ORMColumn(ORMDateTime)
    outward_itinerary = ORMColumn(ORMPickleType)
    return_itinerary = ORMColumn(ORMPickleType)
    forecasts = ORMColumn(ORMPickleType)

    query_id = ORMColumn(ORMInteger, ForeignKey('query.id'), nullable=True)
    place_id = ORMColumn(ORMInteger, ForeignKey('place.id'), nullable=True)
    user_id = ORMColumn(ORMInteger, ForeignKey('user.id'), nullable=True)
    
    partner_relations = relationship('SolutionPartnerRow', cascade='delete')


@dataclass
class Solution:
    '''Solution dataclass.

    It represents a Solution composed by a start location, a destination and
    the two itineraries to make a round trip.

    Attributes:
        id: The unique ID for the database.
        created: The date the database row was created.
        updated: The latest date the database row has been updated.
        start_location: The location where the round trip starts and ends.
        query_id: The id of the query the solution derivates from.
        place_id: The id of the place to reach.
        user_id: The id of the user who launched the search.
        interval: The interval in which the solution should be performed.
        outward_itinerary: The itinerary to go to the destination.
        return_itinerary: The itinerary to return to the start_location.
        forecasts: A list of forecasts for the destination.
        info: A dictionary containing a summary of the main solution info.
    '''
    start_location:Location
    interval:Interval
    outward_itinerary:Itinerary
    return_itinerary:Itinerary
    forecasts:List[Forecast]

    info:dict=None

    query_id:int=None
    place_id:int=None
    user_id:int=None

    id:int=None
    created:datetime=None
    updated:datetime=None


    def __post_init__(self):
        '''Automatically get solution infos after dataclass init.
        
        It allows Flask to perform a correct json conversion based on this
        dataclass field.
        '''
        self.info = self.get_info()


    @classmethod
    def generate_random(cls):
        '''Generates a random Solution object'''
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
        datetime_end = datetime_start + timedelta(days=randrange(8) - delta_days)

        coordinates = faker.local_latlng(
            country_code='CH',
            coords_only=True
        )

        coordinates_2 = faker.local_latlng(
            country_code='CH',
            coords_only=True
        )

        return Solution(
            start_location=Location.from_dict({
                'lat': coordinates[0],
                'lng': coordinates[1]
            }),
            interval=Interval.from_dict({
                'start': datetime_start.strftime(datetime_format),
                'end': datetime_end.strftime(datetime_format)
            }),
            outward_itinerary=Itinerary.from_dict({
                'start_location' : {
                    'lat': coordinates[0],
                    'lng': coordinates[1]
                },
                'end_location' : {
                    'lat': coordinates_2[0],
                    'lng': coordinates_2[1]
                },
                'departure_time': {
                    'value': datetime_start.strftime(datetime_format)
                },
                'arrival_time': {
                    'value': (
                        datetime_start + timedelta(minutes=randrange(60))
                    ).strftime(datetime_format),
                },
                'distance': {
                    'value': randint(1000, 100000)
                },
                'steps': []
            }),
            return_itinerary=Itinerary.from_dict({
                'start_location' : {
                    'lat': coordinates_2[0],
                    'lng': coordinates_2[1]
                },
                'end_location' : {
                    'lat': coordinates[0],
                    'lng': coordinates[1]
                },
                'departure_time': {
                    'value': (
                        datetime_end - timedelta(minutes=randrange(60))
                    ).strftime(datetime_format)
                },
                'arrival_time': {
                    'value': datetime_end.strftime(datetime_format),
                },
                'distance': {
                    'value': randint(1000, 100000)
                },
                'steps': []
            }),
            forecasts=[],
            query_id=None,
            place_id=None,
            user_id=None,
        )


    @property
    def walk_duration(self) -> timedelta:
        '''Calculate and return the walk duration'''
        return (
            self.outward_itinerary.walk_duration
            + self.return_itinerary.walk_duration
        )


    @property
    def travel_duration(self) -> timedelta:
        '''Calculate and return the travel duration'''
        return (
            self.outward_itinerary.travel_duration
            + self.return_itinerary.travel_duration
        )
    

    @property
    def total_trip_duration(self) -> timedelta:
        '''Calculate and return the total trip duration'''
        return (
            self.walk_duration
            + self.travel_duration
        )


    @property
    def free_time(self) -> timedelta:
        '''Calculate the free time remaining'''
        place = Place.get_from_id(self.place_id) if self.place_id else None

        place_duration = (
            place.duration
            if place and hasattr(place, 'duration')
            else timedelta(0)
        )
        
        return (
            self.interval.duration
            - self.total_trip_duration
            - place_duration
        )


    def get_info(self) -> dict:
        '''Populates solution info'''
        return {
            'walk_duration': self.walk_duration,
            'travel_duration': self.travel_duration,
            'total_trip_duration': self.total_trip_duration,
            'free_time': self.free_time
        }


    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates and returns a Solution object from a dictionary'''
        return Solution(
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
            start_location=Location.from_dict(dictionary['start_location']),
            interval=Interval.from_dict(dictionary['interval']),
            outward_itinerary=Itinerary.from_dict(
                dictionary['outward_itinerary']
            ),
            return_itinerary=Itinerary.from_dict(
                dictionary['return_itinerary']
            ),
            forecasts=dictionary['forecasts'],
            query_id=dictionary['query_id']
                if 'query_id' in dictionary else None,
            place_id=dictionary['place_id']
                if 'place_id' in dictionary else None,
            user_id=dictionary['user_id']
                if 'user_id' in dictionary else None
        )


    @classmethod
    def _from_row(cls, row:SolutionRow):
        '''Returns a Solution object obtained from a SolutionRow object'''
        return Solution(
            id=row.id,
            created=time.localize_datetime(row.created),
            updated=time.localize_datetime(row.updated),
            start_location=Location(
                lat=row.start_location_lat,
                lng=row.start_location_lng
            ),
            interval=Interval(
                start=time.localize_datetime(row.interval_start),
                end=time.localize_datetime(row.interval_end)
            ),
            outward_itinerary=row.outward_itinerary,
            return_itinerary=row.return_itinerary,
            forecasts=row.forecasts,
            query_id=row.query_id,
            place_id=row.place_id,
            user_id=row.user_id
        )

    
    def _to_row(self) -> SolutionRow:
        '''Returns a SolutionRow object obtained from a Solution object'''
        return SolutionRow(
            id=self.id,
            created=self.created,
            updated=self.updated,
            start_location_lat=self.start_location.lat,
            start_location_lng=self.start_location.lng,
            interval_start=self.interval.start,
            interval_end=self.interval.end,
            outward_itinerary=self.outward_itinerary,
            return_itinerary=self.return_itinerary,
            forecasts=self.forecasts,
            query_id=self.query_id,
            place_id=self.place_id,
            user_id=self.user_id
        )
    

    def _insert_row(self) -> int:
        '''Insert the Solution row in the database'''
        solution_row = self._to_row()

        with database.create_session().begin() as db_session:
            db_session.add(solution_row)
            db_session.flush()
            solution_id = solution_row.id
        
        with database.create_session().begin() as db_session:
            solution_row = db_session.query(SolutionRow).get(solution_id)
            db_session.close()
        
        self.id = solution_row.id
        self.created = time.localize_datetime(solution_row.created)
        self.updated = time.localize_datetime(solution_row.updated)

        return self.id
    

    def _update_row(self) -> int:
        '''Update the Solution row in the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                solution_row = db_session.query(SolutionRow).get(self.id)

                solution_row.updated = datetime.utcnow()
                solution_row.start_location_lat = self.start_location.lat
                solution_row.start_location_lng = self.start_location.lng
                solution_row.interval_start = self.interval.start
                solution_row.interval_end = self.interval.end
                solution_row.outward_itinerary = self.outward_itinerary
                solution_row.return_itinerary = self.return_itinerary
                solution_row.forecasts = self.forecasts
                solution_row.query_id = self.query_id
                solution_row.place_id = self.place_id
                solution_row.user_id = self.user_id

                db_session.flush()
                
            return self.id
        
        return None

    
    def _delete_row(self) -> bool:
        '''Delete the Solution row from the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                solution_row = db_session.query(SolutionRow).get(self.id)
                db_session.delete(solution_row)
                db_session.flush()
            
            return True
        
        return False


    def save(self) -> int:
        '''Save the Solution in the database'''
        return self._update_row() or self._insert_row()


    def delete(self) -> bool:
        '''Delete the Solution from the database'''
        return self._delete_row()
    

    @classmethod
    def get_from_id(cls, id:int):
        '''Returns a Solution object obtained from a SolutionRow id'''
        with database.create_session().begin() as db_session:
            solution_row = db_session.query(SolutionRow).get(id)
            query = Solution._from_row(solution_row) if solution_row else None
            
            db_session.close()
        
        return query
    

    @classmethod
    def get_all(cls, filter_by:dict={}):
        '''Returns all Solution objects from the database with optional filters'''
        with database.create_session().begin() as db_session:
            rows = db_session.query(SolutionRow).filter_by(**filter_by).all()
            solutions = [Solution._from_row(row) for row in rows]
            
            db_session.close()
        
        return solutions
    

    @classmethod
    def get_count(cls, filter_by:dict={}):
        '''Counts all Solution objects in the database with optional filters'''
        with database.create_session().begin() as db_session:
            count = len(
                db_session.query(SolutionRow).filter_by(**filter_by).all()
            )
            
            db_session.close()
        
        return count


    def associate_partner_row(self, partner_id=int) -> int:
        '''Insert a SolutionPartner association row in the database'''
        solution_partner_row = SolutionPartnerRow(
            solution_id=self.id,
            partner_id=partner_id
        )

        with database.create_session().begin() as db_session:
            db_session.add(solution_partner_row)
            db_session.flush()
            solution_partner_row_id = solution_partner_row.id

        return solution_partner_row_id
    

    def get_partner_ids(self):
        '''Get all the Partner ids linked to the Solution object'''
        partner_ids = []

        if self.id:
            with database.create_session().begin() as db_session:
                solution_partner_rows = db_session.query(
                    SolutionPartnerRow
                ).filter_by(
                    solution_id=self.id
                ).all()

                partner_ids = [
                    solution_partner_row.partner_id
                    for solution_partner_row in solution_partner_rows
                ]
                
                db_session.close()
        
        return partner_ids