from dataclasses import dataclass
from datetime import datetime
from random import randrange

from sqlalchemy import Column as ORMColumn
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import String as ORMString
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from services import database
from utils import time
from utils.faker import faker


class CommentRow(database.Base):
    '''ORM Comment representation'''
    __tablename__ = 'comment'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    created = ORMColumn(ORMDateTime, default=datetime.utcnow)
    updated = ORMColumn(ORMDateTime, default=datetime.utcnow)
    content = ORMColumn(ORMString, nullable=False)
    user_id = ORMColumn(ORMInteger, ForeignKey('user.id'), nullable=True)
    parent_id = ORMColumn(
        ORMInteger,
        ForeignKey('comment.id'),
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

    parent = relationship('CommentRow', cascade='delete')


@dataclass
class Comment:
    '''Comment dataclass.

    It represents a comment.
    
    Attributes:
        id: The unique ID for the database.
        created: The date the database row was created.
        updated: The latest date the database row has been updated.
        content: The content of the comment.
        user_id: The user id of the author.
        parent_id: The parent comment id if this comment is a reply to it.
        partner_id: The id of the partner to which the comment refers.
        place_id: The id of the place to which the comment refers.
    '''
    content:str
    user_id:int=None
    
    parent_id:int=None
    partner_id:int=None
    place_id:int=None

    id:int=None
    created:datetime=None
    updated:datetime=None


    @classmethod
    def generate_random(cls):
        '''Generates a random Comment object'''
        return Comment(
            content=faker.unique.sentence(nb_words=randrange(50) + 1)
        )


    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates and returns a Comment object from a dictionary'''
        return Comment(
            id=dictionary['id']
                if 'id' in dictionary else None,
            created=time.localize_datetime(dictionary['created'])
                if 'created' in dictionary else None,
            updated=time.localize_datetime(dictionary['updated'])
                if 'updated' in dictionary else None,
            content=dictionary['content'],
            user_id=dictionary['user_id'],
            parent_id=dictionary['parent_id']
                if 'parent_id' in dictionary else 0,
            partner_id=dictionary['partner_id']
                if 'partner_id' in dictionary else 0,
            place_id=dictionary['place_id']
                if 'place_id' in dictionary else 0
        )


    @classmethod
    def _from_row(cls, row:CommentRow):
        '''Returns a Comment object obtained from a CommentRow object'''
        return Comment(
            id=row.id,
            created=time.localize_datetime(row.created),
            updated=time.localize_datetime(row.updated),
            content=row.content,
            user_id=row.user_id,
            parent_id=row.parent_id,
            partner_id=row.partner_id,
            place_id=row.place_id
        )


    def _to_row(self) -> CommentRow:
        '''Returns a CommentRow object obtained from a Comment object'''
        return CommentRow(
            content=self.content,
            user_id=self.user_id,
            parent_id=self.parent_id,
            partner_id=self.partner_id,
            place_id=self.place_id
        )


    def _insert_row(self) -> int:
        '''Insert the Comment row in the database'''
        comment_row = self._to_row()

        with database.create_session().begin() as db_session:
            db_session.add(comment_row)
            db_session.flush()
            comment_id = comment_row.id
        
        with database.create_session().begin() as db_session:
            comment_row = db_session.query(CommentRow).get(comment_id)
            db_session.close()
        
        self.id = comment_row.id
        self.created = time.localize_datetime(comment_row.created)
        self.updated = time.localize_datetime(comment_row.updated)

        return self.id


    def _update_row(self) -> bool:
        '''Update the Comment row in the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                comment_row = db_session.query(CommentRow).get(self.id)

                comment_row.updated = datetime.utcnow()
                comment_row.content = self.content
                comment_row.user_id = self.user_id
                comment_row.parent_id = self.parent_id
                comment_row.partner_id = self.partner_id
                comment_row.place_id = self.place_id

                db_session.flush()
                
            return self.id
        
        return None


    def _delete_row(self) -> bool:
        '''Delete the Comment row from the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                comment_row = db_session.query(CommentRow).get(self.id)
                db_session.delete(comment_row)
                db_session.flush()
            
            return True
        
        return False


    def save(self) -> int:
        '''Save the Comment in the database'''
        return self._update_row() or self._insert_row()


    def delete(self) -> bool:
        '''Delete the Comment from the database'''
        return self._delete_row()

    @classmethod
    def get_from_id(cls, id:int):
        '''Returns a Comment object obtained from a CommentRow id'''
        with database.create_session().begin() as db_session:
            comment_row = db_session.query(CommentRow).get(id)
            comment = Comment._from_row(comment_row) if comment_row else None
            
            db_session.close()
        
        return comment

        