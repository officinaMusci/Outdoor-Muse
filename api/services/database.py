import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()


'''Base class'''
Base = declarative_base()


def create_session(engine=None):
    '''Creates a database session.
    
    ARGS:
        engine: The database engine, it uses the DB_ENGINE environment variable.
        or a SQLite database if no engine has been declared.

    RETURNS:
        Session: The SQLAlchemy database session class.
    '''
    engine = create_engine(
        engine
        or os.getenv('DB_ENGINE')
        or 'sqlite:///outdoor_muse.db'
    )
    
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine)
    return Session