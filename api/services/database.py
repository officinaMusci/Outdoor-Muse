import os
import math

from dotenv import load_dotenv
from sqlalchemy import create_engine, event
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
        'outdoor_muse.db'
    )

    engine = create_engine(
        engine
        or os.getenv('DB_ENGINE')
        or f"sqlite:///{default_db_path}"
    )
    
    @event.listens_for(engine, 'connect')
    def create_functions_on_connect(dbapi_connection, connection_record):
        '''Add missing functions to SQLite'''
        dbapi_connection.create_function('sin', 1, math.sin)
        dbapi_connection.create_function('cos', 1, math.cos)
        dbapi_connection.create_function('acos', 1, math.acos)
        dbapi_connection.create_function('radians', 1, math.radians)
        dbapi_connection.create_function('m_to_mi', 1, lambda m: int(m) * 0.000621371)
    
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine)
    
    return Session