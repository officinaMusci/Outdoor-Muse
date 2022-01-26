from dataclasses import dataclass
from datetime import datetime
import random
import statistics

from sqlalchemy import Column as ORMColumn
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import String as ORMString
from sqlalchemy import Float as ORMFloat
from sqlalchemy import PickleType as ORMPickleType
from sqlalchemy.orm import relationship

from services import database
from .location import Location
from .review import Review
from .relations import QueryPartnerRow
from utils import time
from utils.faker import faker


TYPES = [
    'restaurant',
    'hotel',
    'bar'
]


class PartnerRow(database.Base):
    '''ORM Partner representation'''
    __tablename__ = 'partner'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    created = ORMColumn(ORMDateTime, default=datetime.utcnow)
    updated = ORMColumn(ORMDateTime, default=datetime.utcnow)
    name = ORMColumn(ORMString, nullable=False)
    location_lat = ORMColumn(ORMFloat, nullable=False)
    location_lng = ORMColumn(ORMFloat, nullable=False)
    types = ORMColumn(ORMPickleType, nullable=False)

    query_relations = relationship('QueryPartnerRow', cascade='delete')
    reviews = relationship('ReviewRow', cascade='delete')


@dataclass
class Partner:
    '''Partner dataclass.

    It represents a partner.
    
    Attributes:
        id: The unique ID for the database.
        created: The date the database row was created.
        updated: The latest date the database row has been updated.
        name: The partner name.
        location: The partner location.
        types: The types the partner belongs to.
        average_rating: The average rating obtained from reviews.
        query_count: The amount of query relations.
    '''
    name:str
    location:Location
    types:str

    average_rating:int=0
    query_count:int=0

    id:int=None
    created:datetime=None
    updated:datetime=None


    def __post_init__(self):
        '''Get additional data from database relations'''
        reviews = Review.get_all(filter_by={'partner_id': self.id})

        self.average_rating = statistics.mean([
            review.rating for review in reviews
        ]) if reviews else 0

        with database.create_session().begin() as db_session:
            self.query_count = len(
                db_session
                .query(QueryPartnerRow)
                .filter_by(partner_id=self.id)
                .all()
            )
            
            db_session.close()


    @classmethod
    def generate_random(cls):
        '''Generates a random Partner object'''
        coordinates = faker.local_latlng(
            country_code='CH',
            coords_only=True
        )

        return Partner(
            name=faker.unique.company(),
            location=Location.from_dict({
                'lat': coordinates[0],
                'lng': coordinates[1]
            }),
            types=random.sample(TYPES, 1)
        )


    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates and returns a Partner object from a dictionary'''
        return Partner(
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
            location=Location.from_dict(dictionary['location']),
            types=dictionary['types']
        )


    @classmethod
    def _from_row(cls, row:PartnerRow):
        '''Returns a Partner object obtained from a PartnerRow object'''
        return Partner(
            id=row.id,
            created=time.localize_datetime(row.created),
            updated=time.localize_datetime(row.updated),
            name=row.name,
            location=Location(
                lat=row.location_lat,
                lng=row.location_lng
            ),
            types=row.types
        )


    def _to_row(self) -> PartnerRow:
        '''Returns a PartnerRow object obtained from a Partner object'''
        return PartnerRow(
            id=self.id,
            created=self.created,
            updated=self.updated,
            name=self.name,
            location_lat=self.location.lat,
            location_lng=self.location.lng,
            types=self.types
        )


    def _insert_row(self) -> int:
        '''Insert the Partner row in the database'''
        partner_row = self._to_row()

        with database.create_session().begin() as db_session:
            db_session.add(partner_row)
            db_session.flush()
            partner_id = partner_row.id
        
        with database.create_session().begin() as db_session:
            partner_row = db_session.query(PartnerRow).get(partner_id)
            db_session.close()
        
        self.id = partner_row.id
        self.created = time.localize_datetime(partner_row.created)
        self.updated = time.localize_datetime(partner_row.updated)

        return self.id


    def _update_row(self) -> int:
        '''Update the Partner row in the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                partner_row = db_session.query(PartnerRow).get(self.id)

                partner_row.updated = datetime.utcnow()
                partner_row.name = self.name
                partner_row.location = self.location
                partner_row.types = self.types

                db_session.flush()
                
            return self.id
        
        return None


    def _delete_row(self) -> bool:
        '''Delete the Partner row from the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                partner_row = db_session.query(PartnerRow).get(self.id)
                db_session.delete(partner_row)
                db_session.flush()
            
            return True
        
        return False


    def save(self) -> int:
        '''Save the Partner in the database'''
        return self._update_row() or self._insert_row()


    def delete(self) -> bool:
        '''Delete the Partner from the database'''
        return self._delete_row()

    @classmethod
    def get_from_id(cls, id:int):
        '''Returns a Partner object obtained from a PartnerRow id'''
        with database.create_session().begin() as db_session:
            partner_row = db_session.query(PartnerRow).get(id)
            partner = Partner._from_row(partner_row) if partner_row else None
            
            db_session.close()
        
        return partner
        
    
    @classmethod
    def get_all(cls, filter_by:dict={}):
        '''Returns all Partner objects from the database with optional filters'''
        with database.create_session().begin() as db_session:
            rows = db_session.query(PartnerRow).filter_by(**filter_by).all()
            partners = [Partner._from_row(row) for row in rows]
            
            db_session.close()
        
        return partners