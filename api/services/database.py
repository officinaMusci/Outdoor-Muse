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
    default_db_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'outdoor_muse.sqlite'
    )

    engine = create_engine(
        engine
        or os.getenv('DB_ENGINE')
        or f"sqlite:///{default_db_path}"
    )
    
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine)
    
    return Session