from dataclasses import dataclass
from datetime import datetime
from random import randint, randrange

from sqlalchemy import Column as ORMColumn
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import String as ORMString
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from services import database
from utils import time
from utils.faker import faker


class ReviewRow(database.Base):
    '''ORM Review representation'''
    __tablename__ = 'review'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    created = ORMColumn(ORMDateTime, default=datetime.utcnow)
    updated = ORMColumn(ORMDateTime, default=datetime.utcnow)
    comment = ORMColumn(ORMString, nullable=False)
    rating = ORMColumn(ORMInteger, nullable=False)
    
    user_id = ORMColumn(ORMInteger, ForeignKey('user.id'), nullable=True)
    parent_id = ORMColumn(
        ORMInteger,
        ForeignKey('review.id'),
        nullable=True
    )
    partner_id = ORMColumn(
        ORMInteger,
        ForeignKey('partner.id'),
        nullable=True
    )
    place_id = ORMColumn(
        ORMInteger,
        ForeignKey('place.id'),
        nullable=True
    )

    parent = relationship('ReviewRow', cascade='delete')


@dataclass
class Review:
    '''Review dataclass.

    It represents a review with a rating and a comment.
    
    Attributes:
        id: The unique ID for the database.
        created: The date the database row was created.
        updated: The latest date the database row has been updated.
        rating: The rating of the review.
        comment: The comment of the review.
        user_id: The user id of the author.
        parent_id: The parent review id if this review is a reply to it.
        partner_id: The id of the partner to which the review refers.
        place_id: The id of the place to which the review refers.
    '''
    rating:int
    comment:str=''

    user_id:int=None
    parent_id:int=None
    partner_id:int=None
    place_id:int=None

    id:int=None
    created:datetime=None
    updated:datetime=None


    @classmethod
    def generate_random(cls):
        '''Generates a random Review object'''
        return Review(
            comment=faker.sentence(nb_words=randrange(50)),
            rating=randint(1, 5)
        )


    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates and returns a Review object from a dictionary'''
        return Review(
            id=dictionary['id']
                if 'id' in dictionary else None,
            created=time.localize_datetime(dictionary['created'])
                if 'created' in dictionary else None,
            updated=time.localize_datetime(dictionary['updated'])
                if 'updated' in dictionary else None,
            rating=dictionary['rating'],
            comment=dictionary['comment']
                if 'comment' in dictionary else '',
            user_id=dictionary['user_id']
                if 'user_id' in dictionary else None,
            parent_id=dictionary['parent_id']
                if 'parent_id' in dictionary else 0,
            partner_id=dictionary['partner_id']
                if 'partner_id' in dictionary else 0,
            place_id=dictionary['place_id']
                if 'place_id' in dictionary else 0
        )


    @classmethod
    def _from_row(cls, row:ReviewRow):
        '''Returns a Review object obtained from a ReviewRow object'''
        return Review(
            id=row.id,
            created=time.localize_datetime(row.created),
            updated=time.localize_datetime(row.updated),
            rating=row.rating,
            comment=row.comment,
            user_id=row.user_id,
            parent_id=row.parent_id,
            partner_id=row.partner_id,
            place_id=row.place_id
        )


    def _to_row(self) -> ReviewRow:
        '''Returns a ReviewRow object obtained from a Review object'''
        return ReviewRow(
            rating=self.rating,
            comment=self.comment,
            user_id=self.user_id,
            parent_id=self.parent_id,
            partner_id=self.partner_id,
            place_id=self.place_id
        )


    def _insert_row(self) -> int:
        '''Insert the Review row in the database'''
        review_row = self._to_row()

        with database.create_session().begin() as db_session:
            db_session.add(review_row)
            db_session.flush()
            review_id = review_row.id
        
        with database.create_session().begin() as db_session:
            review_row = db_session.query(ReviewRow).get(review_id)
            db_session.close()
        
        self.id = review_row.id
        self.created = time.localize_datetime(review_row.created)
        self.updated = time.localize_datetime(review_row.updated)

        return self.id


    def _update_row(self) -> int:
        '''Update the Review row in the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                review_row = db_session.query(ReviewRow).get(self.id)

                review_row.updated = datetime.utcnow()
                review_row.rating = self.rating
                review_row.comment = self.comment
                review_row.user_id = self.user_id
                review_row.parent_id = self.parent_id
                review_row.partner_id = self.partner_id
                review_row.place_id = self.place_id

                db_session.flush()
                
            return self.id
        
        return None


    def _delete_row(self) -> bool:
        '''Delete the Review row from the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                review_row = db_session.query(ReviewRow).get(self.id)
                db_session.delete(review_row)
                db_session.flush()
            
            return True
        
        return False


    def save(self) -> int:
        '''Save the Review in the database'''
        return self._update_row() or self._insert_row()


    def delete(self) -> bool:
        '''Delete the Review from the database'''
        return self._delete_row()

    @classmethod
    def get_from_id(cls, id:int):
        '''Returns a Review object obtained from a ReviewRow id'''
        with database.create_session().begin() as db_session:
            review_row = db_session.query(ReviewRow).get(id)
            review = Review._from_row(review_row) if review_row else None
            
            db_session.close()
        
        return review

    
    @classmethod
    def get_all(cls, filter_by:dict={}):
        '''Returns all Review objects from the database with optional filters'''
        with database.create_session().begin() as db_session:
            rows = db_session.query(ReviewRow).filter_by(**filter_by).all()
            reviews = [Review._from_row(row) for row in rows]
            
            db_session.close()
        
        return reviews