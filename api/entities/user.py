from dataclasses import dataclass
from datetime import datetime
from random import randrange

from sqlalchemy import Column as ORMColumn
from sqlalchemy import DateTime as ORMDateTime
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import String as ORMString
from sqlalchemy import Boolean as ORMBoolean
from sqlalchemy.orm import relationship
from werkzeug import security
import flask_jwt_extended as flask_jwt

from services import database
from utils import time
from utils.faker import faker


class UserRow(database.Base):
    '''ORM User row representation'''
    __tablename__ = 'user'

    id = ORMColumn(ORMInteger, primary_key=True, autoincrement=True)
    created = ORMColumn(ORMDateTime, default=datetime.utcnow)
    updated = ORMColumn(ORMDateTime, default=datetime.utcnow)
    email = ORMColumn(ORMString, nullable=False)
    password = ORMColumn(ORMString, nullable=False)
    confirmed = ORMColumn(ORMBoolean, default=False)
    role = ORMColumn(ORMString, default='user')
    name = ORMColumn(ORMString, nullable=True)
    points = ORMColumn(ORMInteger, default=0)

    queries = relationship('QueryRow')
    reviews = relationship('ReviewRow')


@dataclass
class User:
    '''User dataclass.

    It represents a user.
    
    Attributes:
        id: The unique ID for the database.
        created: The date the database row was created.
        updated: The latest date the database row has been updated.
        email: The user email address.
        password: The user authentication password.
        confirmed: If the user has been confirmed.
        role: The user role.
        name: The user name.
        points: The points earned by the user.
    '''
    email:str
    password:str
    confirmed:bool=False
    role:str='user'
    name:str=None
    points:int=0

    id:int=None
    created:datetime=None
    updated:datetime=None


    @classmethod
    def generate_random(cls):
        '''Generates a random User object'''
        return User(
            email=faker.unique.email(),
            password=faker.password(),
            confirmed=False,
            role='user',
            name=faker.unique.name(),
            points=randrange(10000)
        )


    @classmethod
    def from_dict(cls, dictionary:dict):
        '''Creates and returns a User object from a dictionary'''
        return User(
            id=dictionary['id']
                if 'id' in dictionary else None,
            created=time.localize_datetime(dictionary['created'])
                if 'created' in dictionary else None,
            updated=time.localize_datetime(dictionary['updated'])
                if 'updated' in dictionary else None,
            email=dictionary['email']
                if 'email' in dictionary else None,
            password=dictionary['password'],
            confirmed=dictionary['confirmed']
                if 'confirmed' in dictionary else False,
            role=dictionary['role']
                if 'role' in dictionary else 'user',
            name=dictionary['name'],
            points=dictionary['points']
                if 'points' in dictionary else 0,
        )


    @classmethod
    def _from_row(cls, row:UserRow):
        '''Returns a User object obtained from a UserRow object'''
        return User(
            id=row.id,
            created=time.localize_datetime(row.created),
            updated=time.localize_datetime(row.updated),
            email=row.email,
            password=row.password,
            confirmed=row.confirmed,
            role=row.role,
            name=row.name,
            points=row.points
        )


    def _to_row(self) -> UserRow:
        '''Returns a UserRow object obtained from a User object'''
        return UserRow(
            id=self.id,
            created=self.created,
            updated=self.updated,
            email=self.email,
            password=self.password,
            confirmed=self.confirmed,
            role=self.role,
            name=self.name,
            points=self.points
        )


    def _insert_row(self) -> int:
        '''Insert the User row in the database'''
        self.password = security.generate_password_hash(
            self.password
        )

        user_row = self._to_row()

        with database.create_session().begin() as db_session:
            db_session.add(user_row)
            db_session.flush()
            user_id = user_row.id
        
        with database.create_session().begin() as db_session:
            user_row = db_session.query(UserRow).get(user_id)
            db_session.close()
        
        self.id = user_row.id
        self.created = time.localize_datetime(user_row.created)
        self.updated = time.localize_datetime(user_row.updated)

        return self.id


    def _update_row(self) -> int:
        '''Update the User row in the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                user_row = db_session.query(UserRow).get(self.id)

                if self.password != user_row.password:
                    self.password = security.generate_password_hash(
                        self.password
                    )

                user_row.updated = datetime.utcnow()
                user_row.email = self.email
                user_row.password = self.password
                user_row.confirmed = self.confirmed
                user_row.role = self.role
                user_row.name = self.name
                user_row.points = self.points

                db_session.flush()
            
            return self.id
        
        return None


    def _delete_row(self) -> bool:
        '''Delete the User row from the database'''
        if self.id:
            with database.create_session().begin() as db_session:
                user_row = db_session.query(UserRow).get(self.id)
                db_session.delete(user_row)
                db_session.flush()

            return True
        
        return False


    def save(self) -> int:
        '''Save the User in the database and returns the ID'''
        return self._update_row() or self._insert_row()


    def delete(self) -> bool:
        '''Delete the User from the database'''
        return self._delete_row()


    @classmethod
    def get_from_id(cls, id:int):
        '''Returns a User object obtained from a UserRow id'''
        with database.create_session().begin() as db_session:
            user_row = db_session.query(UserRow).get(id)
            user = User._from_row(user_row) if user_row else None
            
            db_session.close()
        
        return user
    
    
    @classmethod
    def get_all(cls, filter_by:dict={}):
        '''Returns all User objects from the database with optional filters'''
        with database.create_session().begin() as db_session:
            rows = db_session.query(UserRow).filter_by(**filter_by).all()
            users = [User._from_row(row) for row in User._from_row(rows)]
            
            db_session.close()
        
        return users


    def check_password(self, password:str) -> bool:
        '''Checks a password with the hashed one from the database.
    
        ARGS:
            password: the password to check.
        RETURNS:
            boolean: if the password matches or not.
        '''
        return self.password == password or security.check_password_hash(
            self.password,
            password
        )


    @classmethod
    def get_from_credentials(cls, email:str, password:str):
        '''Gets the User object corresponding to the given credentials
    
        ARGS:
            email: The User email.
            password: The User password.
        RETURNS:
            user: The User object or None if the User has not been found.
        '''
        with database.create_session().begin() as db_session:
            user_row = db_session.query(UserRow).filter_by(
                email=email
            ).first()
            
            user = User._from_row(user_row) if user_row else None
            db_session.close()
        
        if user.check_password(password):
            return user

        return None


    def create_access_token(self):
        '''Creates and returns an access token (JWT) for the User'''
        if self.id:
            return flask_jwt.create_access_token(
                identity=self.id
            )

        return None

    
    @classmethod
    def get_from_access_token(cls):
        '''Gets the User object corresponding to the session access token'''
        user_id = flask_jwt.get_jwt_identity()
        if user_id:
            return cls.get_from_id(user_id)
        
        return None